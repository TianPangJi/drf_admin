from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    """
    用户
    """
    name = models.CharField(max_length=20, default='', blank=True, verbose_name='真实姓名')
    mobile = models.CharField(max_length=11, default='', unique=True, blank=True, verbose_name='手机号码')
    image = models.ImageField(upload_to='%Y/%m', default='default.png', blank=True, verbose_name='头像')
    roles = models.ManyToManyField('system.Roles', db_table='oauth_users_to_system_roles', blank=True,
                                   verbose_name='角色')
    department = models.ForeignKey('system.Departments', null=True, blank=True, on_delete=models.SET_NULL,
                                   verbose_name='部门')

    class Meta:
        db_table = 'oauth_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.username

    def _get_user_permissions(self):
        # 获取用户权限
        permissions = []
        for roles in self.roles.values('name'):
            if 'admin' == roles.get('name'):
                permissions.append('admin')
        for item in self.roles.values('permissions__sign').distinct():
            sign = item.get('permissions__sign')
            if sign:
                permissions.append(sign)
        return permissions

    def get_user_info(self):
        # 获取用户信息
        user_info = {
            'id': self.pk,
            'username': self.username,
            'name': self.name,
            'avatar': '/media/' + str(self.image),
            'email': self.email,
            'permissions': self._get_user_permissions()
        }
        return user_info
