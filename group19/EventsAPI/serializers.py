"""
The serializers module contains the serializers for the models in the myapi app.
"""
import json

from rest_framework import serializers

from myapi.models import Calendar, Activity, Charity, AgeGroup, ActivityLeader
from .validators import validate_future_date


class CharitySerializer(serializers.ModelSerializer):
    """
    CharitySerializer class is a subclass of ModelSerializer that serializes the Charity model.
    It contains the following fields:
    - charity_name: A CharField that represents the name of the charity.
    """

    class Meta:
        model = Charity
        fields = ['charity_name']


class AgeGroupSerializer(serializers.ModelSerializer):
    """
    AgeGroupSerializer class is a subclass of ModelSerializer that serializes the AgeGroup model.
    It contains the following fields:
    - group_title: A CharField that represents the title of the age group.
    """

    class Meta:
        model = AgeGroup
        fields = ['group_title']


class ActivitySerializer(serializers.ModelSerializer):
    """
    ActivitySerializer class is a subclass of ModelSerializer that serializes the Activity model.

    It contains the following fields:
    - description: A CharField that represents the description of the activity.
    - latitude: A DecimalField that represents the latitude of the location of the activity.
    - longitude: A DecimalField that represents the longitude of the location of the activity.
    - compatible_disabilities: A JSONField that represents the compatible disabilities of the activity.
    - charity: The CharitySerializer that represents the charity of the activity.
    - age_group: The AgeGroupSerializer that represents the age group of the activity.
    - activity_id: An AutoField that represents the ID of the activity.
    """
    charity = CharitySerializer(read_only=True)
    age_group = AgeGroupSerializer(read_only=True)

    class Meta:
        model = Activity
        fields = ['description', 'latitude', 'longitude', 'compatible_disabilities', 'charity', 'age_group',
                  'activity_id']

    def to_representation(self, instance):
        """
        A method to serialize the representation of the activity in a custom way.

        :param instance: The instance of the activity.
        :return: The serialized representation of the activity.
        """

        # Serialize the instance
        representation = super().to_representation(instance)

        # Update the representation
        representation['charity'] = representation['charity']['charity_name']
        representation['age_group'] = representation['age_group']['group_title']

        # Load the compatible disabilities from JSON
        representation['compatible_disabilities'] = json.loads(representation['compatible_disabilities'])

        # Return the updated representation
        return representation


class CalendarSerializer(serializers.ModelSerializer):
    """
    CalendarSerializer class is a subclass of ModelSerializer that serializes the Calendar model.

    It contains the following fields:
    - activity: The ActivitySerializer that represents the activity of the calendar event.
    - time: A DateTimeField that represents the time of the calendar event.
    - event_id: An AutoField that represents the ID of the calendar event.
    """

    activity = ActivitySerializer()

    class Meta:
        model = Calendar
        fields = ['activity', 'time', 'event_id']

    def to_representation(self, instance):
        """
        A method to serialize the representation of the calendar event in a custom way.

        :param instance: The instance of the calendar event.
        :return: The serialized representation of the calendar event.
        """

        # Serialize the instance
        representation = super().to_representation(instance)

        # Update the representation
        representation['date'] = representation.pop('time')

        # Load and update the activity representation
        activity_representation = representation.pop('activity')
        representation.update(activity_representation)

        # Return the updated representation
        return representation


class EventSerializer(serializers.Serializer):
    """
    EventSerializer class is a subclass of Serializer that serializes the data for creating a new event.

    It contains the following fields:
    - description: A CharField that represents the description of the event.
    - latitude: A DecimalField that represents the latitude of the location of the event.
    - longitude: A DecimalField that represents the longitude of the location of the event.
    - age_range_lower: An IntegerField that represents the lower bound of the age range of the event.
    - age_range_higher: An IntegerField that represents the upper bound of the age range of the event.
    - group_title: A CharField that represents the title of the age group of the event.
    - compatible_disabilities: A JSONField that represents the compatible disabilities of the event.
    - time: A DateTimeField that represents the time of the event.

    It contains the following methods:
    - create: A method that creates a new event.
    """

    # Defining the fields
    description = serializers.CharField(max_length=500)
    latitude = serializers.DecimalField(max_digits=8, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    age_range_lower = serializers.IntegerField()
    age_range_higher = serializers.IntegerField()
    group_title = serializers.CharField(max_length=20)
    compatible_disabilities = serializers.JSONField()
    time = serializers.DateTimeField(validators=[validate_future_date])

    def create(self, validated_data):
        """
        A method that creates a new event.

        :param validated_data: The validated data for creating the new event.

        :return: The new event.
        """

        # Get and validate data for AgeGroup
        age_range_lower = validated_data.pop('age_range_lower')
        age_range_higher = validated_data.pop('age_range_higher')
        group_title = validated_data.pop('group_title')

        # Create and save the new AgeGroup
        age_group = AgeGroup.objects.create(age_range_lower=age_range_lower, age_range_higher=age_range_higher,
                                            group_title=group_title)
        age_group.save()

        # Get the activity leader from the request
        activity_leader = ActivityLeader.objects.get(
            user=self.context['request'].user)

        # Extract and validate data for Calendar
        time = validated_data.pop('time')

        # Create and save the new Activity
        activity = Activity(age_group=age_group, charity=activity_leader.charity)
        activity.set_compatible_disabilities(validated_data.pop('compatible_disabilities'))
        activity.description = validated_data.pop('description')
        activity.latitude = validated_data.pop('latitude')
        activity.longitude = validated_data.pop('longitude')
        activity.save()

        # Create and save the new Calendar event
        event = Calendar.objects.create(activity=activity, time=time, activity_leader=activity_leader)
        event.save()

        return event
