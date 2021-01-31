## 三、drf_admin(权限RBAC)后台管理系统(鉴权篇) 
drf_admin采用Python、Django、DRF等技术开发，志在用最短的时间、最简洁的代码，实现开箱即用的后台管理系统。

欢迎访问[drf_admin](https://github.com/TianPangJi/drf_admin)；欢迎star，点个☆小星星☆哦。

## 项目地址
drf_admin（后端）：[https://github.com/TianPangJi/drf_admin](https://github.com/TianPangJi/drf_admin)
fe_admin（前端）：[https://github.com/TianPangJi/fe_admin](https://github.com/TianPangJi/fe_admin)

## 系列文章
* [一、drf_admin(权限RBAC)后台管理系统(介绍篇)](https://blog.csdn.net/Mr_w_ang/article/details/111303774)
* [二、drf_admin(权限RBAC)后台管理系统(配置篇)](https://blog.csdn.net/Mr_w_ang/article/details/113483668)
* [三、drf_admin(权限RBAC)后台管理系统(鉴权篇)](https://blog.csdn.net/Mr_w_ang/article/details/113484448)
* [四、drf_admin(权限RBAC)后台管理系统(RBAC权限篇)]() 留坑

## Web JWT鉴权
* 本项目使用django-rest-framework-jwt，但django-rest-framework-jwt项目已封存，后续可能更新为其他替代方案:
    * Fork: [django-rest-framework-jwt](https://github.com/Styria-Digital/django-rest-framework-jwt)
    * Alternative: [django-rest-framework-simplejwt](https://github.com/davesque/django-rest-framework-simplejwt)
* 如您想改用其他鉴权方式可参考[DRF官方文档](https://www.django-rest-framework.org/api-guide/authentication/#authentication)

## 配置文档
* 官方配置文档写的很全面,这里就不在做过多阐述，[→官方文档](https://jpadilla.github.io/django-rest-framework-jwt/)