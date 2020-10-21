""" 
@author   : Wang Meng
@github   : https://github.com/tianpangji 
@software : PyCharm 
@file     : users.py 
@create   : 2020/7/1 22:33 
"""
import re
import traceback

from django.conf import settings
from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from oauth.models import Users
from system.models import Roles


class UsersSerializer(serializers.ModelSerializer):
    """
    用户增删改查序列化器
    """
    roles_list = serializers.SerializerMethodField()
    date_joined = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    department_name = serializers.ReadOnlyField(source='department.name')

    class Meta:
        model = Users
        fields = ['id', 'username', 'name', 'mobile', 'email', 'is_active', 'department', 'department_name',
                  'date_joined', 'roles', 'roles_list']

    def validate(self, attrs):
        # 数据验证
        if attrs.get('mobile'):
            if not re.match(r'^1[3-9]\d{9}$', attrs.get('mobile')):
                raise serializers.ValidationError('手机格式不正确')
        return attrs

    def get_roles_list(self, obj):
        return [{'id': role.id, 'desc': role.desc} for role in obj.roles.all()]

    def create(self, validated_data):
        # 添加默认密码
        validated_data['password'] = settings.DEFAULT_PWD

        # 未直接调用父类create方法(原因: 新建用户时使用 create_user() 方法)
        raise_errors_on_nested_writes('create', self, validated_data)
        ModelClass = self.Meta.model

        # Remove many-to-many relationships from validated_data.
        # They are not valid arguments to the default `.create()` method,
        # as they require that the instance has already been saved.
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        try:
            instance = ModelClass._default_manager.create_user(**validated_data)
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                    'Got a `TypeError` when calling `%s.%s.create()`. '
                    'This may be because you have a writable field on the '
                    'serializer class that is not a valid argument to '
                    '`%s.%s.create()`. You may need to make the field '
                    'read-only, or override the %s.create() method to handle '
                    'this correctly.\nOriginal exception was:\n %s' %
                    (
                        ModelClass.__name__,
                        ModelClass._default_manager.name,
                        ModelClass.__name__,
                        ModelClass._default_manager.name,
                        self.__class__.__name__,
                        tb
                    )
            )
            raise TypeError(msg)

        # Save many-to-many relationships after the instance is created.
        if many_to_many:
            for field_name, value in many_to_many.items():
                field = getattr(instance, field_name)
                field.set(value)

        return instance


class UsersPartialSerializer(serializers.ModelSerializer):
    """
    用户局部更新序列化器
    """

    class Meta:
        model = Users
        fields = ['id', 'is_active']


class ResetPasswordSerializer(serializers.ModelSerializer):
    """
    重置密码序列化器
    """
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ['id', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate(self, attrs):
        # partial_update, 局部更新required验证无效, 手动验证数据
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if not password:
            raise serializers.ValidationError('字段password为必填项')
        if not confirm_password:
            raise serializers.ValidationError('字段confirm_password为必填项')
        if password != confirm_password:
            raise serializers.ValidationError('两次密码不一致')
        return attrs

    def save(self, **kwargs):
        # 重写save方法, 保存密码
        self.instance.set_password(self.validated_data.get('password'))
        self.instance.save()
        return self.instance
