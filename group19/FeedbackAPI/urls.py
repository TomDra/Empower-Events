from django.urls import path

from . import views

urlpatterns = [
    path('feedback/<int:activity_id>/overiew', views.FeedbackOverview.as_view(), name='feedback_overview'),
    path('feedback/<int:activity_id>/activity-feedback-list/', views.ActivityFeedbackList.as_view(),
         name='activity_feedback_list'),
    path('feedback/<int:activity_id>/leader-feedback-list/', views.LeaderFeedbackList.as_view(),
         name='leader_feedback_list'),
]
