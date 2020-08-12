"""Defines URL patterns for usres"""
from django.conf.urls import url
#from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from . import views

app_name = 'users'
urlpatterns = [
    # Login page
    url(r'^login/$', LoginView.as_view(template_name='users/login.html'),
        name='login'),

    # Logout page
    url('^logout/$', views.logout_view, name='logout'),
    
    # Registration page
    url('^register/$', views.register, name='register'),
]
