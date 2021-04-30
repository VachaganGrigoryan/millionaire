from django.db import models
from django.contrib.auth.models import User


class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='question')
    selected = models.ForeignKey('Option', on_delete=models.CASCADE, related_name='selected')

    class Meta:
        verbose_name_plural = "Quiz Answers"
        unique_together = ['quiz', 'question']
        ordering = ['id']

    def __str__(self):
        return self.selected.body


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
        quiz_answer = None
        question = self.questions.all().filter(id=question_id).first()
        if question:
            option = question.check_answer(answer)
            if option:
                quiz_answer = Answer.objects.create(
                    quiz=self,
                    question=question,
                    selected=option
                )

        return quiz_answer

    def is_answered_question(self, question_id):
        return self.answers.all().filter(question_id=question_id).first()


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField(blank=False)
    coin = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Questions"
        ordering = ['id']

    def check_answer(self, option_body):
        option = self.options.all().filter(body=option_body).first()
        return option

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

