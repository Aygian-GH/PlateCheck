from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),

    # Authentication
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Features
    path('upload/', views.image_upload_view, name='image_upload'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('chatbot/', views.chatbot_view, name='chatbot'),
]