from django.contrib import admin
from django.db.models import Count
from django.template.loader import get_template

from .models import Quiz, Question, Answer,Result
from nested_inline.admin import NestedStackedInline, NestedModelAdmin


# Register your models here.


class AnswerInline(NestedStackedInline):
    model = Answer
    readonly_fields = ['question']
    extra = 1


class QuestionInline(NestedStackedInline):
    model = Question
    inlines = [AnswerInline]
    extra = 1


class QuestionAdmin(NestedModelAdmin):
    inlines = [AnswerInline]


class QuizAdmin(NestedModelAdmin):
    inlines = [QuestionInline]
    list_filter = ["is_show", "created"]

    def get_question_count(self, obj):
        return obj.question_set.count()

    list_display = ('title', 'is_show', 'created','get_question_count')
    get_question_count.short_description = ("Кількість питань")


class ResultAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'user', 'score','completed')


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question,QuestionAdmin)
admin.site.register(Result,ResultAdmin)
