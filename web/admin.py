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

for m in get_models():
	exec "from %s import %s" % (m.__module__, m.__name__)

class ExpositionAdmin(admin.ModelAdmin):
    exclude = ('owner',)
    
    def save_model(self, request, obj, form, change):
        if not change:
			obj.owner = request.user
			obj.save()
        super(ExpositionAdmin, self).save_model(request, obj, form, change)


class ExposInline(admin.StackedInline):
    model = Exposition
    exclude = ()
    extra = 1
    raw_id_fields = ("owner",)

class LecNoteInline(admin.StackedInline):
    model = Note
    exclude = ()
    extra = 1

class ExampleInline(admin.StackedInline):
    model = Example
    exclude = ()
    extra = 1


    #class VideoInline(admin.StackedInline):
    #model = Video.tags.through
#extra = 1



	
class FileUploadForm(forms.ModelForm):
	r"""
	Custom form for only allowing file types defined in ``knoatom/settings.py`` as ``settings.ALLOWED_FILE_EXTENSIONS``.
	"""
	
	def clean_file(self):
		r"""
		Cleans the file data to only allow certain file extensions.
		"""
		
		valid = False
		for ext in ALLOWED_FILE_EXTENTIONS:
			if self.cleaned_data['file'].name.endswith(ext):
				valid = True
		if not valid:
			raise ValidationError(u'Not valid file type, only {} are accepted.'.format(ALLOWED_FILE_EXTENTIONS))
		return self.cleaned_data['file']

class NoteAdmin(admin.ModelAdmin):
	exclude = ('owner',)
	form = FileUploadForm
	def save_model(self, request, obj, form, change):
		if not change:
			obj.owner = request.user
			obj.save()
		super(NoteAdmin, self).save_model(request, obj, form, change)
		
class ExampleAdmin(admin.ModelAdmin):
	exclude = ('owner',)
	form = FileUploadForm
	def save_model(self, request, obj, form, change):
		if not change:
			obj.owner = request.user
			obj.save()
		super(ExampleAdmin, self).save_model(request, obj, form, change)

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
	
	def clean(self):
		cleaned_data = super(BaseCategoryAdminForm, self).clean()
		potential_parent_category_name = cleaned_data.get("title")
		potential_child_category = cleaned_data.get("child_categories")
		temp = potential_child_category
		if potential_parent_category_name and potential_child_category:
			potential_parent_category = BaseCategory.objects.filter(title = potential_parent_category_name)
			potential_conflict_category = potential_child_category.filter(child_categories__in = potential_parent_category)
			while (not potential_conflict_category):
				for item in potential_child_category.all():
					potential_child_category = item.child_categories
					potential_conflict_category = potential_child_category.filter(child_categories__in = potential_parent_category)
					if potential_conflict_category:
						print("There is a conflict!!!")
						c = ""
						for item in temp:
							c = c +" \" " + item.title + " \" "
						raise forms.ValidationError("Current category has already been a child category of "+ c + " !")
						return cleaned_data
				if (not potential_child_category.all()):
					print("Returned Correctly!!!")
					return cleaned_data
			if potential_conflict_category:
				print("I have the direct inverse relation!")
				c = ""
				for item in potential_conflict_category:
					c = c +" \" " + item.title + " \" "
				raise forms.ValidationError("Current category has already been a child category of "+ c + " !")
				return cleaned_data
		return cleaned_data


class BaseCategoryAdmin(admin.ModelAdmin):
	form = BaseCategoryAdminForm
	filter_horizontal=("child_categories",)
	
	def formfield_for_manytomany(self, db_field, request, **kwargs):
		if request.path != "/admin/web/basecategory/add/":
			if db_field.name == "child_categories":
				#retrieve the category id from request.path
				temp0 = "/admin/web/basecategory/"
				temp1 = "/"
				temp2 = request.path.split(temp0,1)[1]
				category_id = int(temp2.split(temp1,1)[0])
				#erase the current category from form field "child_categories"
				kwargs["queryset"] = BaseCategory.objects.exclude(pk = category_id)
			return super(BaseCategoryAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
		return super(BaseCategoryAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
	
	
	def queryset(self, request):
		qs = super(BaseCategoryAdmin, self).queryset(request)
		if request.user.is_superuser:
			return qs
		#return qs.filter(Q(parent_class__instructors = request.user) | Q(parent_class__owner = request.user))
		
class BCAA(admin.ModelAdmin):
	fields = ('title', 'summary', 'parent_categories')


class ClassCategoryAdminForm(forms.ModelForm):
	def clean(self):
		cleaned_data = super(ClassCategoryAdminForm, self).clean()
		potential_parent_category_name = cleaned_data.get("title")
		potential_child_category = cleaned_data.get("child_categories")
		temp = potential_child_category
		if potential_parent_category_name and potential_child_category:
			potential_parent_category = ClassCategory.objects.filter(title = potential_parent_category_name)
			potential_conflict_category = potential_child_category.filter(child_categories__in = potential_parent_category)
			while (not potential_conflict_category):
				for item in potential_child_category.all():
					potential_child_category = item.child_categories
					potential_conflict_category = potential_child_category.filter(child_categories__in = potential_parent_category)
					if potential_conflict_category:
						print("There is a conflict!!!")						 
						c = ""
						for item in temp:
							c = c +" \" " + item.title + " \" "
						raise forms.ValidationError("Current category has already been a child category of "+ c + " !")
						return cleaned_data
				if (not potential_child_category.all()):
					print("Returned Correctly!!!")
					return cleaned_data
			if potential_conflict_category:
				print("I have the direct inverse relation!")
				c = ""
				for item in potential_conflict_category:
					c = c +" \" " + item.title + " \" "
				raise forms.ValidationError("Current category has already been a child category of "+ c + " !")
				return cleaned_data
		return cleaned_data


class ClassCategoryAdmin(admin.ModelAdmin):
	form = ClassCategoryAdminForm
	def formfield_for_manytomany(self, db_field, request, **kwargs):
		if request.path != "/admin/web/atomcategory/add/":
			if db_field.name == "child_categories":
				#retrieve the category id from request.path
				temp0 = "/admin/web/atomcategory/"
				temp1 = "/"
				temp2 = request.path.split(temp0,1)[1]
				category_id = int(temp2.split(temp1,1)[0])
				#erase the current category from form field "child_categories" 
				kwargs["queryset"] = ClassCategory.objects.filter(parent_class__owner=request.user).exclude(pk = category_id)
			return super(ClassCategoryAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
		return super(ClassCategoryAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
	
	def queryset(self, request):
		qs = super(ClassCategoryAdmin, self).queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(Q(parent_class__instructors = request.user) | Q(parent_class__owner = request.user))


def TestChild(potential_parent, potential_child, ClassCategoryDict):
	"""
	Recursive funtion to test potential loop in ClassCategoryInlineFormSet
	"""
	if potential_parent == potential_child:
		return False
	else:
		if potential_child in ClassCategoryDict.keys():
			for temp_child in ClassCategoryDict[potential_child]:
				if TestChild(potential_parent, temp_child, ClassCategoryDict) == False:
					return False
	return True



class ClassCategoryInlineFormSet(BaseInlineFormSet):
	def clean(self):
		super(ClassCategoryInlineFormSet, self).clean()
		ClassCategoryDict = {}
		for form in self.forms:
			potential_parent_name = form.cleaned_data.get("title")
			potential_parent_object = ClassCategory.objects.filter(title = potential_parent_name)
			for p_p_o in potential_parent_object.all():
				potential_parent = str(p_p_o.category_name.split('Category:',1))
			potential_children = form.cleaned_data.get("child_categories")
			if potential_children:
				S=set()
				for item in potential_children.all():
					potential_child = str(item.category_name.split('Category:',1))
					for group in ClassCategoryDict.values():
						for g in group:
							if potential_parent == g:
								temp_child = potential_child
								temp_parent = potential_parent
								if not TestChild(temp_parent, temp_child, ClassCategoryDict):
								   raise forms.ValidationError("There is a loop between "+ temp_child +" and " + temp_parent+" !") 
					S.add(potential_child)
					ClassCategoryDict[potential_parent] = S
				
			


class ClassCategoryInline(admin.StackedInline):
	model = ClassCategory
	formset = ClassCategoryInlineFormSet
	filter_horizontal=("child_categories","child_atoms",)
	extra = 2

	
class ClassAdmin(admin.ModelAdmin):
	list_display = ('title','status')
	lsit_display_links = ('status')
	exclude = ('owner',)
	inlines = [ClassCategoryInline]
	actions = ['make_active','make_not_active']
	
	def make_active(self, request, queryset):
		rows_updated = queryset.update(status='A')
		if rows_updated == 1:
			print("1 row")
			message_bit = "1 class was"
		else:
			print("many rows")
			message_bit = "%s classes were" % rows_updated
		self.message_user(request, "%s successfully marked as active." % message_bit)
	make_active.short_description = "Activate selected classes"
	
	def make_not_active(self, request, queryset):
		rows_updated = queryset.update(status='N')
		if rows_updated == 1:
			print("1 row")
			message_bit = "1 class was"
		else:
			print("many rows")
			message_bit = "%s classes were" % rows_updated
		self.message_user(request, "%s successfully marked as NOT active." % message_bit)
	make_not_active.short_description = "Inactivate selected classes"
		
	def get_formsets(self, request, obj=None):
		print("get_formsets is called, but not be put in use yet!!")
		for inline in self.get_inline_instances(request, obj):
			# hide MyInline in the add view
			if isinstance(inline, ClassCategoryInline) and obj is None:
				continue
			yield inline.get_formset(request, obj)

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
			potential_user = User.objects.all().exclude(user = request.user)
			form.base_fields["instructors"].queryset=potential_user
		else:
			potential_user = User.objects.all().exclude(user = obj.owner)
			form.base_fields["instructors"].queryset=potential_user
		return form

class VideoAdminForm(forms.ModelForm):
	
    def clean(self):
        cleaned_data = super(VideoAdminForm, self).clean()
        video = cleaned_data.get("video")
        if video.startswith("[\"") and video.endswith("\"]"):
            video_raw_num = video.strip('["]')
        else:
            video_raw_num = video
        if not video_raw_num.isalnum() or not len(video_raw_num)==11:
            raise forms.ValidationError("Something wrong with the 11 character or [\"VIDEO_ID\"]!")
        return cleaned_data


class VideoAdmin(admin.ModelAdmin):
    form = VideoAdminForm
    exclude = ()

    def save_model(self, request, obj, form, change):
		#if change:
        if not obj.video.startswith("[\""):
            obj.video = "[\""+obj.video+"\"]"
            obj.save()
            print(obj.video)
        super(VideoAdmin, self).save_model(request, obj, form, change)

admin.site.register(Example, ExampleAdmin)
admin.site.register(BaseCategory,BCAA)
#admin.site.register(ClassCategory, ClassCategoryAdmin)
admin.site.register(Atom, AtomAdmin)
admin.site.register(Exposition, ExpositionAdmin)
admin.site.register(Video, VideoAdmin)
#admin.site.register(Class, ClassAdmin)
admin.site.register(Note, NoteAdmin)

