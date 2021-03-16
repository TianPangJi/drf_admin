from django.contrib import admin
from django.contrib.auth import get_user_model

from system.models import Permissions, Roles, Departments

Users = get_user_model()

# Register your models here.
admin.site.register(Users)
admin.site.register(Permissions)
admin.site.register(Roles)
admin.site.register(Departments)
