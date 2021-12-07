from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/create', views.createRoom, name='create-room'),
    path('room/update/<str:id>', views.updateRoom, name='update-room'),
    path('room/delete/<str:id>', views.deleteRoom, name='delete-room'),
    path('room/<str:id>', views.room, name='room'),
    path('auth/login', views.registerOrLoginView, name='login'),
    path('auth/logout', views.logoutUser, name='logout'),
    path('auth/register', views.registerOrLoginView, name='register')
]
