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
from django.conf import settings


class ResourcesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 建立连接
        if not self.scope['user']:
            await self.close()
        else:
            await self.channel_layer.group_add(
                self.scope['user'].username,
                self.channel_name,
            )
            await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        # 接收消息
        data = await self.get_data()
        await self.channel_layer.group_send(
            self.scope['user'].username,
            {
                'type': 'service.message',
                'message': json.dumps(data),
            }
        )

    async def disconnect(self, code):
        # 关闭
        await self.channel_layer.group_discard(
            self.scope['user'].username,
            self.channel_name
        )

    async def service_message(self, event):
        # 发送信息
        await self.send(event['message'])

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
        # 项目不间断运行时间
        date_now = datetime.now()
        run_time = date_now - datetime.fromtimestamp(settings.PROJECT_START_TIME)
        # 系统时间
        now_date, now_time = date_now.strftime('%Y-%m-%d'), datetime.now().strftime('%H:%M:%S')
        days = run_time.days
        hours = round(run_time.seconds / 60 / 60, 1)
        # 磁盘信息
        disk = psutil.disk_usage('/')
        disk_total = disk.total
        disk_free = disk.free
        disk_used = disk.used
        disk_percent = disk.percent
        data = {'cpu': {'percent': float(cpu_percent), 'count': str(cpu_count) + ' Cores'},
                'mem': {'total': str(round(men_total / 1024 / 1024 / 1024, 2)) + ' GB',
                        'free': str(round(men_free / 1024 / 1024 / 1024, 2)) + ' GB',
                        'used': str(round(men_used / 1024 / 1024 / 1024, 2)) + ' GB',
                        'percent': float(men_percent)
                        },
                'disk': {'total': str(round(disk_total / 1024 / 1024 / 1024, 2)) + ' GB',
                         'free': str(round(disk_free / 1024 / 1024 / 1024, 2)) + ' GB',
                         'used': str(round(disk_used / 1024 / 1024 / 1024, 2)) + ' GB',
                         'percent': float(disk_percent)
                         },
                'sys': {'run_time': f'{days} 天 {hours} 小时'},
                'time': {'date': now_date, 'time': now_time}
                }
        return data
