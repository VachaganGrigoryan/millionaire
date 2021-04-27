from django.test import TestCase
from quiz.models import Question, Option


class QuestionTestCase(TestCase):
    def setUp(self):
        op1 = Option.objects.create(body='Option 1')
        op2 = Option.objects.create(body='Option 2')
        op3 = Option.objects.create(body='Option 3')
        op4 = Option.objects.create(body='Option 4')
        q = Question.objects.create(content='Question 1', answer=op3, coin=5)

    def test_data_output(self):
        q = Question.objects.all()
        print(q)
        self.assertEqual(q)