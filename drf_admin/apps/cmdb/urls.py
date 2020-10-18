# -*- coding: utf-8 -*-

""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : urls.py
@create   : 2020/10/18 15:30
"""
from django.urls import path, include

from cmdb.views import servers
from drf_admin.utils import routers

router = routers.AdminRouter()
router.register(r'servers', servers.ServersViewSet, basename="servers")  # 服务器管理
urlpatterns = [
    path('', include(router.urls)),
]
