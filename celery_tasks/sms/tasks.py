# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : tasks.py
@create   : 2020/8/10 19:24
"""
from celery_tasks.main import app


@app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code):
    # 发送短信celery任务, 任务调度 send_sms_code.delay(13111111111,0101)
    pass
