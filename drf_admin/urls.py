"""drf_admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# swagger API文档配置
schema_view = get_schema_view(
    openapi.Info(
        title="DRF Admin API",
        default_version='v1.0.0',
        description="Test Description",
        terms_of_service="https://github.com/tianpangji",
        contact=openapi.Contact(email="92178199@qq.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

base_api = settings.BASE_API

urlpatterns = [
    # admin管理页面
    path('admin/', admin.site.urls),

    # 项目模块
    path(f'{base_api}oauth/', include('oauth.urls')),  # 用户鉴权模块
    path(f'{base_api}system/', include('system.urls')),  # 系统管理模块
    path(f'{base_api}monitor/', include('monitor.urls')),  # 系统监控模块
    path(f'{base_api}cmdb/', include('cmdb.urls')),  # 资源管理模块

    # swagger(API文档)
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
