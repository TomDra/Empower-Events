from django.urls import path

from . import views

urlpatterns = [
    path('upcoming-events/', views.EventsUpcomingList.as_view(), name='upcoming_events'),
]
