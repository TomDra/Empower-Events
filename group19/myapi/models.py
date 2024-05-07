from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import json


class User(AbstractUser):
    disabilities = models.TextField(blank=True, null=True)  # Store JSON as a string
    email = models.EmailField(unique=True)

    def set_disabilities(self, data):
        self.disabilities = json.dumps(data)

    def get_disabilities(self):
        return json.loads(self.disabilities) if self.disabilities else None


class ActivityLeader(models.Model):
    activity_leader_id = models.AutoField(primary_key=True, )
    name = models.CharField(max_length=30)
    birth_date = models.DateTimeField()
    charity = models.ForeignKey('Charity', on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)


class CharityManager(BaseUserManager):
    def create_charity(self, charity_name, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        charity = self.model(charity_name=charity_name, email=email, **extra_fields)
        charity.set_password(password)
        charity.save(using=self._db)
        return charity


class Charity(AbstractBaseUser, PermissionsMixin):
    charity_name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'charity_name'
    REQUIRED_FIELDS = ['email']

    objects = CharityManager()

    # Specify related_name for groups and user_permissions to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="charity_groups_set",
        related_query_name="charity",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="charity_user_permissions_set",
        related_query_name="charity",
    )

    def __str__(self):
        return self.charity_name


class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    calendar_event = models.ForeignKey('Calendar', on_delete=models.CASCADE)
    activity_feedback_text = models.CharField(max_length=500, blank=True, null=True)
    activity_feedback_audio = models.BinaryField(blank=True, null=True)
    activity_feedback_question_answers = models.TextField(blank=True, null=True)  # Store JSON as a string

    leader_feedback_text = models.CharField(max_length=500, blank=True, null=True)
    leader_feedback_audio = models.BinaryField(blank=True, null=True)
    leader_feedback_question_answers = models.TextField(blank=True, null=True)  # Store JSON as a string
    
    feedback_questions = models.TextField(blank=True, null=True)  # New field to store JSON as a string

    def set_feedback_question_answers(self, data):
        self.feedback_question_answers = json.dumps(data)

    def get_feedback_question_answers(self):
        return json.loads(self.feedback_question_answers) if self.feedback_question_answers else None

    def set_feedback_questions(self, data):
        self.feedback_questions = json.dumps(data)

    def get_feedback_questions(self):
        return json.loads(self.feedback_questions) if self.feedback_questions else None


class Calendar(models.Model):
    event_id = models.AutoField(primary_key=True)
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE)
    time = models.DateTimeField()
    activity_leader = models.ForeignKey(ActivityLeader, on_delete=models.CASCADE)

    def get_time(self):
        return self.time


class Activity(models.Model):
    activity_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    age_group = models.ForeignKey('AgeGroup', on_delete=models.CASCADE)
    compatible_disabilities = models.TextField(blank=True, null=True)  # Store JSON as a string
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE)
    photo_file_path = models.CharField(max_length=300, default='defalt.jpg')

    def set_compatible_disabilities(self, data):
        self.compatible_disabilities = json.dumps(data)

    def get_compatible_disabilities(self):
        return json.loads(self.compatible_disabilities) if self.compatible_disabilities else {}




class AgeGroup(models.Model):
    age_group_id = models.AutoField(primary_key=True)
    age_range_lower = models.IntegerField()
    age_range_higher = models.IntegerField()
    group_title = models.CharField(max_length=20)
