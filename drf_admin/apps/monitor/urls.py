# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : urls.py
@create   : 2020/9/9 20:07
"""
from django.urls import path, include

from drf_admin.utils import routers
from monitor.views import users, service, error, ip, crud

router = routers.AdminRouter()
router.register(r'ip', ip.IpBlackListViewSet, basename="ip")  # ip黑名单管理
urlpatterns = [
    path('users/', users.OnlineUsersListAPIView.as_view()),  # 在线用户监控
    path('service/', service.ServiceMonitorAPIView.as_view()),  # 服务监控
    path('error/', error.ErrorLogAPIView.as_view()),  # 错误日志监控
    path('crud/', crud.CRUDListAPIView.as_view()),  # CRUD变更记录
    path('', include(router.urls)),
]
