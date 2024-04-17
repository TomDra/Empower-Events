from django.urls import path

from . import views

urlpatterns = [
    path('feedback/<int:activity_id>/overiew', views.FeedbackOverview.as_view(), name='feedback_overview'),
]
