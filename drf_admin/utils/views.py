""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : views.py 
@create   : 2020/7/1 22:37 
"""
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, serializers
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from drf_admin.utils.swagger_schema import OperationIDAutoSchema


class MultipleDestroyMixin:
    """
    自定义批量删除mixin
    """
    swagger_schema = OperationIDAutoSchema

    class MultipleDeleteSerializer(serializers.Serializer):
        ids = serializers.ListField(required=True, write_only=True)

    @swagger_auto_schema(request_body=MultipleDeleteSerializer)
    def multiple_delete(self, request, *args, **kwargs):
        delete_ids = request.data.get('ids')
        if not delete_ids:
            return Response(data={'detail': '参数错误,ids为必传参数'}, status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(delete_ids, list):
            return Response(data={'detail': 'ids格式错误,必须为List'}, status=status.HTTP_400_BAD_REQUEST)
        queryset = self.get_queryset()
        del_queryset = queryset.filter(id__in=delete_ids)
        if len(delete_ids) != del_queryset.count():
            return Response(data={'detail': '删除数据不存在'}, status=status.HTTP_400_BAD_REQUEST)
        del_queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminViewSet(ModelViewSet, MultipleDestroyMixin):
    """
    继承ModelViewSet, 并新增MultipleDestroyMixin
    添加multiple_delete action
    """
    pass


class TreeSerializer(serializers.ModelSerializer):
    """
    TreeAPIView使用的基类序列化器
    """
    id = serializers.IntegerField()
    label = serializers.CharField(max_length=20, source='name')
    pid = serializers.PrimaryKeyRelatedField(read_only=True)


class TreeAPIView(ListAPIView):
    """
    定义Element Tree树结构
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        tree_dict = {}
        tree_data = []
        try:
            for item in serializer.data:
                tree_dict[item['id']] = item
            for i in tree_dict:
                if tree_dict[i]['pid']:
                    pid = tree_dict[i]['pid']
                    parent = tree_dict[pid]
                    parent.setdefault('children', []).append(tree_dict[i])
                else:
                    tree_data.append(tree_dict[i])
            results = tree_data
        except KeyError:
            results = serializer.data
        if page is not None:
            return self.get_paginated_response(results)
        return Response(results)


class ChoiceAPIView(APIView):
    """
    model choice字段API, 需指定choice属性或覆盖get_choice方法
    """
    choice = None

    def get(self, request):
        methods = [{'value': value[0], 'label': value[1]} for value in self.get_choice()]
        return Response(data={'results': methods})

    def get_choice(self):
        assert self.choice is not None, (
                "'%s' 应该包含一个`choice`属性,或覆盖`get_choice()`方法."
                % self.__class__.__name__
        )
        assert isinstance(self.choice, tuple) and len(self.choice) > 0, 'choice数据错误, 应为二维元组'
        for values in self.choice:
            assert isinstance(values, tuple) and len(values) == 2, 'choice数据错误, 应为二维元组'
        return self.choice
