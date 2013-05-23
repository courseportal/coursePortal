from django.contrib import admin
from web.models import Submission, Category, Exposition, Vote, VoteCategory, Class


class ExposInline(admin.StackedInline):
    model = Exposition
    extra = 3

class CategoryAdmin(admin.ModelAdmin):
    inlines = [ExposInline]

class ClassAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        if obj==None:
            return True
        elif request.user.is_superuser or obj.allowed_users.filter(username=request.user).exists():
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if obj==None:
            return True
        elif request.user.is_superuser or obj.allowed_users.filter(username=request.user).exists():
            return True
        return False

    def queryset(self, request):
        qs = super(ClassAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(allowed_users = request.user)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Exposition)
admin.site.register(Submission)
admin.site.register(Vote)
admin.site.register(VoteCategory)
admin.site.register(Class, ClassAdmin)

