from django.contrib import admin
from django.db.models.loading import get_models
for m in get_models():
    exec "from %s import %s" % (m.__module__, m.__name__)

class ChoicesInline(admin.TabularInline):
    model = QuestionChoice
    extra = 0

class VarsInline(admin.TabularInline):
    model = QuestionVariable
    extra = 0


class QuestionChoiceAdmin(admin.ModelAdmin):
    add_form_template = 'question/admin/change_form.html'

class QuestionAdmin(admin.ModelAdmin):
    add_form_template = 'question/admin/change_form.html'
    change_form_template = 'question/admin/change_form.html'
    inlines = [VarsInline, ChoicesInline]


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
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionChoice, QuestionChoiceAdmin)
admin.site.register(Assignment)
admin.site.register(LectureNote)
