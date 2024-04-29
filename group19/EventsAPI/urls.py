from django.urls import path

from . import views

urlpatterns = [
    path('upcoming-list/', views.UpcomingEventsList.as_view(), name='list_events_upcoming'),
    path('past-list/', views.PastEventsList.as_view(), name='list_events_past'),
    path('add-event', views.AddEvent.as_view(), name='add_event'),
]
