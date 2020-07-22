""" 
@author: Wang Meng
@github: https://github.com/tianpangji
@software: PyCharm 
@file: oauth.py 
@create: 2020/6/24 20:48 
"""
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebToken


class UserLoginView(ObtainJSONWebToken):
    """
    post:
    用户鉴权获取Token值
    """

    def post(self, request, *args, **kwargs):
        # 重写父类方法, 定义响应字段内容
        response = super().post(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return response
        else:
            if serializer.errors.get('non_field_errors'):
                # 日后将增加用户多次登录错误,账户锁定功能(待完善)
                return Response(data={'detail': '用户名或密码错误'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                raise APIException(serializer.errors)


class UserInfoView(APIView):
    """
    get:
    获取当前用户信息和权限
    """

    @staticmethod
    def get_user_permissions(request):
        permissions = []
        for item in request.user.roles.values('permissions__name').distinct():
            name = item.get('permissions__name')
            if name:
                permissions.append(name)
        return permissions

    def get(self, request):
        permissions = self.get_user_permissions(request)
        data = {
            'username': request.user.username,
            'avatar': request._request._current_scheme_host + '/media/' + str(request.user.image),
            'email': request.user.email,
            'is_active': request.user.is_active,
            'permissions': permissions
        }
        return Response(data, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    """
    post:
    退出登录(后端不做处理, 前端删除Token信息, 后期完善)
    """

    def post(self, request):
        content = {'code': 0, 'data': {}, 'msg': '成功'}
        # 后续将增加redis token黑名单功能
        return Response(data=content)
