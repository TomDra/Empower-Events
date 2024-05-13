"""
Serializers for the FeedbackAPI.
"""
from rest_framework import serializers

from myapi.models import Activity, Feedback


class FeedbackOverviewSerializer(serializers.Serializer):
    """
    FeedbackOverviewSerializer is a serializer class that is used to serialize the overall feedback data.

    It contains the following fields:
    - average_user_sentiment (FloatField): The average sentiment of the user feedback.
    - average_leader_sentiment (FloatField): The average sentiment of the leader feedback.
    - average_user_subjectivity (FloatField): The average subjectivity of the user feedback.
    - average_leader_subjectivity (FloatField): The average subjectivity of the leader feedback.
    - possible_improvements (ListField): A list of possible improvements based on the feedback.
    - possible_accomplishments (ListField): A list of possible accomplishments based on the feedback.
    - user_adjectives (ListField): A list of adjectives used in the user feedback.
    - leader_adjectives (ListField): A list of adjectives used in the leader feedback.
    - user_word_freq (JSONField): A dictionary containing the frequency of words in the user feedback.
    - leader_word_freq (JSONField): A dictionary containing the frequency of words in the leader feedback.
    - user_phrase_freq (JSONField): A dictionary containing the frequency of phrases in the user feedback.
    - leader_phrase_freq (JSONField): A dictionary containing the frequency of phrases in the leader feedback.
    """

    average_user_sentiment = serializers.FloatField()
    average_leader_sentiment = serializers.FloatField()
    average_user_subjectivity = serializers.FloatField()
    average_leader_subjectivity = serializers.FloatField()
    possible_improvements = serializers.ListField(child=serializers.CharField())
    possible_accomplishments = serializers.ListField(child=serializers.CharField())
    user_adjectives = serializers.ListField(child=serializers.CharField())
    leader_adjectives = serializers.ListField(child=serializers.CharField())
    user_word_freq = serializers.JSONField()
    leader_word_freq = serializers.JSONField()
    user_phrase_freq = serializers.JSONField()
    leader_phrase_freq = serializers.JSONField()


class ActivityFeedbackListSerializer(serializers.ModelSerializer):
    """
    ActivityFeedbackListSerializer is a serializer class that is used to serialize a list of feedback about an activity.

    It contains the following fields:
    - activity_feedback_text (CharField): The text feedback about the activity.
    - activity_feedback_audio (BinaryField): The audio feedback about the activity.
    """

    class Meta:
        model = Feedback
        fields = ['activity_feedback_text', 'activity_feedback_audio', 'activity_feedback_question_answers']


class LeaderFeedbackListSerializer(serializers.ModelSerializer):
    """
    LeaderFeedbackListSerializer is a serializer class that is used to serialize a list of feedback about a leader.

    It contains the following fields:
    - leader_feedback_text (CharField): The text feedback about the leader.
    - leader_feedback_audio (BinaryField): The audio feedback about the leader.
    """

    class Meta:
        model = Feedback
        fields = ['leader_feedback_text']


class FeedbackSubmissionSerializer(serializers.ModelSerializer):
    """
    FeedbackSubmissionSerializer is a serializer class that is used to serialize feedback submission data.

    It contains the following fields:
    - feedback_id (AutoField): The ID of the feedback. This field is read-only.
    - user (ForeignKey): The user submitting the feedback.
    - calendar_event (ForeignKey): The calendar event associated with the feedback.
    - activity_feedback_text (CharField): The text feedback about the activity.
    - activity_feedback_audio (FileField): The audio feedback about the activity.
    - leader_feedback_text (CharField): The text feedback about the leader.
    - leader_feedback_audio (BinaryField): The audio feedback about the leader.
    """

    class Meta:
        model = Feedback
        fields = ['feedback_id', 'user', 'calendar_event', 'activity_feedback_text', 'activity_feedback_audio',
                  'leader_feedback_text', 'activity_feedback_question_answers']
        read_only_fields = ['feedback_id']


class FeedbackQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['feedback_questions']
