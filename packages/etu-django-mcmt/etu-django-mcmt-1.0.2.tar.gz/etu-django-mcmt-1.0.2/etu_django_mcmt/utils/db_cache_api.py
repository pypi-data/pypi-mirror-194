# -*- coding: utf-8 -*-
# @Time    : 2022/12/31 17:10
# @Author  : Jieay
# @File    : db_cache_api.py
import logging
logger = logging.getLogger(__name__)

import os
import re
# import shutil
import datetime
import difflib
from django.apps import apps
# from importlib import import_module
# from django.utils.module_loading import module_has_submodule
# from importlib import import_module
# from importlib.util import find_spec as importlib_find
from django.db import DEFAULT_DB_ALIAS, connections, router
from .commapi import datetime_to_str
from django.conf import settings


class DjangoCacheMigrations(object):
    """Django Migrations 缓存管理"""

    DJ_PROJECT_ROOT = settings.BASE_DIR
    dcm_table_name = 'django_cache_migrations'
    dm_table_name = 'django_migrations'
    sql_create_table = "CREATE TABLE %(table)s (%(definition)s)"
    sqlite_create_table_id_field_sql = '`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT'
    mysql_create_table_id_field_sql = '`id` bigint(20) NOT NULL AUTO_INCREMENT'
    create_table_comm_field_sql = (
        '`app` varchar(255) NOT NULL',
        '`name` varchar(255) NOT NULL',
        '`mtime` datetime(6) NOT NULL',
        '`contents` longtext'
    )
    sql_check_table = "SELECT * FROM %(table)s LIMIT 1"
    sql_select_table = "SELECT %(column)s FROM %(table)s %(definition)s"
    # column_value_exp: app='xxx', name='xxx.py'
    sql_update_table = "UPDATE %(table)s SET %(set_column_value_exp)s WHERE %(term_column_value_exp)s"
    # column_value: 'app', 'name', 'mtime', 'contents'
    sql_insert_table = "INSERT INTO %(table)s VALUES(NULL, %(column_value)s)"

    def __init__(self, db_alias=DEFAULT_DB_ALIAS, app_names=None):
        """
        :param db_alias: DB别名，默认：default，是settings中 DATABASES 的 KEY
        """
        self.DB_ALIAS = db_alias
        self.app_names = app_names

    def print_base_info(self):
        """输出基础信息"""
        logger.info('数据库类型: {}'.format(self.get_db_type()))
        logger.info('数据库标签: {}'.format(self.DB_ALIAS))
        logger.info('项目app标签: {}'.format(','.join(self.app_labels())))

    def _dj_project_root_dirs(self):
        """获取项目根目录下子目录"""
        dj_p_list = os.listdir(self.DJ_PROJECT_ROOT)
        return [x for x in dj_p_list if os.path.isdir(x)]

    def app_labels(self):
        """
        获取所有app标签
        :return: `set` {app,xxx}
        """
        un_migrated_apps = set()
        for app_config in apps.get_app_configs():
            un_migrated_apps.add(app_config.label)
        # 指定 app 标签则取值指定的标签
        if isinstance(self.app_names, (list, tuple)) and self.app_names:
            un_migrated_apps = un_migrated_apps.intersection(self.app_names)
        dj_project_root_dirs = self._dj_project_root_dirs()
        # 检查标签是否是项目子目录
        un_migrated_apps = un_migrated_apps.intersection(dj_project_root_dirs)
        return un_migrated_apps

    def connection(self):
        """
        创建DB连接
        """
        db_connection = connections[self.DB_ALIAS]
        db_connection.prepare_database()
        return db_connection

    def get_db_type(self):
        """
        获取DB客户端类型
        :return: mysql | sqlite3
        """
        connection = self.connection()
        return connection.client.executable_name

    def go_cursor(self):
        """
        获取数据库连接
        :return: cursor 对象
        """
        connection = self.connection()
        return connection.cursor()

    def cursor_execute(self, sql_data):
        """
        执行SQL语句
        :param sql_data: SQL语句
        """
        connection = self.connection()
        return connection.cursor().execute(sql_data)

    def select_execute(self, sql_data):
        """
        执行查询SQL语句
        :param sql_data: SQL语句
        """
        cursor = self.go_cursor()
        cursor.execute(sql_data)
        return cursor.fetchall()

    def get_tables(self):
        """
        获取数据库中所有表名称列表
        :return: `list` ['app_common_fake', 'auth_group']
        """
        connection = self.connection()
        with connection.cursor() as cursor:
            tables = connection.introspection.table_names(cursor)
        return tables

    def all_models(self):
        """
        获取 Django 各个模块的数据模型
        :return: `list` [('app', [app.models.common.fake_model.FakeModel, app.models.user.members.Members])]
        """
        app_labels = self.app_labels()
        connection = self.connection()
        all_models = [
            (
                app_config.label,
                router.get_migratable_models(app_config, connection.alias, include_auto_created=False),
            )
            for app_config in apps.get_app_configs()
            if app_config.models_module is not None and app_config.label in app_labels
        ]
        return all_models

    def get_manifest(self):
        """
        获取 migrations 有变更的 各个模块的数据模型
        :return: `dict` {'admin': [], 'app': [app.models.asset.cluster_model.ClustersModel,]}
        """
        connection = self.connection()
        tables = self.get_tables()
        all_models = self.all_models()

        def model_installed(model):
            opts = model._meta
            converter = connection.introspection.identifier_converter
            return not (
                (converter(opts.db_table) in tables) or
                (opts.auto_created and converter(opts.auto_created._meta.db_table) in tables)
            )

        manifest = {
            app_name: list(filter(model_installed, model_list))
            for app_name, model_list in all_models
        }
        return manifest

    def _set_create_table_sql(self, field_list):
        """
        构造创建表SQL语句
        :param field_list: 字段语法列表
        :return: SQL语句
        """
        sql = self.sql_create_table % {
            'table': self.dcm_table_name,
            'definition': ', '.join(field_list),
        }
        return sql

    def _set_check_table_sql(self):
        """
        构造查询表SQL语句
        :return: SQL语句
        """
        sql = self.sql_check_table % {
            'table': self.dcm_table_name
        }
        return sql

    def get_cache_mysql_create_table_sql(self):
        """
        MySQL数据库创建migrations缓存表SQL语句
        :return: SQL语句
        """
        field_list = [self.mysql_create_table_id_field_sql]
        field_list.extend(self.create_table_comm_field_sql)
        field_list.append('PRIMARY KEY (`id`)')
        return self._set_create_table_sql(field_list)

    def get_cache_sqlite_create_table_sql(self):
        """
        sqlite数据库创建migrations缓存表SQL语句
        :return: SQL语句
        """
        field_list = [self.sqlite_create_table_id_field_sql]
        field_list.extend(self.create_table_comm_field_sql)
        return self._set_create_table_sql(field_list)

    def get_cache_check_table_sql(self):
        """
        查询migrations缓存表SQL语句
        :return: SQL语句
        """
        return self._set_check_table_sql()

    def check_cache_table_is_exist(self):
        """
        检查数据库中migrations缓存表是否存在
        :return: `bool` True or False
        """
        try:
            self.select_execute(self.get_cache_check_table_sql())
        except Exception as e:
            logger.debug(e)
            return False
        return True

    def create_django_cache_migrations_table(self):
        """
        创建migrations缓存表
        """
        db_type = self.get_db_type()
        if db_type in ['mysql']:
            sql = self.get_cache_mysql_create_table_sql()
        elif db_type in ['sqlite3', 'sqlite']:
            sql = self.get_cache_sqlite_create_table_sql()
        else:
            sql = ''
        if not sql:
            return False
        try:
            self.cursor_execute(sql)
        except Exception as e:
            logger.error(e)
            return False
        return True

    def _set_select_table_sql(self, name_list=None, term_data=None, table_name=None):
        """
        构造查询数据SQL语句
        :param term_data: 查询条件，{'field1': 'value1', 'field2': 'value2'}
        :return: 查询SQL语句
        """
        if not isinstance(term_data, dict):
            term_data = {}

        if table_name in [self.dcm_table_name, self.dm_table_name]:
            table = table_name
        else:
            table = self.dcm_table_name
        term_column_value_exp = []
        column_name_list = ['*']
        if isinstance(name_list, (list, tuple)):
            column_name_list = name_list
        for k, v in term_data.items():
            column_value_exp = '%(column_name)s="%(column_value)s"' % {'column_name': k, 'column_value': v}
            term_column_value_exp.append(column_value_exp)
            if name_list:
                column_name_list.append(k)

        if term_column_value_exp:
            definition = 'WHERE %s' % ' AND '.join(term_column_value_exp)
        else:
            definition = ';'
        column_name_list = list(set(column_name_list))
        sql = self.sql_select_table % {
            'column': ','.join(column_name_list),
            'table': table,
            'definition': definition
        }
        return column_name_list, sql

    def get_cache_check_table_column_sql(self, data):
        """
        查询 migrations 缓存表指定字段值是否存在SQL语句
        :param data: {'app': 'app', 'name': '0001_initial.py'}
        :return: 查询SQL语句
        """
        name_list = ['app', 'name']
        term_data = {'app': data.get('app', ''), 'name': data.get('name', '')}
        return self._set_select_table_sql(name_list=name_list, term_data=term_data)

    def check_django_cache_migrations_column_data_exist(self, data):
        """
        检查 migrations 缓存表中app和name字段记录是否存在
        :param data: {'app': 'app', 'name': '0001_initial.py'}
        :return: `bool` 存在 True | 否则 False
        """
        is_exist = False
        column_name_list, sql = self.get_cache_check_table_column_sql(data=data)
        logger.info("检查 migrations 缓存表中记录: {}".format(sql))
        try:
            cursor = self.cursor_execute(sql)
            if cursor != 0:
                is_exist = True
        except Exception as e:
            logger.error(e)
        return is_exist

    def _set_insert_column_value_data(self, data):
        """
        构造migrations缓存表新增数据记录的value表达式
        :param data: {'app': '', 'name': '', 'contents': ''}
        :return: `str`
        """
        _data = '"%s","%s","%s","%s"' % (
            data.get('app', ''),
            data.get('name', ''),
            datetime_to_str(datetime.datetime.now()),
            data.get('contents', '')
        )
        return _data

    def get_cache_insert_table_sql(self, data):
        """
        获取migrations缓存表新增数据记录SQL语句
        :param data: {'app': '', 'name': '', 'contents': ''}
        :return: SQL语句
        """
        column_value_data = self._set_insert_column_value_data(data=data)
        sql = self.sql_insert_table % {
            'table': self.dcm_table_name,
            'column_value': column_value_data
        }
        return sql

    def _set_update_column_value_exp_data(self, data):
        """
        构造migrations缓存表更新数据记录的value表达式和条件表达式
        :param data: {'app': '', 'name': '', 'contents': ''}
        :return: `tuple`
        """
        set_column_value_exp = (
            'app="%s"' % data.get('app', ''),
            'name="%s"' % data.get('name', ''),
            'mtime="%s"' % datetime_to_str(datetime.datetime.now()),
            'contents="%s"' % data.get('contents', '')
        )
        term_column_value_exp = (
            'app="%s"' % data.get('app', ''),
            'name="%s"' % data.get('name', '')
        )
        return set_column_value_exp, term_column_value_exp

    def get_cache_update_table_sql(self, data):
        """
        获取migrations缓存表更新数据记录SQL语句
        :param data: {'app': '', 'name': '', 'contents': ''}
        :return: SQL语句
        """
        set_column_value_exp, term_column_value_exp = self._set_update_column_value_exp_data(data=data)
        sql = self.sql_update_table % {
            'table': self.dcm_table_name,
            'set_column_value_exp': ', '.join(set_column_value_exp),
            'term_column_value_exp': ' AND '.join(term_column_value_exp)
        }
        return sql

    def check_django_cache_migrations(self):
        """
        【检查表】检查 migrations 缓存表是否存在，不存在则创建
        :return: `bool` 存在或者创建成功返回 True
        """
        if self.check_cache_table_is_exist() is False:
            logger.info('Migrations 缓存表不存在，开始创建表。')
            if self.create_django_cache_migrations_table() is True:
                logger.info('创建 migrations 缓存表成功！')
                return True
            else:
                logger.info('创建 migrations 缓存表失败！')
        else:
            logger.info('Migrations 缓存表已经存在。')
            return True
        return False

    def get_django_cache_migrations_to_app(self, name):
        """
        获取指定 app 的 migrations 缓存表数据
        :param name: app 名称，标签名称
        :return: `list` [{'field1': 'value1', 'field2': 'value2'}]
        """
        data = []
        name_list = ['app', 'name', 'contents']
        term_data = {'app': name}
        column_name_list, sql = self._set_select_table_sql(name_list=name_list, term_data=term_data)
        query_data = self.select_execute(sql)
        for _data in query_data:
            data.append(dict(zip(column_name_list, _data)))
        return data

    def check_contents_diff_is_alike(self, n_c_lines, o_c_lines):
        """
        检查 contents 是否相似
        :param n_c_lines: 新 contents 值，n_c_lines.splitlines() ，[]
        :param o_c_lines: 旧 contents 值，o_c_lines.splitlines()，[]
        :return: `bool` 相似 True
        """
        d = difflib.Differ()
        diff = d.compare(n_c_lines, o_c_lines)
        data = list(diff)
        # 检查对比值是否有差异，-（n_c_lines 相对 o_c_lines减少）+ （o_c_lines 相对 n_c_lines 新增）
        data = [x for x in data if re.match('^[-+]', x)]
        if len(data) == 2 and '# Generated by Django' in data:
            return True
        if not data:
            return True
        return False

    def get_django_migrations_to_app(self, name):
        """
        获取 django_migrations 表指定 app 数据记录
        :param name: app 名称，标签名称
        :return: `list` [{'field1': 'value1', 'field2': 'value2'}]
        """
        data = []
        name_list = ['app', 'name']
        term_data = {'app': name}
        column_name_list, sql = self._set_select_table_sql(
            name_list=name_list, term_data=term_data, table_name=self.dm_table_name
        )
        try:
            query_data = self.select_execute(sql)
            for _data in query_data:
                data.append(dict(zip(column_name_list, _data)))
        except Exception as e:
            logger.error(e)
        return data

    def add_django_cache_migrations_data(self, data):
        """
        新增 migrations 缓存表数据记录
        :param data: {'app': '', 'name': '', 'contents': ''}
        :return: `bool`
        """
        app = data.get('app', '')
        name = data.get('name', '')
        insert_sql = self.get_cache_insert_table_sql(data)
        update_sql = self.get_cache_update_table_sql(data)
        django_migrations_to_app_list = self.get_django_migrations_to_app(name=app)
        name_list = ['%s.py' % x.get('name') for x in django_migrations_to_app_list if x.get('name')]

        # 检查相同的 app 下，新增 migration 是否已经 migrate，未执行则无需新增
        if name_list and name not in name_list:
            return False

        try:
            # 检查数据记录是否存在，存在则更新数据，不存在则新增数据
            if self.check_django_cache_migrations_column_data_exist(data=data):
                logger.info('开始更新 migrations 缓存表数据，{app} - {name}'.format(**data))
                self.cursor_execute(update_sql)
            else:
                logger.info('开始新增 migrations 缓存表数据，{app} - {name}'.format(**data))
                self.cursor_execute(insert_sql)
            return True
        except Exception as e:
            logger.error(e)
        return False

    def get_app_migrations_dir(self, name):
        """
        获取 app 的 migrations 目录
        :param name: app 名称
        :return: dir
        """
        return os.path.join(self.DJ_PROJECT_ROOT, name, 'migrations')

    def get_app_migrations_files(self, name):
        """
        获取 app 的 migrations 目录下的文件
        :param name: app 名称
        :return: `list`
        """
        app_migrations_dir = self.get_app_migrations_dir(name)
        return os.listdir(app_migrations_dir)

    def clean_app_migrations_dir(self, name):
        """
        清除指定 app 下的 migrations 目录文件
        :param name: app 名称
        :return: `list`
        """
        clean_files = []
        if self.get_db_type() in ['sqlite3', 'sqlite']:
            return clean_files
        app_migrations_dir = self.get_app_migrations_dir(name)
        exclude_files = ['__init__.py']
        if os.path.exists(app_migrations_dir):
            for a_m_file in self.get_app_migrations_files(name):
                if a_m_file not in exclude_files:
                    # 删除文件
                    clean_files.append(a_m_file)
                    rm_file = os.path.join(app_migrations_dir, a_m_file)
                    if os.path.exists(rm_file) and os.path.isfile(rm_file):
                        logger.info('清除本地文件：{}'.format(rm_file))
                        logger.info('开始清除文件')
                        os.remove(rm_file)
                        logger.info('清除文件完成')
            # shutil.rmtree(app_migrations_dir)
        return clean_files

    def write_migration_file(self, path, contents):
        """
        生成 migration 文件
        :param path: 文件路径
        :param contents: 文件内容
        """
        with open(path, 'w') as f:
            f.write(contents)

    def read_migration_file(self, path):
        """
        读取 migration 文件
        :param path: 文件路径
        :return: `str`
        """
        with open(path, 'r') as f:
            contents = f.read()
        return contents

    def update_app_migrations_dir_files_to_db(self, name):
        """
        【更新远程】更新指定 app 下的 migrations 目录文件到数据库
        :param name: app 名称
        """
        app_migrations_dir = self.get_app_migrations_dir(name)
        app_migrations_files = self.get_app_migrations_files(name)
        for a_m_file in app_migrations_files:
            amf_path = os.path.join(app_migrations_dir, a_m_file)
            if os.path.isfile(amf_path):
                logger.info('更新文件：{}'.format(amf_path))
                contents = self.read_migration_file(amf_path)
                data = {'app': name, 'name': a_m_file, 'contents': contents}
                self.add_django_cache_migrations_data(data=data)

    def get_app_migrations_from_db_cache(self, name):
        """
        【更新本地】从数据库缓存更新数据到本地 app 的 migrations 目录
        :param name: app 名称
        """
        app_migrations_dir = self.get_app_migrations_dir(name=name)
        # 清除本地旧文件
        logger.info('清除本地旧文件')
        self.clean_app_migrations_dir(name=name)
        django_cache_migrations_data = self.get_django_cache_migrations_to_app(name=name)
        for migration_data in django_cache_migrations_data:
            file_name = migration_data.get('name')
            file_contents = migration_data.get('contents')
            file_path = os.path.join(app_migrations_dir, file_name)
            # 新增本地文件
            logger.info('新增本地文件: {}'.format(file_path))
            self.write_migration_file(path=file_path, contents=file_contents)








