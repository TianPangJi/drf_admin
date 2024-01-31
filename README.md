# DILAB後台管理系統(1/31更新)

#### 專案简介
一個基於 Django、Django REST framework（DRF）、Channels、Redis、Vue的前後端分離的後台管理系統


#### 專案程式碼
|     |   後端程式碼  |   前端程式碼   |
|---  |--- | --- |
|  github   |  https://github.com/peter1421/drf_admin   |  https://github.com/peter1421/fe_admin   |

#### 專案啟動
* [TODO:委託/領取任務]()
* https://github.com/peter1421/drf_admin/issues
* https://github.com/users/peter1421/projects/2
* [啟動專案教學](https://github.com/peter1421/drf_admin/blob/master/doc/run_drf.md)
* [TODO:推送程式碼教學]()
* [TODO:伺服器部屬]()

#### 程式碼結構
```python
"""
├── celery_task # Celery非同步任務
├── docs # 文檔
├── drf_admin # 專案主文件
│ ├── apps # 專案app
│ ├── common # 公共接口
│ ├── media # 上傳文件media
│ ├── settings # 設定文件
│ ├── utils # 全域工具
│ │ ├── exceptions.py # 異常捕獲
│ │ ├── middleware.py # 中介軟體
│ │ ├── models.py # 基類models文件
│ │ ├── pagination.py # 分頁配置
│ │ ├── permissions.py # RBAC權限控制
│ │ ├── routers.py # 視圖routers
│ │ ├── swagger_schema.py # swagger
│ │ ├── views.py # 基類視圖
│ │ └── websocket.py # WebSocket使用者驗證
│ ├── routing.py # WebSocket路由
│ ├── urls.py # 專案根路由
│ └── wsgi.py # wsgi
├── .gitignore # .gitignore文件
├── init.json # 資料庫基礎資料文件
├── LICENSE # LICENSE
├── manage.py # 專案入口、啟動文件
├── README.md # README
└── requirements.txt # requirements文件
"""
```