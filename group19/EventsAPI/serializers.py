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


class ActivityLeaderSerializer(serializers.ModelSerializer):
    """
    ActivityLeaderSerializer class is a subclass of ModelSerializer that serializes the ActivityLeader model.

    It contains the following fields:
    - name: A CharField that represents the name of the activity leader.
    - charity: The CharitySerializer that represents the charity of the activity leader.
    - email: An EmailField that represents the email of the activity leader.
    """

    charity = CharitySerializer(read_only=True)

    class Meta:
        model = ActivityLeader
        fields = ['activity_leader_id', 'name', 'charity', 'email']


class AgeGroupSerializerAddEvent(serializers.ModelSerializer):
    """
    AgeGroupSerializerAddEvent class is a subclass of ModelSerializer that serializes the AgeGroup model.

    It contains the following fields:
    - age_range_lower: An IntegerField that represents the lower bound of the age range.
    - age_range_higher: An IntegerField that represents the upper bound of the age range.
    - group_title: A CharField that represents the title of the age group.

    It contains the following methods:
    - create: A method that creates an age group.
    """

    class Meta:
        model = AgeGroup
        fields = ['age_range_lower', 'age_range_higher', 'group_title']

    def create(self, validated_data):
        """
        A method that creates an age group.

        :param validated_data: The validated data.

        :return: The created age group.
        """

        # Create the age group
        age_group = AgeGroup.objects.create(age_range_lower=validated_data['age_range_lower'],
                                            age_range_higher=validated_data['age_range_higher'],
                                            group_title=validated_data['group_title'])
        return age_group


class ActivitySerializerAddEvent(serializers.ModelSerializer):
    """
    ActivitySerializerAddEvent class is a subclass of ModelSerializer that serializes the Activity model.

    It contains the following fields:
    - description: A CharField that represents the description of the activity.
    - latitude: A DecimalField that represents the latitude of the location of the activity.
    - longitude: A DecimalField that represents the longitude of the location of the activity.
    - age_group: The AgeGroupSerializerAddEvent that represents the age group of the activity.
    - compatible_disabilities: A ListField that represents the compatible disabilities of the activity.

    It contains the following methods:
    - create: A method that creates an activity.
    """

    age_group = AgeGroupSerializerAddEvent()
    compatible_disabilities = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Activity
        fields = ['title', 'description', 'latitude', 'longitude', 'age_group', 'compatible_disabilities', 'photo_file_path']

    def create(self, validated_data):
        """
        A method that creates an activity.

        :param validated_data: The validated data.

        :return: The created activity.
        """

        # Create the age group using the age group serializer
        age_group_data = validated_data.pop('age_group')
        age_group_serializer = AgeGroupSerializerAddEvent(data=age_group_data)

        # Validate the age group serializer
        if age_group_serializer.is_valid():
            age_group = age_group_serializer.save()
        else:
            raise serializers.ValidationError(age_group_serializer.errors)

        # Create the activity
        title = validated_data.get('title')
        description = validated_data.get('description')
        latitude = validated_data.get('latitude')
        longitude = validated_data.get('longitude')
        compatible_disabilities = json.dumps(validated_data.get('compatible_disabilities'))
        photo_file_path = validated_data.get('photo_file_path')

        activity = Activity.objects.create(
            title = title,
            description=description,
            latitude=latitude,
            longitude=longitude,
            age_group=age_group,
            charity=self.context['request'].user,
            compatible_disabilities=compatible_disabilities,
            photo_file_path = validated_data.get('photo_file_path')
        )
        return activity


class CalendarSerializerAddEvent(serializers.ModelSerializer):
    """
    CalendarSerializerAddEvent class is a subclass of ModelSerializer that serializes the Calendar model.

    It contains the following fields:
    - activity: The ActivitySerializerAddEvent that represents the activity of the calendar event.
    - time: A DateTimeField that represents the time of the calendar event.
    - activity_leader: An IntegerField that represents the ID of the activity leader.

    It contains the following methods:
    - create: A method that creates a calendar event.
    """

    activity = ActivitySerializerAddEvent()
    time = serializers.DateTimeField(validators=[validate_future_date])
    activity_leader_id = serializers.IntegerField()

    class Meta:
        model = Calendar
        fields = ['activity', 'time', 'activity_leader_id']

    def create(self, validated_data):
        """
        A method that creates a calendar event.

        :param validated_data: The validated data.

        :return: The created calendar event.
        """

        # Create the activity using the activity serializer
        activity_data = validated_data.pop('activity')
        activity_serializer = ActivitySerializerAddEvent(data=activity_data, context=self.context)

        # Validate the activity serializer
        if activity_serializer.is_valid():
            activity = activity_serializer.save()
        else:
            raise serializers.ValidationError(activity_serializer.errors)

        # Create the calendar event
        time = validated_data.get('time')
        activity_leader_id = validated_data.get('activity_leader_id')

        # Get the activity leader
        activity_leader = ActivityLeader.objects.get(activity_leader_id=activity_leader_id)

        calendar = Calendar.objects.create(
            activity=activity,
            time=time,
            activity_leader=activity_leader
        )
        return calendar
