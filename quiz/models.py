from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    questions = models.ManyToManyField('Question', max_length=5, related_name='questions')
    total = models.PositiveIntegerField(default=0)


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField(blank=False)
    options = models.ManyToManyField('Option', blank=True, related_name='options')
    answer = models.ForeignKey('Option', on_delete=models.PROTECT, related_name='answer')
    coin = models.PositiveIntegerField(default=0)


class Option(models.Model):
    id = models.AutoField(primary_key=True)
    # question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, related_name='options')
    body = models.TextField(blank=False)


class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question')
    selected = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='selected')

    class Meta:
        unique_together = ['quiz', 'question']