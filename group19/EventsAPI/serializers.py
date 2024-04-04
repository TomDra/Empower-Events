# Importing necessary libraries/modules from Django and rest_framework.
from rest_framework import serializers
from myapi.models import Calendar, Activity, ActivityLeader


# TODO: Adjust the serializers to return more information about the models.
class ActivitySerializer(serializers.ModelSerializer):
    """
    ActivitySerializer class is a subclass of ModelSerializer that serializes the Activity model.
    It contains all fields from the expected Activity model.
    """

    class Meta:
        model = Activity
        fields = '__all__'


class ActivityLeaderSerializer(serializers.ModelSerializer):
    """
    ActivityLeaderSerializer class is a subclass of ModelSerializer that serializes the ActivityLeader model.
    It contains all fields from the expected ActivityLeader model.
    """

    class Meta:
        model = ActivityLeader
        fields = '__all__'


class CalendarSerializer(serializers.ModelSerializer):
    """
    CalendarSerializer class is a subclass of ModelSerializer that serializes the Calendar model.
    It contains all fields from the expected Calendar model.
    """

    # Serializing the activity and activity_leader fields.
    activity = ActivitySerializer()
    activity_leader = ActivityLeaderSerializer()

    class Meta:
        model = Calendar
        fields = '__all__'
