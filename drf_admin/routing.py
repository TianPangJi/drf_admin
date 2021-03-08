# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : routing.py
@create   : 2020/7/29 20:21
"""
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf_admin.settings.dev')
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path

from drf_admin.utils.websocket import TokenAuthMiddleware
from monitor.consumers import service

django.setup()
application = ProtocolTypeRouter({
    'websocket': TokenAuthMiddleware(
        URLRouter([
            re_path(r'^monitor/service', service.ResourcesConsumer),
        ])
    )
})
