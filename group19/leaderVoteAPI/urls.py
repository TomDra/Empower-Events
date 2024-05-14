from django.urls import path
from . import views

urlpatterns = [
    path('vote/', views.vote.as_view(), name='leader_vote'),
    path('results/<int:year>/<int:month>', views.results.as_view(), name='leader_vote'),
    path('leaders/', views.leadersList.as_view(), name='leaders-list'),

]
