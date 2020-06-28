""" 
@author: Wang Meng
@github: https://github.com/tianpangji 
@software: PyCharm 
@file: urls.py 
@create: 2020/6/21 22:28
"""
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from drf_admin.apps.oauth.views.oauth import LogoutAPIView, UserInfoView

urlpatterns = [
    path(r'login/', obtain_jwt_token),
    path(r'logout/', LogoutAPIView.as_view()),
    path(r'refresh/', refresh_jwt_token),
    path(r'info/', UserInfoView.as_view()),
]
