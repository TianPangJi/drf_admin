# -*- coding: utf-8 -*-
""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : jobs.py
@create   : 2020/11/25 21:39
"""
import uuid
from inspect import getmembers, isfunction

from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.models import DjangoJobExecution
from rest_framework import serializers

from system.jobs import tasks
from system.jobs.run import scheduler


class JobFunctionsSerializer(serializers.Serializer):
    """任务调度函数列表序列化器"""
    name = serializers.SerializerMethodField(help_text='任务函数名称')
    desc = serializers.SerializerMethodField(help_text='任务函数描述')

    def get_name(self, obj):
        return obj[0]

    def get_desc(self, obj):
        return obj[1].__doc__


class JobsListSerializer(serializers.Serializer):
    """任务列表序列化器"""
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    desc = serializers.SerializerMethodField()
    next_run_time = serializers.SerializerMethodField()
    cron = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.id

    def get_name(self, obj):
        return obj.name

    def get_desc(self, obj):
        return tasks.__dict__.get(obj.name).__doc__

    def get_next_run_time(self, obj):
        return obj.next_run_time.strftime('%Y-%m-%d %H:%M:%S') if obj.next_run_time else obj.next_run_time

    def get_cron(self, obj):
        def get_cron(name):
            ob = None
            for field in obj.trigger.fields:
                if field.name == name:
                    ob = field
            return ','.join([str(e) for e in ob.expressions])

        return f'{get_cron("minute")} {get_cron("hour")} {get_cron("day")} {get_cron("month")} {get_cron("day_of_week")}'


class JobCreateSerializer(serializers.Serializer):
    """任务新增序列化器"""

    id = serializers.SerializerMethodField()
    desc = serializers.SerializerMethodField()
    next_run_time = serializers.SerializerMethodField()
    name = serializers.CharField(required=True, error_messages={'required': '函数名称为必传项'})
    cron = serializers.CharField(required=True, write_only=True, error_messages={'required': 'cron表达式为必传项'})

    def get_id(self, obj):
        return obj.id

    def get_desc(self, obj):
        return tasks.__dict__.get(obj.name).__doc__

    def get_next_run_time(self, obj):
        return obj.next_run_time.strftime('%Y-%m-%d %H:%M:%S') if obj.next_run_time else obj.next_run_time

    def validate(self, attrs):
        name = attrs.get('name')
        cron = attrs.get('cron')
        job_function = None
        for obj in getmembers(tasks):
            if isfunction(obj[1]) and obj[0] == name:
                job_function = obj[1]
                attrs['job_function'] = job_function
                break
        if job_function is None:
            raise serializers.ValidationError('调度任务函数不存在')
        try:
            trigger = CronTrigger.from_crontab(cron)
            attrs['trigger'] = trigger
        except ValueError:
            raise serializers.ValidationError('cron表达式格式错误')
        return attrs

    def get_cron(self, obj):
        def get_cron(name):
            ob = None
            for field in obj.trigger.fields:
                if field.name == name:
                    ob = field
            return ','.join([str(e) for e in ob.expressions])

        return f'{get_cron("minute")} {get_cron("hour")} {get_cron("day")} {get_cron("month")} {get_cron("day_of_week")}'

    def create(self, validated_data):
        while 1:
            job_id = str(uuid.uuid1())
            if scheduler.get_job(job_id):
                continue
            else:
                break
        scheduler.add_job(validated_data.get('job_function'),
                          args=[],
                          kwargs=None,
                          trigger=validated_data.get('trigger'),
                          id=job_id,
                          max_instances=1,
                          replace_existing=True,
                          misfire_grace_time=10
                          )
        return scheduler.get_job(job_id)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['cron'] = self.get_cron(instance)
        return ret


class JobUpdateSerializer(serializers.Serializer):
    """调度任务启动/暂停"""
    status = serializers.BooleanField(required=True, write_only=True)

    def validate(self, attrs):
        status = attrs.get('status')
        if status is None:
            raise serializers.ValidationError('status参数为必传项')
        if not isinstance(status, bool):
            raise serializers.ValidationError('status参数类型错误')
        return attrs

    def save(self, **kwargs):
        if self.validated_data.get('status'):
            self.instance.resume()
        else:
            self.instance.pause()
        return self.instance

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['status'] = True if self.validated_data.get('status') else False
        return ret


class JobExecutionsSerializer(serializers.ModelSerializer):
    """任务执行历史记录序列化器"""
    run_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = DjangoJobExecution
        fields = '__all__'
