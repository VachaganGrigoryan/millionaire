from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    questions = models.ManyToManyField('Question', max_length=5, related_name='questions')
    created_at = models.DateTimeField(auto_created=True)
    total = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Quizzes"
        ordering = ['id']

    def __str__(self):
        return self.title


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField(blank=False)
    coin = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Questions"
        ordering = ['id']

    def __str__(self):
        return self.content


class Option(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    body = models.TextField(blank=False)
    correct = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Question Options"
        ordering = ['id']

    def __str__(self):
        return self.body


class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question')
    selected = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='selected')

    class Meta:
        verbose_name_plural = "Quiz Answers"
        unique_together = ['quiz', 'question']
        ordering = ['id']

    def __str__(self):
        return self.selected.body