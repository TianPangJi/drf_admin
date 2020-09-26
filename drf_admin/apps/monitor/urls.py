# -*- coding: utf-8 -*-

""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : urls.py
@create   : 2020/9/9 20:07
"""
from django.urls import path

from monitor.views import users, service

urlpatterns = [
    path('users/', users.OnlineUsersListAPIView.as_view()),
    path('service/', service.ServiceMonitorAPIView.as_view()),
]
