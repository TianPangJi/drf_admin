# -*- coding: utf-8 -*-

""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : service.py
@create   : 2020/7/29 20:24
"""
import json
from datetime import datetime

import psutil
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class ResourcesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 建立连接
        if not self.scope['user']:
            await self.close()
        else:
            await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        while True:
            data = await self.get_data()
            await self.send(text_data=json.dumps(data))

    @database_sync_to_async
    def get_data(self):
        # cpu信息
        cpu_percent = psutil.cpu_percent(0.1)
        cpu_count = psutil.cpu_count(False)
        # 内存信息
        mem = psutil.virtual_memory()
        men_total = mem.total
        men_free = mem.free
        men_used = mem.used
        men_percent = mem.percent
        # 系统运行时间
        run_time = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
        days = run_time.days
        hours = round(run_time.seconds / 60, 1)
        # 磁盘信息
        disk = psutil.disk_usage('/')
        disk_total = disk.total
        disk_free = disk.free
        disk_used = disk.used
        disk_percent = disk.percent
        data = {'cpu': {'percent': cpu_percent, 'count': cpu_count},
                'mem': {'total': str(round(men_total / 1024 / 1024 / 1024, 2)) + ' MB',
                        'free': str(round(men_free / 1024 / 1024 / 1024, 2)) + ' MB',
                        'used': str(round(men_used / 1024 / 1024 / 1024, 2)) + ' MB',
                        'percent': str(men_percent) + ' %'
                        },
                'disk': {'total': str(round(disk_total / 1024 / 1024 / 1024, 2)) + ' MB',
                         'free': str(round(disk_free / 1024 / 1024 / 1024, 2)) + ' MB',
                         'used': str(round(disk_used / 1024 / 1024 / 1024, 2)) + ' MB',
                         'percent': str(disk_percent) + ' %'
                         },
                'run_time': {'time': f'{days} Days {hours} Hours'}
                }
        return data
