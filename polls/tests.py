import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls import reverse # URL을 하드코딩하지 않도록

# 자동화된 테스트를 사용하기 위한 코드
# test를 작성하기 위해, 파일 이름은 tests로 작성되어야 함
# 테스트용 함수의 prefix는 test로 시작되어야 함
# 테스트 코드는 기능을 더욱 명확하게 하며, 충분할수록 좋다.
def create_question(question_text, days):
    # Create a question with the given `question_text` and published the
    # given number of `days` offset to now (negative for questions published
    # in the past, positive for questions that have yet to be published).
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    # 상황만 다르고 패턴은 같은 테스트 함수들
    def test_no_questions(self):
        # If no questions exist, an appropriate message is displayed.
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200) 
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        # Questions with a pub_date in the past are displayed on the index page.
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        # Questions with a pub_date in the future aren't displayed on the index page.
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        # Even if both past and future questions exist, only past questions are displayed.
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        # The questions index page may display multiple questions. 
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        # 미래 시점의 pub_date는 was_published_recently() 함수에서 false를 리턴해야 한다.
        time = timezone.now() + datetime.timedelta(days=30) # 현재 시간에 30일을 더한 날짜를 저장
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False) # False return을 기대한다는 코드


    # 1일 이전에 대한 question은 False가 나와야 한다는 test code
    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)


    # 1일이 넘어가지 않으면 True가 나와야 한다는 test code
    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, second=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)