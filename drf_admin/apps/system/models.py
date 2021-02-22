from django.db import models

from drf_admin.utils.models import BaseModel


class Permissions(BaseModel):
    """
    权限
    """
    method_choices = (
        (u'POST', u'增'),
        (u'DELETE', u'删'),
        (u'PUT', u'改'),
        (u'PATCH', u'局部改'),
        (u'GET', u'查')
    )

    name = models.CharField(max_length=30, verbose_name='权限名')
    sign = models.CharField(max_length=30, unique=True, verbose_name='权限标识')
    menu = models.BooleanField(verbose_name='是否为菜单')  # True为菜单,False为接口
    method = models.CharField(max_length=8, blank=True, default='', choices=method_choices, verbose_name='方法')
    path = models.CharField(max_length=200, blank=True, default='', verbose_name='请求路径正则')
    pid = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name='父权限')
    desc = models.CharField(max_length=30, blank=True, default='', verbose_name='权限描述')

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'system_permissions'
        verbose_name = '权限'
        verbose_name_plural = verbose_name
        ordering = ['id']


class Roles(BaseModel):
    """
    角色
    """
    name = models.CharField(max_length=32, unique=True, verbose_name='角色')
    permissions = models.ManyToManyField('Permissions', db_table='system_roles_to_system_permissions',
                                         blank=True, verbose_name='权限')
    desc = models.CharField(max_length=50, blank=True, default='', verbose_name='描述')

    objects = models.Manager()

    class Meta:
        db_table = 'system_roles'
        verbose_name = '角色'
        verbose_name_plural = verbose_name
        ordering = ['id']


class Departments(BaseModel):
    """
    组织架构 部门
    """
    name = models.CharField(max_length=32, unique=True, verbose_name='部门')
    pid = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name='父部门')

    objects = models.Manager()

    class Meta:
        db_table = 'system_departments'
        verbose_name = '部门'
        verbose_name_plural = verbose_name
        ordering = ['id']
