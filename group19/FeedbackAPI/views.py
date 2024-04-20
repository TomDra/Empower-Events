"""
Views module for the FeedbackAPI app.
"""
import os

import joblib
from django.conf import settings
from django.core.cache import cache
from nltk.corpus import stopwords
from rest_framework import status, permissions, pagination, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from textblob import TextBlob
import nltk
from collections import Counter

from .permissions import IsCharityOrActivityLeader
from .serializers import FeedbackOverviewSerializer, ActivityFeedbackListSerializer, LeaderFeedbackListSerializer, \
    FeedbackSubmissionSerializer
from myapi.models import Feedback

from .validators import validate_feedback_text

# Download the stopwords
nltk.download('stopwords')


class FeedbackOverview(APIView):
    """
    FeedbackOverview class is a subclass of APIView. It conducts sentiment,
    objectivity, adjective, word and phrase analysis. It also caches the data to help with performance.

    It contains the following methods:
    - get: A method that analyses the feedback for a specific activity and returns the aforementioned data.
    """
    permission_classes = [permissions.IsAuthenticated, IsCharityOrActivityLeader]

    def get(self, request, activity_id):
        """
        A method that analyses the feedback for a specific activity and returns:
        - Average user sentiment
        - Average leader sentiment
        - Average user subjectivity
        - Average leader subjectivity
        - Adjectives used in user feedback
        - Adjectives used in leader feedback
        - Most common words in user feedback
        - Most common words in leader feedback
        - Most common phrases in user feedback
        - Most common phrases in leader feedback

        The data is cached for 1 hour to help with performance.

        :param request: The request object.
        :param activity_id: The id of the activity.
        """

        # Check if the data is in the cache
        cache_data = cache.get(f'feedback_overview_{activity_id}')

        # If the cache does not exist, calculate the data.
        if cache_data is None:

            # Getting all the feedback for a specific activity.
            cache_feedback = cache.get(f'feedback_{activity_id}')

            if cache_feedback is None:
                feedback = Feedback.objects.filter(calendar_event__activity_id=activity_id)
                cache.set(f'feedback_{activity_id}', feedback, timeout=3600)

            feedback = cache_feedback

            # Calculate average user and leader sentiment and subjectivity
            user_sentiments = [TextBlob(f.activity_feedback_text).sentiment.polarity for f in
                               feedback if f.activity_feedback_text]
            leader_sentiments = [TextBlob(f.leader_feedback_text).sentiment.polarity for f in
                                 feedback if f.leader_feedback_text]
            user_subjectivities = [TextBlob(f.activity_feedback_text).sentiment.subjectivity for f in
                                   feedback if f.activity_feedback_text]
            leader_subjectivities = [TextBlob(f.leader_feedback_text).sentiment.subjectivity for f in
                                     feedback if f.leader_feedback_text]

            # Calculate the average sentiment and subjectivity
            average_user_sentiment = sum(user_sentiments) / len(user_sentiments) if user_sentiments else None
            average_leader_sentiment = sum(leader_sentiments) / len(leader_sentiments) if leader_sentiments else None
            average_user_subjectivity = sum(user_subjectivities) / len(
                user_subjectivities) if user_subjectivities else None
            average_leader_subjectivity = sum(leader_subjectivities) / len(leader_subjectivities) \
                if leader_subjectivities else None

            # Analyse adjectives used in feedback, (JJ, JJR, JJS are adjective tags)
            user_adjectives = [word for f in feedback if f.activity_feedback_text for word, tag in
                               TextBlob(f.activity_feedback_text).tags if
                               tag in ('JJ', 'JJR', 'JJS')]
            leader_adjectives = [word for f in feedback if f.leader_feedback_text for word, tag in
                                 TextBlob(f.leader_feedback_text).tags if
                                 tag in ('JJ', 'JJR', 'JJS')]

            # Define stop words
            stop_words = set(stopwords.words('english'))

            # Calculate word and phrase frequency. Removing stop words.
            n = 10  # Limit the number of words/phrases to 10
            user_word_freq = Counter(word for f in feedback if f.activity_feedback_text
                                     for word in TextBlob(f.activity_feedback_text).words
                                     if word.lower() not in stop_words).most_common(n)
            leader_word_freq = Counter(word for f in feedback if f.leader_feedback_text
                                       for word in TextBlob(f.leader_feedback_text).words
                                       if word.lower() not in stop_words).most_common(n)
            user_phrase_freq = Counter(phrase for f in feedback if f.activity_feedback_text for phrase in
                                       TextBlob(f.activity_feedback_text).noun_phrases).most_common(n)
            leader_phrase_freq = Counter(phrase for f in feedback if f.leader_feedback_text for phrase in
                                         TextBlob(f.leader_feedback_text).noun_phrases).most_common(n)

            # Define the absolute path to the files for the classifier and vectorizer
            classifier_path = os.path.join(settings.BASE_DIR, 'FeedbackAPI', 'FeedbackClassifier',
                                           'feedback_classifier.pkl')
            vectorizer_path = os.path.join(settings.BASE_DIR, 'FeedbackAPI', 'FeedbackClassifier',
                                           'feedback_vectorizer.pkl')

            # Load the files
            clf = joblib.load(classifier_path)
            vectorizer = joblib.load(vectorizer_path)

            # Classify the feedback
            feedback_classification = []
            for f in feedback:
                # Check if the feedback is not empty
                if f.activity_feedback_text:
                    # Transform the feedback into a vector
                    X = vectorizer.transform([f.activity_feedback_text])

                    # Predict the classification
                    classification = clf.predict(X)[0]

                    # Append the feedback and classification to the list
                    feedback_classification.append((f, classification, 'activity_feedback_text'))

                # Check if the feedback is not empty
                if f.leader_feedback_text:
                    # Transform the feedback into a vector
                    X = vectorizer.transform([f.leader_feedback_text])

                    # Predict the classification
                    classification = clf.predict(X)[0]

                    # Append the feedback and classification to the list
                    feedback_classification.append((f, classification, 'leader_feedback_text'))

            # Sort the feedback by classification
            feedback_classification.sort(key=lambda x: x[1], reverse=True)

            # Get the top 5 possible improvements and accomplishments, that are not 'Neither' e.g. useless feedback
            possible_improvements = [f[0].activity_feedback_text if f[2] == 'activity_feedback_text' else f[
                0].leader_feedback_text for f in feedback_classification if
                                     f[1] == 'Improvements' and f[1] != 'Neither'][:5]
            possible_accomplishments = [f[0].activity_feedback_text if f[2] == 'activity_feedback_text' else f[
                0].leader_feedback_text for f in feedback_classification if
                                        f[1] == 'Accomplishments' and f[1] != 'Neither'][:5]

            # Create a dictionary with the analysed data
            data = {
                'average_user_sentiment': average_user_sentiment,
                'average_leader_sentiment': average_leader_sentiment,
                'average_user_subjectivity': average_user_subjectivity,
                'average_leader_subjectivity': average_leader_subjectivity,
                'possible_improvements': possible_improvements,
                'possible_accomplishments': possible_accomplishments,
                'user_adjectives': user_adjectives,
                'leader_adjectives': leader_adjectives,
                'user_word_freq': dict(user_word_freq),
                'leader_word_freq': dict(leader_word_freq),
                'user_phrase_freq': dict(user_phrase_freq),
                'leader_phrase_freq': dict(leader_phrase_freq)
            }

            # Cache the data for 1 hour
            cache.set(f'feedback_overview_{activity_id}', data, timeout=3600)

            # Set the cache data
            cache_data = data

        # Serialise the data
        serializer = FeedbackOverviewSerializer(cache_data)

        # Return the data
        return Response(serializer.data, status=status.HTTP_200_OK)


class ActivityFeedbackList(generics.ListAPIView):
    """
    ActivityFeedbackList class is a subclass of ListAPIView. It allows users to view a list of feedback for an activity.
    It implements caching to help with performance. It implements pagination to limit the number of
    feedback items returned.

    It contains the following methods:
    - get_queryset (GET): A method that returns a list of feedback for an activity.
    """

    permission_classes = [permissions.IsAuthenticated, IsCharityOrActivityLeader]
    pagination_class = pagination.PageNumberPagination
    serializer_class = ActivityFeedbackListSerializer

    def get_queryset(self):
        """
        A method that returns a list of feedback for an activity.

        :return: A list of feedback for an activity.
        """

        # Get the activity id from the URL
        activity_id = self.kwargs['activity_id']

        # Check if the data is in the cache
        cache_feedback = cache.get(f'feedback_{activity_id}')

        # If the cache does not exist, get the feedback from the database
        if cache_feedback is None:
            feedback = Feedback.objects.filter(calendar_event__activity_id=activity_id).order_by('feedback_id')
            cache.set(f'feedback_{activity_id}', feedback, timeout=3600)
        else:
            # If the cache exists, use the cached data
            feedback = cache_feedback
        return feedback


class LeaderFeedbackList(generics.ListAPIView):
    """
    LeaderFeedbackList class is a subclass of ListAPIView. It allows users to view a list of feedback for a leader.
    It implements caching to help with performance. It implements pagination to limit the number of
    feedback items returned.

    It contains the following methods:
    - get_queryset (GET): A method that returns a list of feedback for a leader.
    """

    permission_classes = [permissions.IsAuthenticated, IsCharityOrActivityLeader]
    pagination_class = pagination.PageNumberPagination
    serializer_class = LeaderFeedbackListSerializer

    def get_queryset(self):
        """
        A method that returns a list of feedback for a leader.

        :return: A list of feedback for a leader.
        """

        # Get the activity id from the URL
        activity_id = self.kwargs['activity_id']

        # Check if the data is in the cache
        cache_feedback = cache.get(f'feedback_{activity_id}')

        # If the cache does not exist, get the feedback from the database
        if cache_feedback is None:
            feedback = Feedback.objects.filter(calendar_event__activity_id=activity_id).order_by('feedback_id')
            cache.set(f'feedback_{activity_id}', feedback, timeout=3600)
        else:
            # If the cache exists, use the cached data
            feedback = cache_feedback
        return feedback


class FeedbackSubmission(APIView):
    """
    FeedbackSubmission class is a subclass of APIView. It allows users to submit feedback for an activity.
    TODO: Remove serializer.data, and add support for feedback questions and answers.

    It contains the following methods:
    - post (POST): A method that allows users to submit feedback for an activity.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, activity_id=None):
        """
        A method that allows users to submit feedback for an activity.

        :param request: The request object.
        :param activity_id: The id of the activity.
        """

        # Get the data from the request
        data = request.data
        data['user'] = request.user.id
        data['activity_id'] = activity_id

        # Validate the feedback text
        validate_feedback_text(data.get('activity_feedback_text'))
        validate_feedback_text(data.get('leader_feedback_text'))

        # Create a serializer with the data
        serializer = FeedbackSubmissionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# TODO: Return question answers lists in specific endpoints.
