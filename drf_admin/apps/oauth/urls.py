""" 
@author: Wang Meng
@github: https://github.com/tianpangji 
@software: PyCharm 
@file: urls.py 
@create: 2020/6/21 22:28
"""
from django.urls import path
from rest_framework_jwt.views import refresh_jwt_token

from oauth.views import oauth, home

urlpatterns = [
    path('home/', home.HomeAPIView.as_view()),
    path('login/', oauth.UserLoginView.as_view()),
    path('logout/', oauth.LogoutAPIView.as_view()),
    path('refresh/', refresh_jwt_token),
    path('info/', oauth.UserInfoView.as_view()),
]
