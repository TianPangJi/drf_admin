# -*- coding: utf-8 -*-
""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : jobs.py
@create   : 2020/11/25 20:56
"""
from inspect import isfunction, getmembers

from apscheduler.jobstores.base import JobLookupError
from django_apscheduler.models import DjangoJobExecution
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, ListCreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import mixins

from system.jobs import tasks
from system.jobs.run import scheduler
from system.serializers.jobs import JobsListSerializer, JobCreateSerializer, JobFunctionsSerializer, \
    JobUpdateSerializer, JobExecutionsSerializer


class JobFunctionsListAPIView(ListAPIView):
    """
    get:
    任务调度--任务调度函数列表

    获取任务调度函数列表, status: 200(成功), return: 任务调度函数列表
    """
    serializer_class = JobFunctionsSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name', 'desc')

    def get_queryset(self):
        return list(filter(None, [obj if isfunction(obj[1]) else None for obj in getmembers(tasks)]))

    def filter_queryset(self, queryset):
        search_params = self.request.query_params.get('search')
        if search_params:
            obj_list = list()
            for obj in queryset:
                doc = '' if obj[1].__doc__ is None else obj[1].__doc__
                if search_params in obj[0] or search_params in doc:
                    obj_list.append(obj)
            return obj_list
        else:
            return queryset


class JobsListCreateAPIView(ListCreateAPIView):
    """
    get:
    任务调度--任务列表

    获取任务调度任务列表, status: 200(成功), return: 任务列表

    post:
    任务调度--新增

    新增任务, status: 201(成功), return: 新增任务信息

    delete:
    任务调度--清空任务

    清空任务, status: 204(成功), return: None
    """
    filter_backends = (SearchFilter,)
    search_fields = ('name', 'desc')

    def filter_queryset(self, queryset):
        search_params = self.request.query_params.get('search')
        if search_params:
            obj_list = list()
            for obj in queryset:
                doc = tasks.__dict__.get(obj.name).__doc__
                if search_params in obj.name or search_params in doc:
                    obj_list.append(obj)
            return obj_list
        else:
            return queryset

    def get_queryset(self):
        return scheduler.get_jobs()

    def get_serializer_class(self):
        if self.request.method.lower() == 'get':
            return JobsListSerializer
        else:
            return JobCreateSerializer

    @swagger_auto_schema(operation_id='system_jobs_deletes')
    def delete(self, request, *args, **kwargs):
        scheduler.remove_all_jobs()
        return Response(status=status.HTTP_204_NO_CONTENT)


class JobUpdateDestroyAPIView(mixins.UpdateModelMixin, DestroyAPIView):
    """
    patch:
    任务调度--任务启动/停止

    任务启动/停止, status: 200(成功), return: 任务列表

    delete:
    任务调度--删除

    删除, status: 204(成功), return: None
    """
    serializer_class = JobUpdateSerializer

    def get_queryset(self):
        return scheduler.get_jobs()

    def get_job_id(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        return self.kwargs[lookup_url_kwarg]

    def patch(self, request, *args, **kwargs):
        job = scheduler.get_job(self.get_job_id())
        if not job:
            return Response(data={'detail': '调度任务不存在'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(job, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        try:
            scheduler.remove_job(self.get_job_id())
        except JobLookupError:
            return Response(data={'detail': '调度任务不存在'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class JobExecutionsListAPIView(ListAPIView):
    """
    get:
    任务调度--任务执行历史记录

    获取任务执行历史记录, status: 200(成功), return: 任务执行历史记录
    """
    serializer_class = JobExecutionsSerializer
    queryset = DjangoJobExecution.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ['job__id']
