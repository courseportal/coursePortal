from django.contrib import admin
from django.db.models.loading import get_models
from django.db.models import Q
from web.models import *

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


class CategoryAdmin(admin.ModelAdmin):
    inlines = [ExposInline]

    #This is a dirty hack, but it works, a more elegant solution should
    #be implemented in the future.  This works because this function is called
    #after django overwrites the m2m field, unlike save_model, so I just put the
    #code in here.
    def log_change(self, request, obj, message):
        super(CategoryAdmin, self).log_change(request, obj, message)
        for parent in obj.parent.all():
            for parent_parent in parent.parent.all():
                if parent_parent != None:
                    obj.parent.add(parent_parent)
                    obj.parent.remove(parent)
        obj.save()

    
class ClassAdmin(admin.ModelAdmin):
    exclude = ('author',)

    
    #This is a dirty hack, but it works, a more elegant solution should
    #be implemented in the future.  This works because this function is called
    #after django overwrites the m2m field, unlike save_model, so I just put the
    #code in here.

    
    
    def log_change(self, request, obj, message):
        super(ClassAdmin, self).log_change(request, obj, message)
        child_categories = obj.categories.exclude(parent=None)
        for child in child_categories.all():
            for parent in child.parent.all():
                if parent != None:
                    obj.categories.add(parent)
        obj.save()
    
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
admin.site.register(Exposition)
admin.site.register(Submission)
admin.site.register(Vote)
admin.site.register(VoteCategory)
admin.site.register(Class, ClassAdmin)
admin.site.register(LectureNote, LectureNoteAdmin)