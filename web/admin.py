from django.contrib import admin
from django.db.models.loading import get_models
from django.db.models import Q
from django import forms
from django.forms.models import BaseModelFormSet, modelformset_factory, BaseInlineFormSet
from django.forms.formsets import formset_factory
from django.core.exceptions import ObjectDoesNotExist, ValidationError
#from sets import Set
from django.conf import settings

# Import ForumInlineAdmin
from pybb.models import Forum, Category
from web.forms.edit_class import CategoryForm
#import autocomplete_light

for m in get_models():
    exec "from %s import %s" % (m.__module__, m.__name__)


# class ExpositionAdmin(admin.ModelAdmin):
#     exclude = ('owner',)
#     
#     def save_model(self, request, obj, form, change):
#         if not change:
#             obj.owner = request.user
#             obj.save()
#         super(ExpositionAdmin, self).save_model(request, obj, form, change)
# 
# 
# class ExposInline(admin.StackedInline):
#     model = Exposition
#     exclude = ()
#     extra = 1
#     raw_id_fields = ("owner",)
# 
# class LecNoteInline(admin.StackedInline):
#     model = Note
#     exclude = ()
#     extra = 1
# 
# class ExampleInline(admin.StackedInline):
#     model = Example
#     exclude = ()
#     extra = 1
#     
# class FileUploadForm(forms.ModelForm):
#     r"""
#     Custom form for only allowing file types defined in ``knoatom/settings.py`` as ``settings.ALLOWED_FILE_EXTENSIONS``.
#     """
#     
#     def clean_file(self):
#         r"""
#         Cleans the file data to only allow certain file extensions.
#         """
#         
#         valid = False
#         for ext in ALLOWED_FILE_EXTENTIONS:
#             if self.cleaned_data['file'].name.endswith(ext):
#                 valid = True
#         if not valid:
#             raise ValidationError(u'Not valid file type, only {} are accepted.'.format(ALLOWED_FILE_EXTENTIONS))
#         return self.cleaned_data['file']
# 
# class NoteAdmin(admin.ModelAdmin):
#     exclude = ('owner',)
#     form = FileUploadForm
#     def save_model(self, request, obj, form, change):
#         if not change:
#             obj.owner = request.user
#             obj.save()
#         super(NoteAdmin, self).save_model(request, obj, form, change)
#         
# class ExampleAdmin(admin.ModelAdmin):
#     exclude = ('owner',)
#     form = FileUploadForm
#     def save_model(self, request, obj, form, change):
#         if not change:
#             obj.owner = request.user
#             obj.save()
#         super(ExampleAdmin, self).save_model(request, obj, form, change)

class AtomAdmin(admin.ModelAdmin):
    """
        Admin for the Atom model, automatically creates/updates/deletes the coorsponding forum when the Atom gets created/updated/deleted.
    """
    #inlines = [ExposInline, LecNoteInline, ExampleInline]

    def save_model(self, request, obj, form, change):
        """
            If the model is already created we update the coorsponding forum, or if there is none, we create it.
        """
    
        cat = Category.objects.get_or_create(name="Atoms")[0]
        if change:
            try:
                forum = Forum.objects.get(atom=obj)
            except ObjectDoesNotExist:
                    forum = Forum.objects.create(
                        atom=obj,
                        category=cat,
                        name=obj.title,
                        description=obj.summary # Add when we have field
                    )
                    forum.save()
                    forum.moderators.add(request.user)
                
            forum.name = obj.title
            forum.save()
            #forum.moderators.add(request.user)
            #obj.forum.description = obj.description
        obj.save()
    
    
    def log_addition(self, request, obj):
        """
        If a forum does not exist for the Atom we create it.
        
        This is a bit of a hack because the save_model method doesn't work properly for using the obj when it doesn't exist yet.  This method only ever does anything when the Atom is first created.
        """
        cat = Category.objects.get_or_create(name="Atoms")[0]
        try:
            forum = Forum.objects.get(atom=obj)
        except ObjectDoesNotExist:
            forum = Forum.objects.create(
                    atom=obj,
                    category=cat,
                    name=obj.title,
                    description=obj.summary # Add when we have field
                )
            forum.save()
            forum.moderators.add(request.user)

class BaseCategoryAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        r"""Sets the queryset of categories not include itself."""
        super(BaseCategoryAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk is not None: # Exclude self to prevent loops
            self.fields['parent_categories'].queryset = (
                BaseCategory.objects.exclude(pk=self.instance.pk)
            )
    
    def clean_parent_categories(self):
        data = self.cleaned_data
        if self.instance.pk is not None:
            if (self.instance.child_categories.filter(pk=self.instance.pk)):
                print "Validation Error"
                raise forms.ValidationError(_("There is an infinite loop in the categories."))
            parent_categories = data.get('parent_categories').all()
            if (self.instance.child_categories.filter(id__in=parent_categories)
                    .exists()):
                print "Validation Error indirect"
                raise forms.ValidationError(_("There is an indirect infinite loop in the categories"))
        return data['parent_categories']
        
    class Meta:
        model = BaseCategory
        fields=('title', 'summary', 'parent_categories')

class BaseCategoryAdmin(admin.ModelAdmin):
    form = BaseCategoryAdminForm
    filter_horizontal=("parent_categories",)


class CategoryAdminForm(forms.ModelForm):
    r"""
    Form for category editing outside of a class editing form.
    
    .. warning::
    
        This form assumes that you are only editing **one** category at a time.  Otherwise infinite loops can be formed.
    
    """
    
    class Meta:
        r"""Set the model it is attached to and select the fields."""
        model = ClassCategory
        
    def clean_parent_categories(self):
        data = self.cleaned_data
        parent_categories = data.get('parent_categories').all()
        if (parent_categories.exclude(
                parent_class=data.get('parent_class')).exists()):
            raise forms.ValidationError("The parent categories must be in the class {}".format(data.get('parent_class')))
        if self.instance.pk is not None:
            if (self.instance.child_categories.filter(pk=self.instance.pk)
                    .exists()):
                raise forms.ValidationError("There is an infinite loop in the categories.")
            if (self.instance.child_categories.filter(id__in=parent_categories)
                    .exists()):
                raise forms.ValidationError("There is an indirect infinite loop in the categories")
        return data.get('parent_categories')


class ClassCategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    filter_horizontal=("parent_categories",)
    
class ClassAdmin(admin.ModelAdmin):
    list_display = ('title','status')
    fields = ('title', 'status', 'summary', 'instructors', 'students')
    
    # def make_active(self, request, queryset):
  #       rows_updated = queryset.update(status='A')
  #       if rows_updated == 1:
  #           print("1 row")
  #           message_bit = "1 class was"
  #       else:
  #           print("many rows")
  #           message_bit = "%s classes were" % rows_updated
  #       self.message_user(request, "%s successfully marked as active." % message_bit)
  #   make_active.short_description = "Activate selected classes"
  #   
  #   def make_not_active(self, request, queryset):
  #       rows_updated = queryset.update(status='N')
  #       if rows_updated == 1:
  #           print("1 row")
  #           message_bit = "1 class was"
  #       else:
  #           print("many rows")
  #           message_bit = "%s classes were" % rows_updated
  #       self.message_user(request, "%s successfully marked as NOT active." % message_bit)
  #   make_not_active.short_description = "Inactivate selected classes"

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
            obj.save()
        super(ClassAdmin, self).save_model(request, obj, form, change)
    
    def has_change_permission(self, request, obj=None):
        if obj==None:
            return True
        elif request.user.is_superuser or obj.owner == request.user or obj.instructors.filter(user=request.user).exists():
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if obj==None:
            return True
        elif request.user.is_superuser or obj.owner == request.user or obj.instructors.filter(user=request.user).exists():
            return True
        return False

    def queryset(self, request):
        qs = super(ClassAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(Q(instructors = request.user) | Q(owner = request.user))
    
    #the class owner will never be listed in "instructors" field
    def get_form(self, request, obj=None, **kwargs):
        form = super(ClassAdmin, self).get_form(request, obj, **kwargs)
        if obj == None:
            potential_user = User.objects.all().exclude(pk=request.user.pk)
            form.base_fields["instructors"].queryset=potential_user
        else:
            potential_user = User.objects.all().exclude(pk=obj.owner.pk)
            form.base_fields["instructors"].queryset=potential_user
        return form

# class VideoAdminForm(forms.ModelForm):
#     
#     def clean(self):
#         cleaned_data = super(VideoAdminForm, self).clean()
#         video = cleaned_data.get("video")
#         if not video.isalnum() or not len(video)==11:
#             raise forms.ValidationError("Something wrong with the 11 character VIDEO_ID!")
#         return cleaned_data


#admin.site.register(Example, ExampleAdmin)
admin.site.register(BaseCategory,BaseCategoryAdmin)
admin.site.register(ClassCategory, ClassCategoryAdmin)
admin.site.register(Atom, AtomAdmin)
#admin.site.register(Exposition, ExpositionAdmin)
#admin.site.register(Video, VideoAdmin)
admin.site.register(Class, ClassAdmin)
#admin.site.register(Note, NoteAdmin)
admin.site.register(Content)

