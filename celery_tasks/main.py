# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : main.py
@create   : 2020/8/10 19:20
@docs     : https://docs.celeryproject.org/en/stable/
            https://github.com/celery/celery
"""

import os

from celery import Celery

# 为celery程序设置Django配置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf_admin.settings.dev')

# 创建celery应用
app = Celery('admin')

# 导入celery配置
app.config_from_object('celery_tasks.config')

# 加载celery任务模块
app.autodiscover_tasks(['celery_tasks.sms', ])

# 启动Celery命令, (修改celery任务后必须重启celery)
# celery -A celery_tasks.main  worker --loglevel=info

# win系统(celery4.0版本后不支持win, 需安装eventlet模块启动celery)
# celery -A celery_tasks.main  worker --loglevel=info -P eventlet
