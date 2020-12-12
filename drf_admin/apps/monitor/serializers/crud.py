# -*- coding: utf-8 -*-
"""
@author   : Wang Meng
@github   : https://github.com/tianpangji
@software : PyCharm
@file     : crud.py
@create   : 2020/12/9 20:44
"""
from django.contrib.contenttypes.models import ContentType
from easyaudit.models import CRUDEvent
from rest_framework import serializers


class CRUDSerializer(serializers.ModelSerializer):
    event_type_display = serializers.SerializerMethodField()
    datetime = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    username = serializers.SerializerMethodField()
    content_type_display = serializers.SerializerMethodField()

    class Meta:
        model = CRUDEvent
        fields = ['id', 'event_type_display', 'datetime', 'username', 'content_type_display', 'object_id',
                  'changed_fields']

    def get_event_type_display(self, obj):
        return obj.get_event_type_display()

    def get_username(self, obj):
        try:
            username = obj.user.username
        except AttributeError:
            username = '未知'
        return username

    def get_content_type_display(self, obj):
        content_type = ContentType.objects.get(id=obj.content_type_id)
        return content_type.app_label + '.' + content_type.model

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret.get('changed_fields') == 'null':
            ret['changed_fields'] = ''
        return ret
