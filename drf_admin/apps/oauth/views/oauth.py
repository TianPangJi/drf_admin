""" 
@author: Wang Meng
@github: https://github.com/tianpangji
@software: PyCharm 
@file: oauth.py 
@create: 2020/6/24 20:48 
"""
from rest_framework.response import Response
from rest_framework.views import APIView


class LogoutAPIView(APIView):
    """
    post:
    退出登录
    """

    def post(self, request):
        content = {'code': 0, 'data': {}, 'msg': '成功'}
        return Response(data=content)
