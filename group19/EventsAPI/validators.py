"""
Validators module for the EventsAPI app.

TODO: Add more validators as needed.
"""
from rest_framework import serializers
from django.utils import timezone


def validate_future_date(value):
    """
    Check that the time is not in the past.
    """

    if value < timezone.now():
        raise serializers.ValidationError("Time cannot be set in the past.")
    return value
