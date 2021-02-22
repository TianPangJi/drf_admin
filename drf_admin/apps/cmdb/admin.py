import base64

from Crypto.Cipher import AES
from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet

from cmdb.models import Accounts
from cmdb.models import Assets, Servers, SecurityDevices, StorageDevices, NetworkDevices, IDC, Cabinets

# Register your models here.
admin.site.register(Assets)
admin.site.register(Servers)
admin.site.register(SecurityDevices)
admin.site.register(StorageDevices)
admin.site.register(NetworkDevices)
admin.site.register(IDC)
admin.site.register(Cabinets)


def get_password_display(password):
    """
    原始位置：drf_admin.utils.models.BasePasswordModels.get_password_display
    注：如果原始位置的代码发生更改，也需要更改次函数

    AES 解密登录密码
    :return: 原明文密码
    """
    aes = AES.new(str.encode(settings.SECRET_KEY[4:20]), AES.MODE_ECB)
    return str(
        aes.decrypt(base64.decodebytes(bytes(str(password), encoding='utf8'))).rstrip(b'\0').decode("utf8"))


@admin.register(Accounts)
class AccountsAdmin(admin.ModelAdmin):
    def get_object(self, request, object_id, from_field=None):
        """
        Return an instance matching the field and value provided, the primary
        key is used if no field is provided. Return ``None`` if no match is
        found or the object_id fails validation.
        """

        queryset = self.get_queryset(request)  # type: QuerySet
        model = queryset.model
        field = model._meta.pk if from_field is None else model._meta.get_field(from_field)

        try:
            object_id = field.to_python(object_id)
            result = queryset.get(**{field.name: object_id})  # type:Accounts
            # 解密被加密的密码，允许在Django Admin中显示原始密码，仅在数据库中将密码加密存储
            result.password = get_password_display(result.password)
            return result
        except (model.DoesNotExist, ValidationError, ValueError):
            return None
