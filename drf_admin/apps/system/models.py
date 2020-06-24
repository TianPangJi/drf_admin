from django.db import models


class Permissions(models.Model):
    """
    权限
    """
    name = models.CharField(max_length=30, unique=True, verbose_name='权限名')
    method = models.CharField(max_length=50, null=True, blank=True, verbose_name='方法')
    path = models.CharField(max_length=200, null=True, blank=True, verbose_name='请求路径正则')
    pid = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='父权限')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'permissions'
        verbose_name = '权限'
        verbose_name_plural = verbose_name
        ordering = ['id']


class Roles(models.Model):
    """
    角色
    """
    name = models.CharField(max_length=32, unique=True, verbose_name='角色')
    permissions = models.ManyToManyField('Permissions', blank=True, verbose_name='权限')
    desc = models.CharField(max_length=50, blank=True, null=True, verbose_name='描述')

    class Meta:
        db_table = 'roles'
        verbose_name = '角色'
        verbose_name_plural = verbose_name
        ordering = ['id']
