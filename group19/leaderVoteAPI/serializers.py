from rest_framework import serializers
from .models import ActivityLeaderVote

class ActivityLeaderVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLeaderVote
        fields = ['vote_id', 'date_submitted', 'activity_leader', 'user']
