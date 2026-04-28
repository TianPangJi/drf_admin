# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : urls.py
@create   : 2020/10/18 15:30
"""
from django.urls import path, include

from cmdb.views import servers, assets, network_devices, storage_devices, security_devices
from drf_admin.utils import routers

router = routers.AdminRouter()
router.register(r'servers', servers.ServersViewSet, basename="servers")  # 服务器管理
router.register(r'network-devices', network_devices.NetworkDevicesViewSet, basename="network-devices")  # 网络设备管理
router.register(r'storage-devices', storage_devices.StorageDevicesViewSet, basename="storage-devices")  # 存储设备管理
router.register(r'security-devices', security_devices.SecurityDevicesViewSet, basename="security-devices")  # 安全设备管理
urlpatterns = [
    path('servers/system-type/', servers.ServersSystemTypeAPIView.as_view()),
    path('servers/type/', servers.ServersTypeAPIView.as_view()),
    path('network-devices/type/', network_devices.NetworkDevicesTypeAPIView.as_view()),
    path('storage-devices/type/', storage_devices.StorageDevicesTypeAPIView.as_view()),
    path('security-devices/type/', security_devices.SecurityDevicesTypeAPIView.as_view()),
    path('assets/status/', assets.AssetsStatusAPIView.as_view()),
    path('assets/admin/', assets.AssetsAdminListAPIView.as_view()),
    path('assets/cabinets/', assets.IDCCabinetsTreeAPIView.as_view()),
    path('', include(router.urls)),
]
