from django.contrib import admin

from oauth.models import Users
from system.models import Permissions, Roles, Departments

# Register your models here.
admin.site.register(Users)
admin.site.register(Permissions)
admin.site.register(Roles)
admin.site.register(Departments)
