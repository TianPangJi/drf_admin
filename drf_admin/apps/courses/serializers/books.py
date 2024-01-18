import re

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from drf_admin.apps.courses.models import Book

# Users = get_user_model()

class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
    """
    用户增删改查序列化器
    """
    # roles_list = serializers.SerializerMethodField()
    # date_joined = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    # department_name = serializers.ReadOnlyField(source='department.name')
    # is_superuser = serializers.BooleanField(read_only=True)

    # class Meta:
        # model = Users
        # fields = ['id', 'username', 'name', 'mobile', 'email', 'is_active', 'department', 'department_name',
        #           'date_joined', 'roles', 'roles_list', 'is_superuser']

    # def validate(self, attrs):
    #     # 数据验证
    #     if attrs.get('username'):
    #         if attrs.get('username').isdigit():
    #             raise serializers.ValidationError('用户名不能为纯数字')
    #     if attrs.get('mobile'):
    #         if not re.match(r'^1[3-9]\d{9}$', attrs.get('mobile')):
    #             raise serializers.ValidationError('手机格式不正确')
    #     if attrs.get('mobile') == '':
    #         attrs['mobile'] = None
    #     return attrs

    # def get_roles_list(self, obj):
    #     return [{'id': role.id, 'desc': role.desc} for role in obj.roles.all()]

    # def create(self, validated_data):
    #     # user = super().create(validated_data)
    #     # # 添加默认密码
    #     # user.set_password(settings.DEFAULT_PWD)
    #     # user.save()
    #     # return user
    #     print('create')
    #     return 'user'
