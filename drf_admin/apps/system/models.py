from django.db import models


class Permissions(models.Model):
    """
    权限
    """
    method_choices = (
        (u'POST', u'增'),
        (u'DELETE', u'删'),
        (u'PUT', u'改'),
        (u'GET', u'查'),
    )

    name = models.CharField(max_length=30, unique=True, verbose_name='权限名')
    method = models.CharField(max_length=50, choices=method_choices, verbose_name='方法')
    path = models.CharField(max_length=200, verbose_name='请求路径正则')
    pid = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name='父权限')
    desc = models.CharField(max_length=30, unique=True, verbose_name='权限描述')

    objects = models.Manager()

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
    desc = models.CharField(max_length=50, blank=True, default='', verbose_name='描述')

    objects = models.Manager()

    class Meta:
        db_table = 'roles'
        verbose_name = '角色'
        verbose_name_plural = verbose_name
        ordering = ['id']


class Departments(models.Model):
    """
    组织架构 部门
    """
    name = models.CharField(max_length=32, unique=True, verbose_name='部门')
    pid = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name='父部门')

    objects = models.Manager()

    class Meta:
        db_table = 'department'
        verbose_name = '部门'
        verbose_name_plural = verbose_name
        ordering = ['id']
