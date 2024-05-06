# Importing necessary libraries and modules
import json

from rest_framework import serializers

from myapi.models import Calendar, Activity, Charity, AgeGroup


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
        fields = ['title', 'description', 'latitude', 'longitude', 'compatible_disabilities', 'charity', 'age_group',
                  'activity_id', 'photo_file_path']

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
