""" 
@author: Wang Meng
@github: https://github.com/tianpangji
@software: PyCharm 
@file: oauth.py 
@create: 2020/6/24 20:48 
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class UserInfoView(APIView):
    """
    get
    获取当前用户信息和权限
    """

    def get_permission_from_role(self, request):
        try:
            if request.user:
                perms_list = []
                for item in request.user.roles.values('permissions__name').distinct():
                    perms_list.append(item['permissions__name'])
                return perms_list
        except AttributeError:
            return None

    def get(self, request):
        perms = self.get_permission_from_role(request)
        data = {
            'username': request.user.username,
            'avatar': request._request._current_scheme_host + '/media/' + str(request.user.image),
            'email': request.user.email,
            'is_active': request.user.is_active,
            'permissions': perms
        }
        return Response(data, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    """
    post:
    退出登录(后端不做处理, 前端删除Token信息, 后期完善)
    """

    def post(self, request):
        content = {'code': 0, 'data': {}, 'msg': '成功'}
        return Response(data=content)
