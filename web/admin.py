from django.contrib import admin
from web.models import Submission, Category, Exposition, Vote, VoteCategory

class ExposInline(admin.StackedInline):
    model = Exposition
    extra = 3

class CategoryAdmin(admin.ModelAdmin):
    inlines = [ExposInline]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Exposition)
admin.site.register(Submission)
admin.site.register(Vote)
admin.site.register(VoteCategory)
