# -*- coding: utf-8 -*-
"""
@author: Wang Meng
@github: https://github.com/tianpangji
@software: PyCharm 
@file: oauth.py 
@create: 2020/6/24 20:48 
"""
import json
from django.core.cache import cache  # 引入 Django 的 cache 來處理 Redis 操作，這是新添加的代碼
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebToken
import redis  # 引入 redis 客户端库


class UserLoginView(ObtainJSONWebToken):
    """
    post:
    用户登录

    用户登录, status: 200(成功), return: Token信息
    """
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        # 重写父类方法, 定义响应字段内容
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            conn = get_redis_connection('user_info')
            conn.incr('visits')
            return response
        else:
            if response.data.get('non_field_errors'):
                # 日后将增加用户多次登录错误,账户锁定功能(待完善)
                if isinstance(response.data.get('non_field_errors'), list) and len(
                        response.data.get('non_field_errors')) > 0:
                    if response.data.get('non_field_errors')[0].strip() == '无法使用提供的认证信息登录。':
                        return Response(data={'detail': '用户名或密码错误'}, status=status.HTTP_400_BAD_REQUEST)
            raise ValidationError(response.data)


class UserInfoView(APIView):
    """
    get:
    当前用户信息

    当前用户信息, status: 200(成功), return: 用户信息和权限
    """

    def get(self, request):
        user_info = request.user.get_user_info()

        # 如果是超級用戶且權限列表中不包含'admin'，則添加'admin'權限
        if request.user.is_superuser and 'admin' not in user_info['permissions']:
            user_info['permissions'].append('admin')

        # 將權限列表轉換為 JSON 字符串，以便存儲
        user_info['permissions'] = json.dumps(user_info['permissions'])

        # 確保頭像 URL 是完整的，如果 avatar 為 None，則使用空字符串
        user_info['avatar'] = request._current_scheme_host + user_info.get('avatar', '')

        # 使用 redis-py 直接操作 Redis
        # 建立 Redis 連接（根據您的 Redis 配置進行調整）
        redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
        cache_key = 'user_info_%s' % request.user.id

        # 將 user_info 字典存儲到 Redis，並設置過期時間為 1 天
        for key, value in user_info.items():
            if value is not None:  # 確保只有非 None 值被寫入 Redis
                redis_conn.hset(cache_key, key, value)
        redis_conn.expire(cache_key, 60 * 60 * 24)

        # 將權限列表從 JSON 字符串轉換回列表
        user_info['permissions'] = json.loads(user_info['permissions'])

        # 返回用戶信息
        return Response(user_info, status=status.HTTP_200_OK)



class LogoutAPIView(APIView):
    """
    post:
    退出登录

    退出登录, status: 200(成功), return: None
    """

    def post(self, request):
        content = {}
        # 后续将增加redis token黑名单功能
        return Response(data=content)
