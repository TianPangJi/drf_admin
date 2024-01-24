# DRF-ADMIN 後台管理系統

### 開發環境
**本項目在win10中開發，未在Linux中運行(Linux中可能存在Bug，建議使用Windows運行)**

### 編輯器
1. Pycharm
    * [安裝教程](https://www.runoob.com/w3cnote/pycharm-windows-install.html)
2. Visual Studio Code
    * [安裝教程](https://blog.csdn.net/qq_34195507/article/details/94558862)

### 後端運行
####[操作影片](https://drive.google.com/file/d/1R7ilOs6_h92KCHC8I-FpJSNTmU9JYaYz/view?usp=drive_link)
1. 版本說明
    * Python 3.6.2(建議使用Python3.x以上版本)
    * Redis 3.2.100
    * ~~MySQL~~ 待使用
2. 環境安裝
    * Python
        * 建議使用Python虛擬環境，不占用系統Python
        * 虛擬環境可使用venv、virtualenv
        * 安裝Python3.6版本以上
    * Redis
        * 安裝Redis3.2版本以上
        * 開啟Redis空間通知功能，設置notify-keyspace-events KEA
    * Git
        * 安裝Git，用於代碼拉取及提交
3. 項目啟動
    * 拉取後端代碼
        * [drf_admin](https://github.com/peter1421/drf_admin)，在頁面中直接Download ZIP
        * 或使用如下Git命令clone代碼
            ```shell
            git clone https://github.com/peter1421/drf_admin
            ```
    * 虛擬環境配置(python 3.9.0)
        * ```shell
            python -m  venv venv 
            venv/Scripts/Activate.ps1
            ```
    * 安裝Python第三方包
        * ```shell
            pip install -r requirements.txt
            ```
    * 配置Django配置文件
        * 默認使用SQLite，如使用MySQL，請更改settings/dev.py下的DATABASES參數
        * redis配置，配置settings/dev.py下REDIS_HOST、REDIS_PORT、REDIS_PWD等參數
    * 數據庫遷移
        * ```shell
            python manage.py migrate
            ```
    * 如果有出問題 重新裝一次openai
        * ```shell
            pip install openai
            ```
    * ~~初始化數據庫基礎數據~~(已有現成的資料庫)
        * ```shell
            python manage.py loaddata init.json(略過)
            ```
    * 啟動Django項目
        * ```shell
            python manage.py runserver 0.0.0.0:8769
            ```
    * 接口文檔Swagger
        * http://127.0.0.1:8769/api/swagger/
    * 如果聊天功能出現接口錯誤，去重開一個api，並更改
        ```shell
            drf_admin\apps\chatbot\backend.py
            openai.api_key = "TOKEN"  # 替换为您的 OpenAI API 密钥
            ```

### 前端運行
1. 版本說明
    * Node.js >10.0
2. 環境安裝
    * Node.js，安裝https://nodejs.org/en/download/
    * 拉取前端代碼
3. 項目啟動
    * 拉取前端代碼
        * [fe_admin](https://github.com/peter1421/fe_admin)，在頁面中直接Download ZIP
        * 或使用如下Git命令clone代碼
            ```shell
            git clone https://github.com/peter1421/fe_admin
            ```
    * 安裝第三方包
        * ```shell
          npm i  
            ```
    * 啟動Vue項目
        * 如後端使用8769端口則，無需修改配置文件，如若修改後端啟動端口，則需修改**.env.development**文件中的端口
        * ```shell
            npm run dev
            ```

### 後置說明
1. 頁面登錄地址
    * http://localhost:9527/
2. 賬戶、角色、權限
    * Django 初始化數據庫基礎數據後，會生成2個賬戶、2個角色、項目權限
3. 賬戶
    * **admin/123456**，(admin為用戶名，123456為密碼，該賬戶為超級管理員用戶，具有項目所用權限)
    * **visitor/123456**，(visitor為用戶名，123456為密碼，該賬戶為測試訪客用戶，具有項目部分權限)
4. 角色
    * **admin**，(admin角色，默認擁有項目所有權限；可給用戶授予角色來給用戶配置權限)
    * **visitor**，(visitor角色，默認擁有項目部分權限；可給用戶授予角色來給用戶配置權限)
5. 登錄
    * 現在可以使用賬戶登錄系統去體驗了，加油搬磚人!!
