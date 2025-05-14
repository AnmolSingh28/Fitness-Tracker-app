# urls.py
from django.urls import path
from .import views 

urlpatterns = [
    path('', views.user_login, name='user_login'), 
    path('register/', views.register, name='register'),
    path('dash_board/', views.dash_board, name='dash_board'),
    path('add_workout/', views.add_workout, name='add_workout'),
    path('logbook/', views.logbook, name='logbook'),
    path('workout/<int:workout_id>/', views.workout_detail, name='workout_detail'),
    path('save-workout/', views.save_workout, name='save_workout'),
]
