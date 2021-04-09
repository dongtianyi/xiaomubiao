from django.urls import path

from . import views

urlpatterns = [
    path('clockin/', views.goal_home_view, name='clockin'),
    path('setup/', views.goal_setup_view, name='goal_setup'),
    path('all_setup/', views.all_setup_veiw, name='all_setup'),
    path('all_clockin/', views.all_clockin_view, name='all_clockin'),
    # 删除打卡
    path('clockin/<pk>/', views.ClockInDeleteView.as_view(), name='delete_clockin'),
]
