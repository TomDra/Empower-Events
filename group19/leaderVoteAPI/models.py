from django.db import models
from myapi.models import ActivityLeader, User
from django.utils import timezone
# Create your models here.

class ActivityLeaderVote(models.Model):
    vote_id = models.AutoField(primary_key=True)
    date_submited = models.DateTimeField(default=timezone.now)
    activity_leader = models.ForeignKey(ActivityLeader, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
