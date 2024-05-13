from django.urls import path
from . import views

urlpatterns = [
    path('vote/', views.vote, name='leader_vote'),
    path('results/<int:year>/<int:month>', views.results, name='leader_vote'),

]
