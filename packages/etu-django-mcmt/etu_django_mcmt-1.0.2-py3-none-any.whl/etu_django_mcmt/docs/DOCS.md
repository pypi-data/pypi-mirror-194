# 概括
    etu 系列（easy to use）
    让技术更容易使用！
    Etu Django Migrations Cache Manager Tool，此工具是用于Django框架项目，功能主要是管理 Migrations 缓存，
    实现让 Python 项目更容易上容器，解决容器生命周期 migrations 文件管理不便的问题。


## 说明
    本包名字为 etu-django-mcmt , 通过 setting 配置中 INSTALLED_APPS 的方式导入 etu_django_mcmt 即可。
    目前此工具只支持单一数据库路由模式，不可用于多数据库路由模式，且数据类型为 MySQL 类型。


### 安装方法
    通过pip命令进行安装：pip install etu-django-mcmt==1.0.0


### 参数说明
```python
# settings.py 中新增 etu_django_mcmt
    INSTALLED_APPS = [
        'etu_django_mcmt',
    ]
# 配置说明
DCM_DB_ALIAS = 'default' # 在setting中或者环境变量配置，默认是 default ，可以不用配置
DCM_APP_NAMES = ['app']  # 配置指定的模块列表，即 INSTALLED_APPS 中需要管理 migrations 的模块
```


### 使用方法
```shell
    python manage.py db_makemigrations 
    python manage.py db_migrate 
```


### 错误反馈
    
