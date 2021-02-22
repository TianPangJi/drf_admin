# -*- coding: utf-8 -*-
"""
@author: Wang Meng
@github: https://github.com/tianpangji
@software: PyCharm 
@file: oauth.py 
@create: 2020/6/24 20:48 
"""
import json

from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebToken


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
        # 将用户信息缓存到redis
        conn = get_redis_connection('user_info')
        if request.user.is_superuser and 'admin' not in user_info['permissions']:
            user_info['permissions'].append('admin')
        user_info['permissions'] = json.dumps(user_info['permissions'])
        user_info['avatar'] = request._current_scheme_host + user_info.get('avatar')
        conn.hmset('user_info_%s' % request.user.id, user_info)
        conn.expire('user_info_%s' % request.user.id, 60 * 60 * 24)  # 设置过期时间为1天
        user_info['permissions'] = json.loads(user_info['permissions'])
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
