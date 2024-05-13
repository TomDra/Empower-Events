"""
Views module for the FeedbackAPI app.
"""
import json
import os

import joblib
from django.conf import settings
from nltk.corpus import stopwords
from rest_framework import status, permissions, pagination, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from textblob import TextBlob
import nltk
from collections import Counter

from .permissions import IsCharityOrActivityLeader, IsCharity
from .serializers import FeedbackOverviewSerializer, ActivityFeedbackListSerializer, LeaderFeedbackListSerializer, \
    FeedbackSubmissionSerializer, FeedbackQuestionsSerializer
from myapi.models import Activity, Feedback, Calendar, User
from textblob.download_corpora import download_all
from .validators import validate_feedback_text
from rest_framework.authentication import SessionAuthentication
from django.shortcuts import get_object_or_404

# Download the stopwords
nltk.download('stopwords')
nltk.download('punkt')
download_all()


class FeedbackOverview(APIView):
    """
    FeedbackOverview class is a subclass of APIView. It conducts sentiment, objectivity, adjective, word and phrase
     analysis.

    It contains the following methods:
    - get: A method that analyses the feedback for a specific activity and returns the aforementioned data.
    """
    permission_classes = [permissions.IsAuthenticated, IsCharity]

    def get(self, request, activity_id):
        """
        A method that analyses the feedback for a specific activity and returns:
        - Average user sentiment
        - Average leader sentiment
        - Average user subjectivity
        - Average leader subjectivity
        - Possible improvements
        - Possible accomplishments
        - Adjectives used in user feedback
        - Adjectives used in leader feedback
        - Most common words in user feedback
        - Most common words in leader feedback
        - Most common phrases in user feedback
        - Most common phrases in leader feedback

        :param request: The request object.
        :param activity_id: The id of the activity.
        """

        # Get the feedback for the activity
        feedback = Feedback.objects.filter(calendar_event=activity_id)

        # Check if feedback is not None
        if feedback is not None:
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
            average_leader_sentiment = sum(leader_sentiments) / len(
                leader_sentiments) if leader_sentiments else None
            average_user_subjectivity = sum(user_subjectivities) / len(
                user_subjectivities) if user_subjectivities else None
            average_leader_subjectivity = sum(leader_subjectivities) / len(
                leader_subjectivities) if leader_subjectivities else None

            # Analyse adjectives used in feedback, (JJ, JJR, JJS are adjective tags)
            user_adjectives = [word for f in feedback if f.activity_feedback_text for word, tag in
                               nltk.pos_tag(nltk.word_tokenize(f.activity_feedback_text)) if
                               tag in ['JJ', 'JJR', 'JJS']]
            leader_adjectives = [word for f in feedback if f.leader_feedback_text for word, tag in
                                 nltk.pos_tag(nltk.word_tokenize(f.leader_feedback_text)) if
                                 tag in ['JJ', 'JJR', 'JJS']]

            # Define stop words
            stop_words = set(stopwords.words('english'))

            stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}'])

            # Calculate word and phrase frequency. Removing stop words.
            n = 10  # Limit the number of words/phrases to 10
            user_word_freq = Counter(word for f in feedback if f.activity_feedback_text
                                     for word in nltk.word_tokenize(f.activity_feedback_text) if
                                     word not in stop_words).most_common(n)
            leader_word_freq = Counter(word for f in feedback if f.leader_feedback_text
                                       for word in nltk.word_tokenize(f.leader_feedback_text) if
                                       word not in stop_words).most_common(n)
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
                'user_word_freq': user_word_freq,
                'leader_word_freq': leader_word_freq,
                'user_phrase_freq': user_phrase_freq,
                'leader_phrase_freq': leader_phrase_freq
            }

            serializer = FeedbackOverviewSerializer(data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response({"detail": "Feedback not found."}, status=status.HTTP_400_BAD_REQUEST)


class ActivityFeedbackList(generics.ListAPIView):
    """
    ActivityFeedbackList class is a subclass of ListAPIView. It allows users to view a list of feedback for an activity.
    It implements pagination to limit the number of feedback items returned per page.

    It contains the following methods:
    - get_queryset (GET): A method that returns a list of feedback for an activity.
    """

    permission_classes = [permissions.IsAuthenticated, IsCharity]#OrActivityLeader]
    pagination_class = pagination.PageNumberPagination
    serializer_class = ActivityFeedbackListSerializer

    def get_queryset(self):
        """
        A method that returns a list of feedback for an activity.

        :return: A list of feedback for an activity.
        """

        # Get the activity id from the URL
        activity_id = self.kwargs['activity_id']

        # Grab feedback from the database
        feedback = Feedback.objects.filter(calendar_event=activity_id).order_by('feedback_id')
        # Return the feedback
        return feedback


class LeaderFeedbackList(generics.ListAPIView):
    """
    LeaderFeedbackList class is a subclass of ListAPIView. It allows users to view a list of feedback for a leader.
    It implements pagination to limit the number of feedback items returned per page.

    It contains the following methods:
    - get_queryset (GET): A method that returns a list of feedback for a leader.
    """

    permission_classes = [permissions.IsAuthenticated, IsCharity]
    pagination_class = pagination.PageNumberPagination
    serializer_class = LeaderFeedbackListSerializer

    def get_queryset(self):
        """
        A method that returns a list of feedback for a leader.

        :return: A list of feedback for a leader.
        """

        # Get the activity id from the URL
        activity_id = self.kwargs['activity_id']

        # Grab feedback from the database
        feedback = Feedback.objects.filter(calendar_event=activity_id).order_by('feedback_id')

        # Return the feedback
        return feedback


class FeedbackSubmission(APIView):
    """
    FeedbackSubmission class is a subclass of APIView. It allows users to submit feedback for an activity.

    It contains the following methods:
    - post (POST): A method that allows users to submit feedback for an activity.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, event_id):
        """
        A method that allows users to submit feedback for an activity.

        :param request: The request object.
        :param activity_id: The id of the activity.
        """

        # Get the data from the request
        data = request.data
        serializer_data = {}
        serializer_data['user'] = get_object_or_404(User, pk=request.user.id).id
        serializer_data['calendar_event'] = get_object_or_404(Calendar, pk=event_id).event_id
        serializer_data['activity_feedback_text'] = data.get('activityFeedback')
        serializer_data['leader_feedback_text'] = data.get('leaderFeedback')
        serializer_data['activity_feedback_question_answers'] = data.get('questionAnswers')
        # Validate the feedback text
        validate_feedback_text(data.get('activityFeedback'))
        validate_feedback_text(data.get('leaderFeedback'))

        audio_file = request.FILES.get('audio')
        if audio_file:
            serializer_data['activity_feedback_audio'] = audio_file

        # Create a serializer with the data
        serializer = FeedbackSubmissionSerializer(data=serializer_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeedbackQuestions(APIView):
    """
    FeedbackQuestions class is a subclass of APIView. It allows users to view feedback questions for an activity.

    It contains the following methods:
    - get (GET): A method that returns feedback questions for an activity.
    """

    # Permission classes and serializer class
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FeedbackQuestionsSerializer

    def get(self, request, event_id):
        """
        A method that returns feedback questions for an activity.

        :param request: The request object.
        :param activity_id: The id of the activity.

        :return: A list of feedback questions for an activity.
        """

        # Get the activity id from the URL
        event_id = self.kwargs['event_id']

        # Get the feedback questions from the database
        activity = Calendar.objects.get(event_id=event_id).activity

        if activity is None:
            return Response({"detail": "Feedback not found."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        questions = json.loads(activity.feedback_questions)

        # Return the feedback questions
        return Response(questions, status=status.HTTP_200_OK)


class FeedbackQuestionDetails(generics.ListAPIView):
    """
    ActivityFeedbackList class is a subclass of ListAPIView. It allows users to view a list of feedback for an activity.
    It implements pagination to limit the number of feedback items returned per page.

    It contains the following methods:
    - get_queryset (GET): A method that returns a list of feedback for an activity.
    """

    permission_classes = [permissions.IsAuthenticated, IsCharity]

    def get(self, request, event_id):
        """
        A method that returns feedback questions for an activity.

        :param request: The request object.
        :param activity_id: The id of the activity.

        :return: A list of feedback questions for an activity.
        """
        try:
            # Get the activity id from the URL
            event_id = self.kwargs['event_id']

            # Get the feedback questions from the database
            feedbacks = Feedback.objects.filter(calendar_event=event_id)
            activity = Calendar.objects.get(event_id=event_id).activity

            if feedbacks is None:
                return Response({"detail": "No feedback found."}, status=status.HTTP_204_NO_CONTENT)

            question_counts = {}
            questions = json.loads(activity.feedback_questions)

            for feedback in feedbacks:
                if feedback.activity_feedback_question_answers:
                    answers = json.loads(feedback.activity_feedback_question_answers)
                    for question_id, answer in answers.items():
                        question_text = questions[int(question_id)]['question']
                        if answer == 'positive':
                            if question_text in question_counts:
                                question_counts[question_text]['positive'] = question_counts[question_text]['positive'] + 1
                            else:
                                question_counts[question_text] = {'positive': 1, 'negative': 0}
                        else:
                            if question_text in question_counts:
                                question_counts[question_text]['negative'] = question_counts[question_text]['negative'] + 1
                            else:
                                question_counts[question_text] = {'positive': 0, 'negative': 1}


            # Calculate the total counts of positive and negative answers
            for question, counts in question_counts.items():
                positive_total = counts["positive"]
                negative_total = counts["negative"]

                question_counts[question]["midpoint"] = positive_total - negative_total

            question_detail = {'questions': question_counts}

            if question_counts == {}:
                return Response({'questions': question_counts, "detail": "No feedback found."}, status=status.HTTP_204_NO_CONTENT)



            # Return the feedback questions
            return Response(question_detail, status=status.HTTP_200_OK)

        except Calendar.DoesNotExist:
            return Response({"detail": "Activity not found."}, status=status.HTTP_404_NOT_FOUND)