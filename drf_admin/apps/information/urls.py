# -*- coding: utf-8 -*-
""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : urls.py
@create   : 2020/11/7 14:05
"""
from django.urls import path

from information.views import centre

urlpatterns = [
    path('change-password/', centre.ChangePasswordAPIView.as_view()),  # 修改个人密码
    path('change-information/', centre.ChangeInformationAPIView.as_view()),  # 修改个人信息
    path('change-avatar/', centre.ChangeAvatarAPIView.as_view()),  # 修改个人头像
]
