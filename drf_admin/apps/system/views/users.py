""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : users.py 
@create   : 2020/6/27 17:55 
"""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from drf_admin.apps.system.serializers.users import UsersSerializer
from drf_admin.utils.views import MultipleDestroyMixin
from oauth.models import Users


class UsersViewSet(ModelViewSet, MultipleDestroyMixin):
    """
    create:
    用户--增加

    update:
    用户--修改

    list:
    用户--获取列表

    destroy:
    用户--删除

    multiple_delete:
    用户--批量删除
    """
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('is_active',)
    search_fields = ('username', 'name', 'mobile', 'email')
    ordering_fields = ('id',)
