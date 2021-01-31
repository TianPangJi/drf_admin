<h1 style="text-align: center">drf_admin(权限RBAC)后台管理系统</h1>

## drf_admin(权限RBAC)后台管理系统(介绍篇)
drf_admin采用Python、Django、DRF等技术开发，志在用最短的时间、最简洁的代码，实现开箱即用的后台管理系统。

欢迎访问[drf_admin](https://github.com/TianPangJi/drf_admin)；欢迎给点个☆小星星☆哦

## 项目地址
drf_admin（后端）：[https://github.com/TianPangJi/drf_admin](https://github.com/TianPangJi/drf_admin)
fe_admin（前端）：[https://github.com/TianPangJi/fe_admin](https://github.com/TianPangJi/fe_admin)

## 系列文章
* [一、drf_admin(权限RBAC)后台管理系统(介绍篇)](https://blog.csdn.net/Mr_w_ang/article/details/111303774)
* [二、drf_admin(权限RBAC)后台管理系统(配置篇)](https://blog.csdn.net/Mr_w_ang/article/details/113483668)
* [三、drf_admin(权限RBAC)后台管理系统(鉴权篇)](https://blog.csdn.net/Mr_w_ang/article/details/113484448)
* [四、drf_admin(权限RBAC)后台管理系统(RBAC权限篇)]() 留坑

## 系统功能
* JWT鉴权
* RBAC权限验证
* Swagger接口文档
* WebSocket
* 后台日志log
* 系统管理
    * 用户管理
    * 角色管理
    * 权限管理
    * 部门管理
    * 任务调度(Cron任务)
* 系统监控
    * 在线用户
    * IP黑名单
    * crud日志
    * 错误日志
    * 服务监控

## 主要应用技术
* Django
* Django Rest Framework
* APScheduler
* drf-yasg
* channels
* redis


## 项目目录结构
```
├── celery_task                # Celery异步任务(留坑)
├── docs                       # 文档(留坑)
├── drf_admin                  # 项目主文件
│   ├── apps                   # 项目app
│   ├── common                 # 公共接口
│   ├── media                  # 上传文件media
│   ├── settings               # 配置文件
│   ├── utils                  # 全局工具
│   │   ├── exceptions.py      # 异常捕获
│   │   ├── middleware.py      # 中间件
│   │   ├── models.py          # 基类models文件
│   │   ├── pagination.py      # 分页配置
│   │   ├── permissions.py     # RBAC权限控制
│   │   ├── routers.py         # 视图routers
│   │   ├── views.py           # 基类视图
│   │   └── websocket.py       # WebSocket用户验证
│   ├── routing.py             # WebSocket路由
│   ├── urls.py                # 项目根路由
│   └── wsgi.py                # wsgi
├── .gitignore                 # .gitignore文件
├── LICENSE                    # LICENSE
├── README.md                  # README
├── manage.py                  # 项目入口、启动文件
└── requirements.txt           # requirements文件
```

## 系统预览
<table>
    <tr>
        <td><img src="https://img-blog.csdnimg.cn/2020111416290077.png" border="0" /></td>
        <td><img src="https://img-blog.csdnimg.cn/20201114162859446.png" border="0" /></td>
    </tr>
    <tr>
        <td><img src="https://img-blog.csdnimg.cn/20201114162858969.png" border="0" /></td>
        <td><img src="https://img-blog.csdnimg.cn/20201114162858867.png" border="0" /></td>
    </tr>
    <tr>
        <td><img src="https://img-blog.csdnimg.cn/20201114162858866.png" border="0" /></td>
        <td><img src="https://img-blog.csdnimg.cn/20201114162858950.png" border="0" /></td>
    </tr>
    <tr>
        <td><img src="https://img-blog.csdnimg.cn/20201114162858834.png" border="0" /></td>
        <td><img src="https://img-blog.csdnimg.cn/20201114162859656.png" border="0" /></td>
    </tr>
</table>