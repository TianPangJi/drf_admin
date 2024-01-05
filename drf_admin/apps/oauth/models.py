from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    """
    用户
    """
    GENDER_CHOICES = [
        ('男性', '男性'),
        ('女性', '女性'),
        ('其他', '其他'),
        # 可根據需求添加更多選項
    ]
    name = models.CharField(max_length=20, default='', blank=True, verbose_name='真實姓名')
    mobile = models.CharField(max_length=11, unique=True, null=True, blank=True, default=None, verbose_name='手機號碼')
    image = models.ImageField(upload_to='avatar/%Y/%m', default='avatar/default.png', blank=True, verbose_name='头像')
    roles = models.ManyToManyField('system.Roles', db_table='oauth_users_to_system_roles', blank=True,
                                   verbose_name='角色')
    department = models.ForeignKey('system.Departments', null=True, blank=True, on_delete=models.SET_NULL,
                                   verbose_name='部门')
    # gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    gender = models.CharField(max_length=11,choices=GENDER_CHOICES,  null=True, blank=True, default=None, verbose_name='性別')


    class Meta:
        db_table = 'oauth_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.username

    def _get_user_permissions(self):
        # 获取用户权限
        permissions = list(filter(None, set(self.roles.values_list('permissions__sign', flat=True))))
        if 'admin' in self.roles.values_list('name', flat=True):
            permissions.append('admin')
        return permissions

    def get_user_info(self):
        # 获取用户信息
        user_info = {
            'id': self.pk,
            'username': self.username,
            'name': self.name,
            'gender': self.gender,
            'avatar': '/media/' + str(self.image),
            'email': self.email,
            'permissions': self._get_user_permissions(),
            'department': self.department.name if self.department else '',
            'mobile': '' if self.mobile is None else self.mobile
        }
        return user_info
