from django.urls import path

from quiz import views

urlpatterns = [
    path('new/', views.new_game, name="new-game"),
    path('game/<str:title>', views.game, name="game"),
    path('close/<str:title>', views.close, name="close"),
    path('answer/<str:title>', views.answer, name="answer"),
    path('score/<str:title>', views.score, name="score")
]
