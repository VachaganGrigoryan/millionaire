from django.contrib import admin
from .models import Quiz, Question, Option, Answer


class GameBoardAdmin(admin.ModelAdmin):
    list_display = ('owner', 'winner', 'created', 'is_ended')


class HistoriesAdmin(admin.ModelAdmin):
    list_display = ('game_board', 'board', 'step', 'step_by', 'step_date')


admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Answer)