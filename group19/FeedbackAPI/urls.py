from django.urls import path

from . import views

urlpatterns = [
    path('<int:activity_id>/overview', views.FeedbackOverview.as_view(), name='feedback_overview'),
    path('<int:activity_id>/activity-feedback-list/', views.ActivityFeedbackList.as_view(),
         name='activity_feedback_list'),
    path('<int:activity_id>/leader-feedback-list/', views.LeaderFeedbackList.as_view(),
         name='leader_feedback_list'),
    path('<int:activity_id>/feedback-submission', views.FeedbackSubmission.as_view(),
         name='feedback_submission'),
    path('<int:activity_id>/feedback-questions-list', views.FeedbackSubmission.as_view(),
         name='feedback_questions'),
]
