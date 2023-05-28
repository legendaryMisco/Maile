from django.urls import path
from . import views

urlpatterns = [
    path('', views.RobotAuth, name="RobotAuth"),
    path('welcome/', views.home, name="Home"),
    path('login/<str:pk>/', views.loginPage, name="Login")
]
