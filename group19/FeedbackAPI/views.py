# Importing necessary libraries and modules
from django.core.cache import cache
from nltk.corpus import stopwords
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from textblob import TextBlob
import nltk
from collections import Counter

from .permissions import IsCharityOrActivityLeader
from .serializers import FeedbackOverviewSerializer
from myapi.models import Feedback

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
            feedback = Feedback.objects.filter(calendar_event__activity_id=activity_id)

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

            # Create a dictionary with the analysed data
            data = {
                'average_user_sentiment': average_user_sentiment,
                'average_leader_sentiment': average_leader_sentiment,
                'average_user_subjectivity': average_user_subjectivity,
                'average_leader_subjectivity': average_leader_subjectivity,
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
