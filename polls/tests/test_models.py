import datetime

from django.test import TestCase
from django.utils import timezone

from polls.models import Question


class TestQuestion(TestCase):
    def test_wasPublishedRecently_withFutureQuestion(self):
        future = timezone.now() + datetime.timedelta(days=1)
        question = Question(pub_date=future)
        print(dir(question))
        self.assertIs(question.was_published_recently(), False)

    def test_wasPublishedRecently_withOldQuestion(self):
        publish_time = timezone.now() - datetime.timedelta(days=2)
        question = Question(pub_date=publish_time)
        self.assertIs(question.was_published_recently(), False)

    def test_wasPublishedRecently_withRecentQuestion(self):
        publish_time = timezone.now() - datetime.timedelta(hours=23)
        question = Question(pub_date=publish_time)
        self.assertIs(question.was_published_recently(), True)
