"""
Test cases for the Feedback API.
"""
import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from myapi.models import Charity, AgeGroup, ActivityLeader, Activity, Calendar, Feedback
from rest_framework import status
from rest_framework.test import APIClient

# Getting the User model from Django
User = get_user_model()


# TODO: Implement more tests for the Feedback API
# Base test case for the Feedback API
class FeedbackAPITest(TestCase):
    def setUp(self):
        """
        Set up the test case with a test client and test models.
        """
        self.client = APIClient()

        # Creating users
        self.user1 = User.objects.create_user(username='user1', password='password', email='testfeedback1@email.com')
        self.user2 = User.objects.create_user(username='user2', password='password', email='testfeedback2@email.com')
        self.user3 = User.objects.create_user(username='user3', password='password', email='testfeedback3@email.com')
        self.user4 = User.objects.create_user(username='user4', password='password', email='testfeedback4@email.com')
        self.user5 = User.objects.create_user(username='user5', password='password', email='testfeedback5@email.com')

        # Creating a charity
        self.charity = Charity.objects.create(charity_name='Charity', email='charity@email.com',
                                              password='testpass123')

        # Creating an age group
        self.age_group = AgeGroup.objects.create(age_range_lower=10, age_range_higher=20, group_title='Test Group')

        # Create an activity leader using user1
        self.activity_leader = ActivityLeader.objects.create(name='Test Leader',
                                                             birth_date=timezone.now(), charity=self.charity)

        # Create an activity
        self.activity = Activity.objects.create(description='Test Activity', latitude=0.0, longitude=0.0,
                                                charity=self.charity, age_group=self.age_group)
        self.activity.set_compatible_disabilities(["Test Disability 1", "Test Disability 2"])
        self.activity.save()

        # Create a calendar event
        self.calendar = Calendar.objects.create(activity=self.activity,
                                                time=timezone.now(),
                                                activity_leader=self.activity_leader)

        # User and leader feedback
        feedback_data = [
            {"user_id": self.user2.id,
             "activity_feedback_text": "This event was a great experience! I was really happy to be there.",
             "leader_feedback_text": "The activity leader was fantastic! Very organized and engaging."},
            {"user_id": self.user3.id,
             "activity_feedback_text": "This event was okay. I think it could have been a better experience.",
             "leader_feedback_text": "While the activity leader was knowledgeable, they could improve on providing "
                                     "clearer instructions."},
            {"user_id": self.user4.id,
             "activity_feedback_text": "This event was a terrible experience. I didn't enjoy it at all.",
             "leader_feedback_text": "Kudos to the activity leader for their creativity and passion in leading the "
                                     "activity, but there were some moments where communication could have been "
                                     "clearer."},
            {"user_id": self.user5.id,
             "activity_feedback_text": "This event was an amazing time! I loved every minute of it.",
             "leader_feedback_text": "We had a great time thanks to the activity leader's enthusiasm and energy."},
        ]

        # Assign feedback to the event
        for feedback in feedback_data:
            Feedback.objects.create(user_id=feedback['user_id'], calendar_event=self.calendar,
                                    activity_feedback_text=feedback['activity_feedback_text'],
                                    leader_feedback_text=feedback['leader_feedback_text'])

    def test_feedback_overview(self):
        """
        Test the feedback overview API endpoint.
        """

        # Log in as a charity
        self.client.force_authenticate(user=self.charity)

        # GET request to the feedback overview endpoint
        response = self.client.get(reverse('feedback_overview', kwargs={'activity_id': self.activity.activity_id}))

        # Print the JSON response
        print(json.dumps(response.data, indent=4))

        # Assert that the status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_leader_feedback_list(self):
        """
        Test the leader feedback list API endpoint.
        """

        # Log in as a charity
        self.client.force_authenticate(user=self.charity)

        # GET request to the leader feedback list endpoint
        response = self.client.get(reverse('leader_feedback_list', kwargs={'activity_id': self.activity.activity_id}))

        # Print the JSON response
        print(json.dumps(response.data, indent=4))

        # Assert that the status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_feedback_submission(self):
        """
        Test the feedback submission API endpoint.
        """

        # Log in a user
        self.client.force_authenticate(user=self.user1)

        # Feedback data
        feedback_data = {
            "calendar_event": self.calendar.event_id,
            "activity_feedback_text": "This event was amazing! I had a great time.",
            "activity_feedback_audio": None,
            "leader_feedback_text": "The activity leader was fantastic! Very engaging and supportive.",
            "leader_feedback_audio": None
        }

        # POST request to the feedback submission endpoint
        response = self.client.post(reverse('feedback_submission',
                                            kwargs={'activity_id': self.activity.activity_id}), feedback_data,
                                    format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the feedback is stored in the database
        feedback = Feedback.objects.get(feedback_id=response.data['feedback_id'])
        self.assertEqual(feedback.activity_feedback_text, feedback_data['activity_feedback_text'])
        self.assertEqual(feedback.leader_feedback_text, feedback_data['leader_feedback_text'])
