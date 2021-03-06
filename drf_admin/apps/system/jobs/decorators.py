# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji
@software : PyCharm
@file     : decorators.py
@create   : 2021/2/28 18:12
"""
import logging
import time
import traceback
from functools import wraps

from drf_admin.common.redis import acquire_lock, release_lock

logger = logging.getLogger('info')


# 单节点任务装饰器，被装饰的任务在分布式多节点下同一时间只能运行一次
def single_task(task: str):
    def wrap(func):
        @wraps(func)
        def inner(*args, **kwargs):
            lock = f'single_task:lock:{task}'
            uid = acquire_lock(lock)
            if uid:
                logger.info(f'Successfully obtained redis distributed lock: Task [{task}] : task started')
                try:
                    func(*args, **kwargs)
                    time.sleep(0.5)
                except Exception as e:
                    logger.error(f'Task [{task}] : execution failed :\n {traceback.format_exc()}')
                    raise e
                finally:
                    release_lock(task, uid)
                    logger.info(f'Successfully release redis distributed lock: Task [{task}] : task end')

            else:
                logger.info(f'Failed acquire redis distributed lock: Task [{task}] : task is already running')
                return

        return inner

    return wrap
