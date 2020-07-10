from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    """
    用户
    """
    name = models.CharField(max_length=20, default='', verbose_name='真实姓名')
    mobile = models.CharField(max_length=11, default="", verbose_name='手机号码')
    image = models.ImageField(upload_to='media/%Y/%m', default='default.png', blank=True, verbose_name='头像')
    roles = models.ManyToManyField('system.Roles', blank=True, verbose_name='角色')

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.username
