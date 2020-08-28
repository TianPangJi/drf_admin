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
    path('login/', oauth.UserLoginView.as_view()),
    path('logout/', oauth.LogoutAPIView.as_view()),
    path('refresh/', refresh_jwt_token),
    path('info/', oauth.UserInfoView.as_view()),
]
