# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : urls.py
@create   : 2020/10/18 15:30
"""
from django.urls import path, include

from cmdb.views import servers, assets
from drf_admin.utils import routers

router = routers.AdminRouter()
router.register(r'servers', servers.ServersViewSet, basename="servers")  # 服务器管理
urlpatterns = [
    path('servers/system-type/', servers.ServersSystemTypeAPIView.as_view()),
    path('servers/type/', servers.ServersTypeAPIView.as_view()),
    path('assets/status/', assets.AssetsStatusAPIView.as_view()),
    path('assets/admin/', assets.AssetsAdminListAPIView.as_view()),
    path('assets/cabinets/', assets.IDCCabinetsTreeAPIView.as_view()),
    path('', include(router.urls)),
]
