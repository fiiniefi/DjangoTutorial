from django.contrib import admin

from .models import Question, Choice


class AdminSite(admin.AdminSite):
    admin.AdminSite.site_header = 'Polls-app administration'


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Question text', {'fields': ['question_text']}),
        ('Date of publication', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInLine]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date', 'question_text']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
