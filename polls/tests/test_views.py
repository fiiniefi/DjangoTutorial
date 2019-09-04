from django.urls import reverse
from django.utils import timezone
from django.test import TestCase
from polls.models import Question


def create_question(text, days=0):
    time = timezone.now() + timezone.timedelta(days=days)
    return Question.objects.create(question_text=text, pub_date=time)


class TestIndex(TestCase):
    def test_noQuestions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls.')
        self.assertQuerysetEqual(response.context['latest_questions'], [])

    def test_questionExists(self):
        create_question('Question')
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['latest_questions']), 1)
        self.assertEqual(response.context['latest_questions'][0].question_text, 'Question')

    def test_futureQuestionDoesNotAppear(self):
        create_question('Question', days=1)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['latest_questions']), 0)


class TestDetail(TestCase):
    def test_futureQuestionDoesNotAppear(self):
        question = create_question('Question', days=1)
        response = self.client.get(reverse('polls:detail', args=(question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_questionExists(self):
        question = create_question('Question')
        response = self.client.get(reverse('polls:detail', args=(question.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question.question_text)
