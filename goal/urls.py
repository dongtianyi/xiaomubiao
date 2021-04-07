from django.urls import path

from . import views

urlpatterns = [
    path('clockin/', views.goal_home_view, name='clockin'),
]
