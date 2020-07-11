""" 
@author: Wang Meng
@github: https://github.com/tianpangji 
@software: PyCharm 
@file: urls.py 
@create: 2020/6/21 22:28
"""
from django.urls import path
from rest_framework_jwt.views import refresh_jwt_token

from drf_admin.apps.oauth.views import oauth

urlpatterns = [
    path(r'login/', oauth.UserLoginView.as_view()),
    path(r'logout/', oauth.LogoutAPIView.as_view()),
    path(r'refresh/', refresh_jwt_token),
    path(r'info/', oauth.UserInfoView.as_view()),
]
