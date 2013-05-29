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


class CategoryAdmin(admin.ModelAdmin):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "child_category":
            kwargs["queryset"] = Category.objects.filter(classBelong__author=request.user)
        return super(CategoryAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
        
    def queryset(self, request):
    	#form = CategoryAdminForm(request.user)
        qs = super(CategoryAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(Q(classBelong__allowed_users = request.user) | Q(classBelong__author = request.user))


class CategoryInline(admin.StackedInline):
	model = Category
	extra = 3
	
	#def formfield_for_manytomany(self, db_field, request, **kwargs):
    #	if db_field.name == "child_category":
       # 	kwargs["queryset"] = Category.objects.filter(classBelong__author=request.user)
    #	return super(CategoryInline, self).formfield_for_manytomany(db_field, request, **kwargs)		


    
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

admin.site.register(Category, CategoryAdmin)
admin.site.register(Atom, AtomAdmin)
admin.site.register(Exposition)
admin.site.register(Submission)
admin.site.register(Vote)
admin.site.register(VoteCategory)
admin.site.register(Class, ClassAdmin)
admin.site.register(LectureNote, LectureNoteAdmin)

