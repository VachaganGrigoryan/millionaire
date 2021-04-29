from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    class QuizStatus(models.TextChoices):
        in_progress = 'Ընթացքի մեջ'
        closed = 'Ընդատված'
        done = 'Ավարտված'

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    questions = models.ManyToManyField('Question', max_length=5, related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True)
    total = models.PositiveIntegerField(default=0)
    status = models.CharField(choices=QuizStatus.choices, default=QuizStatus.in_progress, max_length=12)

    class Meta:
        verbose_name_plural = "Quizzes"
        ordering = ['id']

    def __str__(self):
        return self.title

    def election(self, question_id, answer):
        question = self.questions.get(id=56).exists()
        print(question)
        # question.check_answer(answer)


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField(blank=False)
    coin = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Questions"
        ordering = ['id']

    def check_answer(self, option):
        print(self.options.all())

    def __repr__(self):
        return f"Question('{self.id}', '{self.content}')"

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