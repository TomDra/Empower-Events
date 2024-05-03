from django.test import TestCase
from django.utils import timezone
from .models import User, ActivityLeader, Charity, Feedback, Calendar, Activity, AgeGroup
import json

class ModelTestCase(TestCase):
    def setUp(self):
        # Create test data for User
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        self.user_disabilities = {'visual_impairment': True, 'hearing_impairment': False}
        self.user.set_disabilities(self.user_disabilities)

        # Create test data for Charity
        self.charity = Charity.objects.create_charity(charity_name='Test Charity', email='charity@example.com',
                                                      password='testpass')

        # Create test data for ActivityLeader
        self.activity_leader = ActivityLeader.objects.create(name='John Doe', birth_date=timezone.now(),
                                                             charity=self.charity, email='john@example.com')

        # Create test data for AgeGroup
        self.age_group = AgeGroup.objects.create(age_range_lower=10, age_range_higher=15, group_title='Kids')

        # Create test data for Activity
        self.activity_disabilities = {'visual_impairment': True, 'hearing_impairment': True}
        self.activity = Activity.objects.create(description='Test Activity', latitude=0, longitude=0,
                                                age_group=self.age_group,
                                                compatible_disabilities=self.activity_disabilities,
                                                charity=self.charity)

        # Create test data for Calendar
        self.calendar_event = Calendar.objects.create(activity=self.activity, time=timezone.now(),
                                                      activity_leader=self.activity_leader)

        # Create test data for Feedback
        self.feedback_user_answers = {'question1': 'answer1', 'question2': 'answer2'}
        self.feedback = Feedback.objects.create(user=self.user, calendar_event=self.calendar_event,
                                                activity_feedback_text='Good', leader_feedback_text='Nice',
                                                activity_feedback_question_answers=self.feedback_user_answers)

    def test_user_disabilities(self):
        self.assertEqual(self.user.get_disabilities(), self.user_disabilities)

    def test_activity_compatible_disabilities(self):
        self.assertEqual(self.activity.compatible_disabilities, self.activity_disabilities)

    def test_feedback_user_answers(self):
        self.assertEqual(self.feedback.activity_feedback_question_answers, self.feedback_user_answers)

    def test_charity_str(self):
        self.assertEqual(str(self.charity), 'Test Charity')

    def test_age_group_str(self):
        self.assertEqual(str(self.age_group.group_title), 'Kids')

    def test_activity_leader_email(self):
        self.assertEqual(self.activity_leader.email, 'john@example.com')

    def test_feedback_audio_none(self):
        self.assertIsNone(self.feedback.activity_feedback_audio)
        self.assertIsNone(self.feedback.leader_feedback_audio)

    def test_user_creation(self):
        self.assertEqual(User.objects.count(), 1)

    def test_activity_creation(self):
        self.assertEqual(Activity.objects.count(), 1)

    def test_calendar_creation(self):
        self.assertEqual(Calendar.objects.count(), 1)

    def test_feedback_creation(self):
        self.assertEqual(Feedback.objects.count(), 1)

    def test_age_group_creation(self):
        self.assertEqual(AgeGroup.objects.count(), 1)

    def test_activity_leader_creation(self):
        self.assertEqual(ActivityLeader.objects.count(), 1)

    def test_charity_creation(self):
        self.assertEqual(Charity.objects.count(), 1)