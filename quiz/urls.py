from django.urls import path
from quiz import views

urlpatterns = [
    path('new/', views.new_game, name="new-game"),
    path('answer/<str:title>', views.answer, name="answer"),
    path('game/<str:title>', views.game, name="game")
    # path('post/<int:pk>-<str:slug>/', views.post_detail, name='post-detail'),
]