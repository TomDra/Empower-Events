from django.urls import path

from . import views

urlpatterns = [
    path('upcoming-list/', views.UpcomingEventsList.as_view(), name='list_events_upcoming'),
    path('previous-list/', views.PreviousEventsList.as_view(), name='list_events_previous'),
]
