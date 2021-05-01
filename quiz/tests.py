from django.contrib.auth.models import User
from django.test import TestCase

from quiz.models import Question, Option, Quiz


class QuestionTestCase(TestCase):
    def setUp(self):
        q_1 = Question.objects.create(content='Question 1', coin=5)
        Option.objects.create(question=q_1, body='Option 1', correct=False)
        Option.objects.create(question=q_1, body='Option 2', correct=False)
        Option.objects.create(question=q_1, body='Option 3', correct=True)
        Option.objects.create(question=q_1, body='Option 4', correct=False)

    def test_data_output(self):
        q_1 = Question.objects.get(content='Question 1')
        self.assertTrue(q_1)
        self.assertTrue(q_1.options.exists())
        op_2 = Option.objects.get(body='Option 2')
        self.assertEqual(q_1.get_option('Option 2'), op_2)


class QuizTestCase(TestCase):
    def setUp(self):
        q_1 = Question.objects.create(content='Question 1', coin=5)
        Option.objects.create(question=q_1, body='Option 1', correct=True)
        Option.objects.create(question=q_1, body='Option 2', correct=False)
        q_2 = Question.objects.create(content='Question 2', coin=5)
        Option.objects.create(question=q_2, body='Option 1', correct=True)
        Option.objects.create(question=q_2, body='Option 2', correct=False)
        q_3 = Question.objects.create(content='Question 3', coin=5)
        Option.objects.create(question=q_3, body='Option 1', correct=True)
        Option.objects.create(question=q_3, body='Option 2', correct=False)
        q_4 = Question.objects.create(content='Question 4', coin=5)
        Option.objects.create(question=q_4, body='Option 1', correct=True)
        Option.objects.create(question=q_4, body='Option 2', correct=False)
        q_5 = Question.objects.create(content='Question 5', coin=5)
        Option.objects.create(question=q_5, body='Option 1', correct=True)
        Option.objects.create(question=q_5, body='Option 2', correct=False)

        us_1 = User.objects.create(username='kikos', password='password')

        qz_1 = Quiz.objects.create(
            title='Quiz 1',
            user=us_1,
        )
        qz_1.set_questions([q_1, q_2, q_3, q_4, q_5])

    def test_data_output(self):
        qz_1 = Quiz.objects.get(title='Quiz 1')
        self.assertTrue(qz_1)
        self.assertTrue(qz_1.questions.exists())

        qz_1.election(2, 'Option 1')
        qz_1.election(2, 'Option 1')
        self.assertEqual(qz_1.total, 5)

        self.assertFalse(qz_1.is_answered_question(1))
        qz_1.election(1, 'Option 2')
        self.assertTrue(qz_1.is_answered_question(1))
        self.assertEqual(qz_1.total, 5)

        qz_1.election(5, 'Option 1')
        self.assertTrue(qz_1.is_answered_question(5))
        self.assertEqual(qz_1.total, 10)
