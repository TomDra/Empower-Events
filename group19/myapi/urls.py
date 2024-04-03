from django.urls import path
from . import views

urlpatterns = [
    path('hello-world/', views.hello_world, name='hello_world'),
	path('api/events/<int:event_id>/', views.event_detail, name='event-detail'),
]
