""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : views.py 
@create   : 2020/7/1 22:37 
"""
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response


class MultipleDestroyModelMixin:
    """
    自定义批量删除mixin, 与GenericViewSet配合使用
    """

    @action(methods=['delete'], detail=False)
    def multiple_delete(self, request, *args, **kwargs):
        delete_ids = request.data.get('ids')
        if not delete_ids:
            return AttributeError('参数错误,ids为必传参数')
        if not isinstance(delete_ids, list):
            return AttributeError('ids格式错误,必须为List')
        instance = self.get_object()
        for pk in delete_ids:
            get_object_or_404(instance, pk=int(pk)).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
