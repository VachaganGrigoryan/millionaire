from django.contrib import admin
from django.db.models import Q

from .models import Quiz, Question, Option, Answer


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'status', 'total', 'created_at']
    search_fields = ['title']
    list_display_links = ('title',)


class QuizQuestionsFilter(admin.SimpleListFilter):
    title = 'Quiz'
    parameter_name = 'quiz'

    def lookups(self, request, model_admin):
        quizzes = Quiz.objects.all()
        lookups = ()
        for quiz in quizzes:
            lookups += ((quiz.id, quiz.title),)
        return lookups

    def queryset(self, request, queryset):

        if self.value():
            quiz_id = self.value()
            return queryset.filter(Q(questions__id=quiz_id))


class OptionInlineAdmin(admin.TabularInline):
    model = Option
    extra = 0
    min_num = 2


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = [
        'content',
        'coin',
    ]
    list_display = ['id', 'content', 'coin']
    list_display_links = ('content',)
    inlines = [OptionInlineAdmin, ]
    list_filter = [QuizQuestionsFilter, ]
    search_fields = ['content']


class QuestionOptionsFilter(admin.SimpleListFilter):
    title = 'Question'
    parameter_name = 'question'

    def lookups(self, request, model_admin):
        questions = Question.objects.all()
        lookups = ()
        for question in questions:
            lookups += ((question.id, question.content),)
        return lookups

    def queryset(self, request, queryset):
        if self.value():
            question_id = self.value()
            return queryset.filter(Q(question__id=question_id))


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'body', 'correct', 'question']
    list_filter = [QuestionOptionsFilter, ]
    list_display_links = ('body',)


class QuizAnswersFilter(admin.SimpleListFilter):
    title = 'Quiz '
    parameter_name = 'quiz'

    def lookups(self, request, model_admin):
        quizzes = Quiz.objects.all()
        lookups = ()
        for quiz in quizzes:
            lookups += ((quiz.id, quiz.title),)
        return lookups

    def queryset(self, request, queryset):
        if self.value():
            quiz_id = self.value()
            return queryset.filter(Q(quiz__id=quiz_id))


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'quiz', 'question', 'selected']
    list_filter = [QuizAnswersFilter, ]
    list_display_links = ('quiz',)
