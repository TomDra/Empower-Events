from django.shortcuts import render
import os
from collections import Counter
from django.utils import timezone
from rest_framework import permissions, generics, pagination, status, renderers
from .serializers import ActivityLeaderVoteSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsCharity
from myapi.models import ActivityLeader
from .models import ActivityLeaderVote
from django.db.models import Count

from EventsAPI.serializers import ActivityLeaderSerializer
from myapi.models import Charity


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
        charity = Charity.objects.get(charity_name=request.user.charity_name)

        # Get the first and last moments of the month
        start_date = timezone.datetime(year, month, 1, 0, 0, 0)
        end_date = timezone.datetime(year, month, 1, 0, 0, 0) + timezone.timedelta(days=32)

        # Filter ActivityLeaderVotes for the specified year and month
        activity_leader_votes = ActivityLeaderVote.objects.filter(
            date_submited__gte=start_date,
            date_submited__lt=end_date,
            activity_leader__charity=charity
        )
        leader_counter = Counter(vote.activity_leader.name for vote in activity_leader_votes)

        # Serialize the queryset
        #serializer = ActivityLeaderVoteSerializer(activity_leader_votes, many=True)  # Assuming you have a serializer

        # Return the serialized data
        return Response(leader_counter)


class leadersList(APIView):
    """
    AddEvent class is a subclass of APIView. It is used to add an event.

    It contains the following methods:
    - get (get): A method to get the list of all activity leaders and their user id's for the subsequent post request.
    - post (post): A method to add an event.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        A method to get the list of all activity leaders and their user id's for the subsequent post request.

        :param request: The request object.

        :return: A response containing the list of all activity leaders and their user id's.
        """
        activity_leaders = ActivityLeader.objects.filter()
        serializer = ActivityLeaderSerializer(activity_leaders, many=True)
        return Response(serializer.data)