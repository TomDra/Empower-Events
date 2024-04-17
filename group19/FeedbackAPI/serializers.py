# Importing necessary libraries and modules
from rest_framework import serializers


class FeedbackOverviewSerializer(serializers.Serializer):
    """
    FeedbackOverviewSerializer is a serializer class that is used to serialize the overall feedback data.

    It contains the following fields:
    - average_user_sentiment (FloatField): The average sentiment of the user feedback.
    - average_leader_sentiment (FloatField): The average sentiment of the leader feedback.
    - average_user_subjectivity (FloatField): The average subjectivity of the user feedback.
    - average_leader_subjectivity (FloatField): The average subjectivity of the leader feedback.
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
    user_adjectives = serializers.ListField(child=serializers.CharField())
    leader_adjectives = serializers.ListField(child=serializers.CharField())
    user_word_freq = serializers.JSONField()
    leader_word_freq = serializers.JSONField()
    user_phrase_freq = serializers.JSONField()
    leader_phrase_freq = serializers.JSONField()
