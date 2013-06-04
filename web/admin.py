from django.contrib import admin
from django.db.models.loading import get_models
from django.db.models import Q
from django import forms
from django.forms.models import BaseModelFormSet, modelformset_factory, BaseInlineFormSet
from django.forms.formsets import formset_factory
from sets import Set

for m in get_models():
    exec "from %s import %s" % (m.__module__, m.__name__)

class ExposInline(admin.StackedInline):
    model = Exposition
    extra = 3

class LectureNoteAdmin(admin.ModelAdmin):
    exclude = ('owner',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
            obj.save()
        super(LectureNoteAdmin, self).save_model(request, obj, form, change)

class AtomAdmin(admin.ModelAdmin):
    inlines = [ExposInline]


class BaseCategoryAdminForm(forms.ModelForm):
    
    def clean(self):
        cleaned_data = super(BaseCategoryAdminForm, self).clean()
        potential_parent_category_name = cleaned_data.get("name")
        potential_child_category = cleaned_data.get("child_categories")
        temp = potential_child_category
        if potential_parent_category_name and potential_child_category:
            potential_parent_category = BaseCategory.objects.filter(name = potential_parent_category_name)
            potential_conflict_category = potential_child_category.filter(child_categories__in = potential_parent_category)
            while (not potential_conflict_category):
                for item in potential_child_category.all():
                    potential_child_category = item.child_categories
                    potential_conflict_category = potential_child_category.filter(child_categories__in = potential_parent_category)
                    if potential_conflict_category:
                        print("There is a conflict!!!")
                        c = ""
                        for item in temp:
                            c = c +" \" " + item.name + " \" "
                        raise forms.ValidationError("Current category has already been a child category of "+ c + " !")
                        return cleaned_data
                if (not potential_child_category.all()):
                    print("Returned Correctly!!!")
                    return cleaned_data
            if potential_conflict_category:
                print("I have the direct inverse relation!")
                c = ""
                for item in potential_conflict_category:
                    c = c +" \" " + item.name + " \" "
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
        #return qs.filter(Q(parent_class__allowed_users = request.user) | Q(parent_class__author = request.user))


class CategoryAdminForm(forms.ModelForm):
  
    def clean(self):
        cleaned_data = super(CategoryAdminForm, self).clean()
        potential_parent_category_name = cleaned_data.get("name")
        potential_child_category = cleaned_data.get("child_categories")
        temp = potential_child_category
        if potential_parent_category_name and potential_child_category:
            potential_parent_category = Category.objects.filter(name = potential_parent_category_name)
            potential_conflict_category = potential_child_category.filter(child_categories__in = potential_parent_category)
            while (not potential_conflict_category):
                for item in potential_child_category.all():
                    potential_child_category = item.child_categories
                    potential_conflict_category = potential_child_category.filter(child_categories__in = potential_parent_category)
                    if potential_conflict_category:
                        print("There is a conflict!!!")                         
                        c = ""
                        for item in temp:
                            c = c +" \" " + item.name + " \" "
                        raise forms.ValidationError("Current category has already been a child category of "+ c + " !")
                        return cleaned_data
                if (not potential_child_category.all()):
                    print("Returned Correctly!!!")
                    return cleaned_data
            if potential_conflict_category:
                print("I have the direct inverse relation!")
                c = ""
                for item in potential_conflict_category:
                    c = c +" \" " + item.name + " \" "
                raise forms.ValidationError("Current category has already been a child category of "+ c + " !")
                return cleaned_data
        return cleaned_data



class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    filter_horizontal=("child_categories","child_atoms",)
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if request.path != "/admin/web/category/add/":
            if db_field.name == "child_categories":
                #retrieve the category id from request.path
                temp0 = "/admin/web/category/"
                temp1 = "/"
                temp2 = request.path.split(temp0,1)[1]
                category_id = int(temp2.split(temp1,1)[0])
                #erase the current category from form field "child_categories" 
                kwargs["queryset"] = Category.objects.filter(parent_class__author=request.user).exclude(pk = category_id)
            return super(CategoryAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
        return super(CategoryAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    
    def queryset(self, request):
        qs = super(CategoryAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(Q(parent_class__allowed_users = request.user) | Q(parent_class__author = request.user))


def TestChild(potential_parent, potential_child, CategoryDict):
    """
    Recursive funtion to test potential loop in CategoryInlineFormSet
    """
    if potential_parent == potential_child:
        return False
    else:
        if potential_child in CategoryDict.keys():
            for temp_child in CategoryDict[potential_child]:
                if TestChild(potential_parent, temp_child, CategoryDict) == False:
                    return False
    return True



class CategoryInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super(CategoryInlineFormSet, self).clean()
        CategoryDict = {}
        for form in self.forms:
            potential_parent_name = form.cleaned_data.get("name")
            potential_parent_object = Category.objects.filter(name = potential_parent_name)
            for p_p_o in potential_parent_object.all():
                potential_parent = str(p_p_o.name.split('Category:',1))
            potential_children = form.cleaned_data.get("child_categories")
            if potential_children:
                S=set()
                for item in potential_children.all():
                    potential_child = str(item.name.split('Category:',1))
                    for group in CategoryDict.values():
                        for g in group:
                            if potential_parent == g:
                                temp_child = potential_child
                                temp_parent = potential_parent
                                if not TestChild(temp_parent, temp_child, CategoryDict):
                                   raise forms.ValidationError("There is a loop between "+ temp_child +" and " + temp_parent+" !") 
                    S.add(potential_child)
                    CategoryDict[potential_parent] = S
                
            


class CategoryInline(admin.StackedInline):
    model = Category
    formset = CategoryInlineFormSet
    filter_horizontal=("child_categories","child_atoms",)
    extra = 2

    
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name','status')
    lsit_display_links = ('status')
    exclude = ('author',)
    inlines = [CategoryInline]
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
            if isinstance(inline, CategoryInline) and obj is None:
                continue
            yield inline.get_formset(request, obj)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
            obj.save()
        super(ClassAdmin, self).save_model(request, obj, form, change)
    
    def has_change_permission(self, request, obj=None):
        if obj==None:
            return True
        elif request.user.is_superuser or obj.author == request.user or obj.allowed_users.filter(username=request.user).exists():
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if obj==None:
            return True
        elif request.user.is_superuser or obj.author == request.user or obj.allowed_users.filter(username=request.user).exists():
            return True
        return False

    def queryset(self, request):
        qs = super(ClassAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(Q(allowed_users = request.user) | Q(author = request.user))

    #the class author will never be listed in "allowed_users" field
    def get_form(self, request, obj=None, **kwargs):
        form = super(ClassAdmin, self).get_form(request, obj, **kwargs)
        if obj == None:
            potential_user = User.objects.all().exclude(username = request.user)
            form.base_fields["allowed_users"].queryset=potential_user
        else:
            potential_user = User.objects.all().exclude(username = obj.author)
            form.base_fields["allowed_users"].queryset=potential_user
        return form


class SubmissionAdminForm(forms.ModelForm):
    
    def clean(self):
        cleaned_data = super(SubmissionAdminForm, self).clean()
        video = cleaned_data.get("video")
        if video.startswith("[\"") and video.endswith("\"]"):
            video_raw_num = video.strip('["]')
            print(video_raw_num)
        else:
            video_raw_num = video
        if not video_raw_num.isalnum() or not len(video_raw_num)==11:
            raise forms.ValidationError("Something wrong with the 11 character or [\"VIDEO_ID\"]!")
        return cleaned_data


class SubmissionAdmin(admin.ModelAdmin):
    form = SubmissionAdminForm

    def save_model(self, request, obj, form, change):
        if change:
            if not obj.video.startswith("[\""):
                print("I am NOT with [\" ")
                print(obj.video)
                obj.video = "[\""+obj.video+"\"]"
                obj.save()
                print(obj.video)
            print("I am with [\" ")
        super(SubmissionAdmin, self).save_model(request, obj, form, change)


admin.site.register(BaseCategory,BaseCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Atom, AtomAdmin)
admin.site.register(Exposition)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Vote)
admin.site.register(VoteCategory)
admin.site.register(Class, ClassAdmin)
admin.site.register(LectureNote, LectureNoteAdmin)

