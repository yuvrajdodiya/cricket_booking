from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),

    
    path('login/', views.user_login_view, name='user_login'),
]