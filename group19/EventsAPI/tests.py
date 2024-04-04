# Importing the necessary modules and classes.
import datetime
import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from myapi.models import ActivityLeader, Activity, Calendar, Charity, AgeGroup

# Getting the User model from Django
User = get_user_model()


# Base test case for the EventsAPI
class EventsAPITest(TestCase):
    def setUp(self):
        """
        Set up the test case with a test client and a test models.
        """
        self.client = APIClient()

        self.user1 = User.objects.create_user(username='user1', password='testpass123', email='user1@email.com')
        self.user2 = User.objects.create_user(username='user2', password='testpass123', email='user2@email.com')

        self.charity1 = Charity.objects.create(charity_name='Charity 1', email='charity1@email.com',
                                               password='testpass123')
        self.charity2 = Charity.objects.create(charity_name='Charity 2', email='charity2@email.com',
                                               password='testpass123')

        self.age_group1 = AgeGroup.objects.create(age_range_lower=10, age_range_higher=20, group_title='Group 1')
        self.age_group2 = AgeGroup.objects.create(age_range_lower=20, age_range_higher=30, group_title='Group 2')

        self.activity_leader1 = ActivityLeader.objects.create(user=self.user1, name='Test Leader 1',
                                                              birth_date=timezone.now(), charity=self.charity1)
        self.activity_leader2 = ActivityLeader.objects.create(user=self.user2, name='Test Leader 2',
                                                              birth_date=timezone.now(), charity=self.charity2)

        self.activity1 = Activity.objects.create(description='Test Activity 1', latitude=0.0, longitude=0.0,
                                                 charity=self.charity1, age_group=self.age_group1)
        self.activity2 = Activity.objects.create(description='Test Activity 2', latitude=0.0, longitude=0.0,
                                                 charity=self.charity2, age_group=self.age_group2)

        self.calendar1 = Calendar.objects.create(activity=self.activity1,
                                                 time=timezone.now() + datetime.timedelta(days=1),
                                                 activity_leader=self.activity_leader1)
        self.calendar2 = Calendar.objects.create(activity=self.activity2,
                                                 time=timezone.now() + datetime.timedelta(days=2),
                                                 activity_leader=self.activity_leader2)


class UpcomingEventsListTest(EventsAPITest):
    # Test upcoming events list
    def test_get_paginated_events_count_2(self):
        """
        Test that the upcoming events list is paginated and contains two events.
        """
        # Log in a user.
        self.client.force_authenticate(user=self.user1)

        # GET the events list
        response = self.client.get(reverse('list_events_upcoming'), {'page': 1})

        # Print the JSON response
        print(json.dumps(response.data, indent=4))

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response contains the correct number of events
        self.assertEqual(len(response.data['results']), 2)

        # Checking count, next, previous, and results keys in the response.
        self.assertEqual(response.data['count'], 2)
        # Two events fit into one page, so there should be no next or previous pages.
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])

        # Check the first event in the list
        # TODO: Make it extensive.
        event1 = response.data['results'][0]
        self.assertEqual(event1['activity']['description'], 'Test Activity 1')
        self.assertEqual(event1['activity_leader']['name'], 'Test Leader 1')

        # Check the second event in the list
        # TODO: Make it extensive.
        event2 = response.data['results'][1]
        self.assertEqual(event2['activity']['description'], 'Test Activity 2')
        self.assertEqual(event2['activity_leader']['name'], 'Test Leader 2')
