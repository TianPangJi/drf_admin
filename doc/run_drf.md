# DRF-ADMIN 后台管理系统

### 开发环境
**本项目在win10中开发，未在Linux中运行(Linux中可能存在Bug，建议使用Windows运行)**

### 编辑器
1. Pycharm
    * [安装教程](https://www.runoob.com/w3cnote/pycharm-windows-install.html)
2. Visual Studio Code
    * [安装教程](https://blog.csdn.net/qq_34195507/article/details/94558862)

### 后端运行
1. 版本说明
    * Python 3.6.2(建议使用Python3.x以上版本)
    * Redis 3.2.100
    * ~~MySQL~~ 待使用
2. 环境安装
    * Python
        * 建议使用Python虚拟环境，不占用系统Python
        * 虚拟环境可使用venv、virtualenv
        * 安装Python3.6版本以上
    * Redis
        * 安装Redis3.2版本以上
        * 开启Redis空间通知功能，设置notify-keyspace-events KEA
    * Git
        * 安装Git，用于代码拉取及提交
3. 项目启动
    * 拉取后端代码
        * [drf_admin](https://github.com/TianPangJi/drf_admin) ，在页面中直接Download ZIP
        * 或使用如下Git命令clone代码
            ```shell script
            git clone https://github.com/TianPangJi/drf_admin.git
            ```
    * 安装Python第三方包
        * ```shell script
            pip install -r requirements.txt
            ```
    * 配置Django配置文件
        * 默认使用SQLite，如使用MySQL，请更改settings/dev.py下的DATABASES参数
        * redis配置，配置settings/dev.py下REDIS_HOST、REDIS_PORT、REDIS_PWD等参数
    * 数据库迁移
        * ```shell script
            python manage.py migrate
            ```
    * 初始化数据库基础数据
        * ```shell script
            python manage.py loaddata init.json
            ```
    * 启动Django项目
        * ```shell script
            python manage.py runserver 0.0.0.0:8769
            ```
    * 接口文档Swagger
        * http://127.0.0.1:8769/api/swagger/

### 前端运行
1. 版本说明
    * Node.js >10.0
2. 环境安装
    * Node.js，安装https://nodejs.org/en/download/
    * 拉取前端代码
3. 项目启动
    * 拉取前端代码
        * [fe_admin](https://github.com/TianPangJi/fe_admin) ，在页面中直接Download ZIP
        * 或使用如下Git命令clone代码
            ```shell script
            git clone https://github.com/TianPangJi/fe_admin.git
            ```
    * 安装第三方包
        * ```shell script
          npm i  
            ```
    * 启动Vue项目
        * 如后端使用8769端口则，无需修改配置文件，如若修改后端启动端口，则需修改**.env.development**文件中的端口
        * ```shell script
            npm run dev
            ```

### 后置说明
1. 页面登录地址
    * http://localhost:9527/
2. 账户、角色、权限
    * Django 初始化数据库基础数据后，会生成2个账户、2个角色、项目权限
3. 账户
    * **admin/123456**，(admin为用户名，123456为密码，该账户为超级管理员用户，具有项目所用权限)
    * **visitor/123456**，(visitor为用户名，123456为密码，该账户为测试访客用户，具有项目部分权限)
4. 角色
    * **admin**，(admin角色，默认拥有项目所有权限；可给用户授予角色来给用户配置权限)
    * **visitor**，(visitor角色，默认拥有项目部分权限；可给用户授予角色来给用户配置权限)
5. 登录
    * 现在可以使用账户登录系统去体验了，加油搬砖人!!