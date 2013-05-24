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


admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionChoice, QuestionChoiceAdmin)
admin.site.register(Assignment)
