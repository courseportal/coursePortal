from datetime import datetime
import re
from django.contrib.auth.models import User
from django.db import models
from haystack import indexes
from django.http import Http404
from django.db.models.signals import pre_delete, post_delete, pre_save, post_save
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.conf import settings
from rating.models import *
from rating.ratings import *
from assignment.models import Assignment



STATUS_CHOICES = (
    ('A', 'Active'),
    ('N', 'Not active'),
)

class WebBaseModel(models.Model):
    r"""Base Model for all models in web.  All models inherit these properties from it.  `title` is required"""
    title = models.CharField(max_length=200)
    date_created = models.DateTimeField(
        auto_now_add=True,
        default=datetime.now
    )
    date_modified = models.DateTimeField(
        auto_now=True,
        default=datetime.now
    )
    
    class Meta:
        abstract = True
        
    def __unicode__(self):
        return self.title

class BaseCategory(WebBaseModel):
    summary = models.TextField(
        default=_("There is currently no summary.")
    )
    parent_categories = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=False,
        related_name="child_categories"
    )
    
    class Meta:
        ordering = ['title']
        verbose_name_plural = _("Base Categories")

class Atom(WebBaseModel):
    summary = models.TextField(
        default=_("There is currently no summary.")
    )
    base_category = models.ForeignKey(BaseCategory,
        related_name="child_atoms"
    )
    #prereq = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="postreq")
    class Meta:
        ordering = ['title']
        
    def countQuestions(self):
		return self.related_questions.filter(isCopy=False).count()
    
class Content(WebBaseModel):
    LECTURE = "L"
    EXAMPLE = "E"
    READING = "R"
    HOMEWORK = "H"
    CONTENT_TYPES = (
        (LECTURE, "Presentations"),
        (EXAMPLE, "Examples"),
        (READING, "Expositions"),
        (HOMEWORK, "Problems"),
    )
    
    owner = models.ForeignKey(User, related_name="content_set")
    summary = models.TextField(
        verbose_name=_('Description'),
        help_text=_('Enter a description of the content.  HTML tags are '
            'allowed.'), # Change to markdown.
        blank=True,
    )
    content_type = models.CharField(max_length="50", choices=CONTENT_TYPES)
    atoms = models.ManyToManyField(Atom, blank=True)
    classes_stickied_in = models.ManyToManyField(
        "Class",
        blank=True,
        related_name='stickied_content',
        help_text=_('Please select the class(es) that you want this content '
            'to be stickied in.'),
    )
    
    def get_absolute_url(self, class_=None, category=None, atom=None):
        r"""Returns the absolute url of the content object with the correct GET data for the breadcrumbs."""
        if self.pk is not None:
            url = reverse('content_details', args=[self.pk])
            get = '?'
            if class_ is not None:
                get += 'class={}'.format(class_.pk)
                if category is not None or atom is not None:
                    get += '&'
            if category is not None:
                get += 'category={}'.format(category.pk)
                if atom is not None:
                    get += '&'
            if atom is not None:
                get += 'atom={}'.format(atom.pk)
            return (url + get)
        else:
            raise Http404
    
def validate_youtube_video_id(value):
    regex_vid_id = re.compile('[A-Za-z0-9-_-]{11}')
    if not regex_vid_id.match(value):
        raise ValidationError('%s is not a valid YouTube video id.' % value)
    if len(value) > 11:
        raise ValidationError('%s is not a valid YouTube video id.' % value)
    
class YoutubeVideo(models.Model):
    content = models.ForeignKey(Content, related_name="videos")
    title = models.CharField(max_length=200)
    video_id = models.CharField(
        max_length=11,
        verbose_name=_('Youtube Video Id'),
        blank=False,
        help_text=_("Please enter an 11 character YouTube VIDEO_ID (e.g. "
            "http://www.youtube.com/watch?v=VIDEO_ID)"),
        validators=[validate_youtube_video_id],
    )
    
    def __unicode__(self):
        return u"YouTube video"
    
# Validator for links
def validate_link(value):
    r"""Checks that exposition links begin with ``http://`` or ``https://``."""
    if not (re.match('^http://', value) or re.match('^https://', value)):
        raise ValidationError(u'The link must begin with http:// or https://.')
    
class Link(models.Model):
    content = models.ForeignKey(Content, related_name="links")
    title = models.CharField(max_length=200)
    link = models.URLField(
        verbose_name=_('URL'),
        blank=False,
        help_text=_("Enter a valid URL.")
        #validators=[validate_link], 
        #default="http://",
    )
    
    def __unicode__(self):
        return u"link"
    
# Validator for uploaded files
def validate_uploaded_file(value):
    r"""
    Checks that the file is of an allowed type set in ``knoatom/settings.py`` as ``settings.ALLOWED_FILE_EXTENTIONS`` and file size to be under "settings.MAX_UPLOAD_SIZE".
    """
    if value.size > int(settings.MAX_UPLOAD_SIZE):
        raise ValidationError((u'Please keep filesize under {}. Current filesize {}').format(filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(value.size)))
    valid = False
    for ext in settings.ALLOWED_FILE_EXTENSIONS:
        if value.name.endswith(ext):
            valid = True
    if not valid:
        raise ValidationError(u'Not valid file type, we only accept {} files'.format(settings.ALLOWED_FILE_EXTENSIONS))
    
class UploadedFile(models.Model):
    content = models.ForeignKey(Content, related_name="files")
    title = models.CharField(max_length=200)
    file = models.FileField(
        verbose_name=_('File'),
        help_text=_('Please select a file to upload.'),
        upload_to='files/',
        validators=[validate_uploaded_file]
    )
    
    def __unicode__(self):
        return u"file"

class Class(WebBaseModel):
    r"""
    This is the model for the class feature of the site which allows professors to create their own class pages which they can customize to fit their needs.  They can sticky content to force that material to stay at the top of the content display lists.
    
    """
    instructors = models.ManyToManyField(
        User,
        verbose_name=_('Instructors'),
        blank=True,
        related_name='allowed_classes',
        help_text=_('Creater of the class will be automatically added as instructor.'),
    )
    students = models.ManyToManyField(
        User,
        verbose_name=_('Students'),
        blank=True,
        related_name='enrolled_classes'
    )
    owner = models.ForeignKey(
        User,
        verbose_name=_('Professor'),
        related_name = 'classes_authored'
    )
    status = models.CharField(
        verbose_name=_('Status'),
        max_length=1,
        choices=STATUS_CHOICES,
        default='N'
    )
    summary = models.TextField(
        verbose_name=_('Class Description'),
        default=_("There is currently no summary.")
    )
    stickied_assignments = models.ManyToManyField(
        Assignment,
        blank=True,
        related_name='classes_stickied_in'
    )
        
    class Meta:
        ordering = ['title']
        verbose_name_plural = _("Classes")

    def get_absolute_url(self):
        if self.pk is not None:
            return reverse('classes', args=[self.pk])
        raise Http404

class ClassCategory(WebBaseModel):
    summary = models.TextField(
        default=_("There is currently no summary.")
    )
    parent_class = models.ForeignKey(
        Class,
        default=None,
        blank=True,
        null=True,
        related_name="category_set"
    )
    parent_categories = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=False,
        related_name="child_categories"
    )
    child_atoms = models.ManyToManyField(
        Atom,
        blank=True,
        related_name="categories"
    )

    class Meta:
        ordering = ['title']
        verbose_name_plural = _("Categories")

@receiver(post_save, sender=Content)
def add_example_rate(sender, **kwargs):
    if kwargs['created']:
        user_rate = UserRating.objects.get(user=kwargs['instance'].owner)
        user_rate.ContentRating += content_object_delta_rating()
        user_rate.rating += content_object_delta_rating()
        user_rate.save()

@receiver(pre_delete, sender=Content)
def delete_example_rate(sender, **kwargs):
    """
    This adds the functionality to remove the file upon deletion.
    """
    #kwargs['instance'].file.delete()
    user_rate = UserRating.objects.get(user=kwargs['instance'].owner)
    user_rate.ContentRating -= content_object_delta_rating()
    user_rate.rating -= content_object_delta_rating()
    user_vote = Vote.objects.filter(content=kwargs['instance'])
    for v in user_vote:
        if v.vote > 0:
            user_rate.VoteUp -= vote_up_delta_rating()
            user_rate.rating -= vote_up_delta_rating()
        elif v.vote < 0:
            user_rate.VoteDown -= vote_down_delta_rating()
            user_rate.rating -= vote_down_delta_rating()
    user_rate.save()
