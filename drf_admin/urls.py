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
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from rest_framework.documentation import include_docs_urls

from drf_admin.settings.dev import MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),  # 后台管理
    path(r'api/system/', include('system.urls')),  # 系统管理模块
    path(r'api/oauth/', include('oauth.urls')),  # 用户鉴权模块
    path(r'docs/', include_docs_urls(title='My API Docs')),  # API文档
    re_path(r'media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT})
]
