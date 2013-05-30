from django.contrib import admin
from django.db.models.loading import get_models
from django.db.models import Q
from django import forms

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


class CategoryAdminForm(forms.ModelForm):
    
    def clean(self):
        cleaned_data = super(CategoryAdminForm, self).clean()
        #get the name of the potential_parent_category
        potential_parent_category_name = cleaned_data.get("name")
        #get the objects of the potential_child_category
        potential_child_category = cleaned_data.get("child_categories")
        temp = potential_child_category
        if potential_parent_category_name and potential_child_category:
            # get the object of the potential_parent_category
            potential_parent_category = Category.objects.filter(name = potential_parent_category_name)
            #for item in potential_parent_category:
                #print(item.name)                           ################
            # save the potiential_conflict
            potential_conflict_category = potential_child_category.filter(child_categories__in = potential_parent_category)
            print(not potential_conflict_category.all())   ################
            while (not potential_conflict_category):
                for item in potential_child_category.all():
                    print("child name is:"+item.name)       ################
                    print("\n")                             ################
                    potential_child_category = item.child_categories
                    print(potential_child_category.all())         ################
                    for item in potential_child_category.all():
                        print("child of child name is: " + item.name)   #############
                        print("\n")                                     #############
                    potential_conflict_category = potential_child_category.filter(child_categories__in = potential_parent_category)
                    if potential_conflict_category:
                        print("I am here")                              #############
                        c = ""
                        for item in temp: #potential_conflict_category:
                            c = c +" \" " + item.name + " \" "
                        raise forms.ValidationError("Current category has already been a child category of "+ c + " !")
                        return cleaned_data
                if (not potential_child_category.all()):
                    print("11111")                                      ##############
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


class CategoryInlineForm(forms.ModelForm):
    
    def clean(self):
        cleaned_data = super(CategoryInlineForm, self).clean()
        #get the name of the potential_parent_category
        potential_parent_category_name = cleaned_data.get("name")
        potential_parent_category = Category.objects.filter(name = potential_parent_category_name)
        #get the objects of the potential_child_category
        #print(potential_parent_category)                       #######################
        potential_child_category = cleaned_data.get("child_categories")
        temp = potential_child_category
        potential_conflict_category = potential_child_category.filter(child_categories__in = potential_parent_category)
        while (not potential_conflict_category.all()):
            for item in potential_child_category.all():
                #print("direct potential child "+item.name)     #######################
                #print(potential_parent_category)               #######################
                potential_child_category = item.child_categories
                #for item in potential_child_category.all():
                    #print("potential child of child " + item.name)      ######################
                #print(not potential_child_category.all())
                if (not potential_child_category.all()):
                    print("*********11111*********no potential_child_of_child_category exist!!!*************")     ##############
                    return cleaned_data
                potential_conflict_category = potential_child_category.filter(child_categories__in=potential_parent_category)
                if potential_conflict_category:
                    print("********there is a conflict with potential_child_of_child_category!!!!***********")                         #######################
                    c = ""
                    for item in temp:
                        c = c +" \" " + item.name + " \" "
                    raise forms.ValidationError("Current category has already been a child category of "+ c + " !")
                    return cleaned_data
            if (not potential_child_category.all()):
                print("*********22222*********no potential_child_of_child_category exist!!!*************")
                return cleaned_data
        if potential_conflict_category:
            print("I have the direct inverse relation!")
            c = ""
            for item in potential_conflict_category:
                c = c +" \" " + item.name + " \" "
            raise forms.ValidationError("Current category has already been a child category of "+ c + " !")
            return cleaned_data
        return cleaned_data


class CategoryInline(admin.StackedInline):
    model = Category
    form = CategoryInlineForm
    extra = 3
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "child_categories":
            kwargs["queryset"] = Category.objects.filter(parent_class__author=request.user)
        return super(CategoryInline, self).formfield_for_manytomany(db_field, request, **kwargs)


    
class ClassAdmin(admin.ModelAdmin):
    exclude = ('author',)
    inlines = [CategoryInline]

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

admin.site.register(BaseCategory)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Atom, AtomAdmin)
admin.site.register(Exposition)
admin.site.register(Submission)
admin.site.register(Vote)
admin.site.register(VoteCategory)
admin.site.register(Class, ClassAdmin)
admin.site.register(LectureNote, LectureNoteAdmin)

