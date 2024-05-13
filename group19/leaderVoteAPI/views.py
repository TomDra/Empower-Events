from django.shortcuts import render
import os

from django.utils import timezone
from rest_framework import permissions, generics, pagination, status, renderers
from .serializers import ActivityLeaderVoteSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsCharity
from myapi.models import ActivityLeader
from .models import ActivityLeaderVote
from django.db.models import Count



class vote(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Get the current user
        user = request.user

        # Check if the user has already voted this month
        current_month = timezone.now().month
        has_voted_this_month = ActivityLeaderVote.objects.filter(
            user=user,
            date_submited__month=current_month
        ).exists()

        if has_voted_this_month:
            # If the user has already voted this month, return an error response
            return Response(
                {"error": "You have already voted this month"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Proceed with the vote submission process
        activity_leader_name = request.data.get("activity_leader_name")
        activity_leader = ActivityLeader.objects.get(name=activity_leader_name)

        vote = ActivityLeaderVote.objects.create(
            activity_leader=activity_leader,
            user=user
        )

        return Response({"message": "Vote submitted successfully"})



class results(APIView):
    permission_classes = [permissions.IsAuthenticated, IsCharity]

    def get(self, request, year, month):
        # Convert year and month to integers
        year = int(year)
        month = int(month)

        # Get the first and last moments of the month
        start_date = timezone.datetime(year, month, 1, 0, 0, 0, tzinfo=timezone.utc)
        end_date = timezone.datetime(year, month, 1, 0, 0, 0, tzinfo=timezone.utc) + timezone.timedelta(days=32)

        # Filter ActivityLeaderVotes for the specified year and month
        activity_leader_votes = ActivityLeaderVote.objects.filter(
            date_submitted__gte=start_date,
            date_submitted__lt=end_date
        )

        # Serialize the queryset
        serializer = ActivityLeaderVoteSerializer(activity_leader_votes, many=True)  # Assuming you have a serializer

        # Return the serialized data
        return Response(serializer.data)
