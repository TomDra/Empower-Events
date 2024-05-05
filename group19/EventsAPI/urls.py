from django.urls import path

from . import views

urlpatterns = [
    # Get events
    path('upcoming-list/', views.UpcomingEventsList.as_view(), name='list_events_upcoming'),
    path('past-list/', views.PastEventsList.as_view(), name='list_events_past'),
    path('previous-list/', views.PreviousEventsList.as_view(), name='list_events_previous'),
    # get event details
    path('activity-details/<int:activity_id>/', views.activity_detail, name='event-detail'),
    path('detail/<int:event_id>/', views.calander_details),
    # add events
    path('add-event', views.AddEvent.as_view(), name='add_event'),
]
