# -*- coding: utf-8 -*-

import os
import sys

import pandas as pd
import redis
from loguru import logger
from pymongo import MongoClient
from redis.sentinel import Sentinel
from sqlalchemy import create_engine


class MysqlTools(object):
    """
    MySQL数据库工具类
    """

    def __init__(self, host, port, username, password, dbname):
        """
        指定所处环境及数据库名称
        :param host: 主机地址
        :param port: 主机端口
        :param username: 用户
        :param password: 密码
        """
        self.mysql_engine = create_engine(
            "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(username, password, host, port, dbname))

    @property
    def mysql(self):
        """
        返回MySql会话
        :return:
        """
        return self.mysql_engine

    def update_string(self, update_sql):
        """
        更新语句操作
        :param update_sql: 更新SQL
        :return:
        """
        update_result = self.mysql_engine.execute(update_sql)
        return update_result.rowcount

    def delete_string(self, delete_sql):
        """
        删除语句操作
        :param delete_sql: 删除SQL
        :return:
        """
        delete_result = self.mysql_engine.execute(delete_sql)
        return delete_result.rowcount

    def query_string(self, script_str):
        """
        通过sqlalchemy并使用engine方式执行脚本(字符串)并返回结果
        :param script_str: 脚本字符串
        :return:
        """
        try:
            result = self.mysql_engine.execute(script_str).fetchall()
            return result
        except Exception:
            logger.exception("[Exception]：执行MySQL脚本过程中发生异常，请检查！~ 脚本为：【{}】".format(script_str))

    def query_file(self, script_file):
        """
        通过sqlalchemy并使用engine方式执行脚本(文本文件)并返回结果
        :param script_file: 脚本文件
        :return:
        """
        script_string = None
        try:
            if os.path.exists(script_file):
                with open(script_file, mode=r'r', encoding='utf-8') as script:
                    script_string = script.read()
                    result = self.mysql_engine.execute(script_string).fetchall()
                    return result
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            logger.exception('[Exception]：MySQL脚本文件"{}"当前并不存在'.format(script_file))
        except Exception:
            logger.exception("[Exception]：执行MySQL脚本过程中发生异常，请检查！~ 脚本为：【{}】".format(script_string))

    def query_string_df(self, script_str, index_col=None, columns=None, chunksize=None):
        """
        通过sqlalchemy并使用read_sql方式执行脚本(字符串)并返回结果
        :param script_str: 脚本字符串
        :param index_col: 将指定列作为索引
        :param columns: 指定获取列(read_sql_table时候可用)
        :param chunksize: 缓存区大小
        :return:
        """
        try:
            result = pd.read_sql(script_str, con=self.mysql_engine, index_col=index_col, columns=columns,
                                 chunksize=chunksize)
            return result
        except Exception:
            logger.exception("[Exception]：执行MySQL脚本过程中发生异常，请检查！~ 脚本为：【{}】".format(script_str))

    def query_file_df(self, script_file, index_col=None, chunksize=None):
        """
        通过sqlalchemy并使用read_sql_query方式执行脚本文件并返回结果
        :param script_file: 脚本文件
        :param index_col: 将指定列作为索引
        :param chunksize: 缓存区大小
        :return:
        """
        script_string = None
        try:
            if os.path.exists(script_file):
                with open(script_file, mode=r'r', encoding='utf-8') as script:
                    script_string = script.read()
                    result = pd.read_sql_query(script_string, con=self.mysql_engine, index_col=index_col,
                                               chunksize=chunksize)
                    return result
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            logger.exception('[Exception]：MySQL脚本文件"{}"当前并不存在'.format(script_file))
        except Exception:
            logger.exception("[Exception]：执行MySQL脚本过程中发生异常，请检查！~ 脚本为：【{}】".format(script_string))


class MongoTools(object):
    """
    MongoDB数据库工具类
    """

    def __init__(self, host, port, dbname, auth_dict=None):
        """
        指定所处环境及数据库名称
        :param host: 主机地址
        :param port: 主机端口
        :param dbname: 数据库名称
        :param auth_dict: 授权字典，样例格式为{"auth_db":"admin", "auth_username":"root", "auth_password":"123456"}
        """
        self.mongodb = MongoClient(host=host, port=port)
        if auth_dict is not None:
            if isinstance(auth_dict, dict):
                auth_db = auth_dict.get("auth_db")
                auth_username = auth_dict.get("auth_username")
                auth_password = str(auth_dict.get("auth_password"))
                auth = eval("self.mongodb.{}".format(auth_db))
                auth.authenticate(auth_username, auth_password)
                self.db_client = eval("self.mongodb.{}".format(dbname))
            else:
                logger.warning("auth_dict授权信息必须为字典形式，请检查！")
                sys.exit(1)

    def db(self, dbname=None):
        """
        获取MongoDB数据库会话
        :param dbname: 数据库名称
        :return:
        """
        if dbname is None:
            return self.DbClient(db_client=self.db_client)
        else:
            db_client = eval("self.mongodb.{}".format(dbname))
            return self.DbClient(db_client=db_client)

    @property
    def mongo(self):
        """
        获取MongoDB实例
        :return:
        """
        return self.mongodb

    class DbClient:
        """
        MongoDB数据库操作
        """

        def __init__(self, db_client):
            """
            初始化MongoDB数据库实例
            :param db_client: MongoDB数据库实例
            """
            self.db_client = db_client

        @property
        def client(self):
            """
            获取MongoDB数据库实例
            :return:
            """
            return self.db_client

        def drop(self, tbname):
            """
            删除指定表
            :param tbname: MongoDB表名
            :return:
            """
            tb = eval("self.db_client.{}".format(tbname))
            drop = tb.drop()
            return drop

        def insert_one(self, tbname, insert_json):
            """
            单条数据插入
            :param tbname: MongoDB表名
            :param insert_json: 单条插入json, 最好指定_id否则可能重复插入
            :return: 插入数据id
            """
            tb = eval("self.db_client.{}".format(tbname))
            insert = tb.insert_one(insert_json)
            return insert.inserted_id

        def insert_many(self, tbname, insert_json_list):
            """
            批量数据插入
            :param tbname: MongoDB表名
            :param insert_json_list: 批量插入json列表，最好指定_id否则可能重复插入
            :return: 插入数据id列表
            """
            tb = eval("self.db_client.{}".format(tbname))
            insert = tb.insert_many(insert_json_list)
            return insert.inserted_ids

        def delete_one(self, tbname, delete_json):
            """
            删除匹配到的第一条数据
            :param tbname: MongoDB表名
            :param delete_json: 删除数据json, _id必须用ObjectId("5ff2c39364efd65eed78597e")方式
            :return: 删除数据id
            """
            tb = eval("self.db_client.{}".format(tbname))
            delete = tb.delete_one(delete_json)
            return delete.deleted_count

        def delete_many(self, tbname, delete_json):
            """
            删除多条数据
            :param tbname: MongoDB表名
            :param delete_json: 删除数据json，若为{}则删除集合全部数据, _id必须用ObjectId("5ff2c39364efd65eed78597e")方式
            :return: 删除数据id
            """
            tb = eval("self.db_client.{}".format(tbname))
            delete = tb.delete_many(delete_json)
            return delete.deleted_count

        def update_one(self, tbname, filter_json, update_json, upsert=False):
            """
            更新匹配到的第一条数据
            :param tbname: MongoDB表名
            :param filter_json: 过滤json, _id必须用ObjectId("5ff2c39364efd65eed78597e")方式
            :param update_json: 更新json
            :param upsert: 更新插入开关
            :return:
            """
            tb = eval("self.db_client.{}".format(tbname))
            update = tb.update_one(filter=filter_json, update=update_json, upsert=upsert)
            return update.modified_count

        def update_many(self, tbname, filter_json, update_json, upsert=False):
            """
            更新多条数据
            :param tbname: MongoDB表名
            :param filter_json: 过滤json, _id必须用ObjectId("5ff2c39364efd65eed78597e")方式
            :param update_json: 更新json
            :param upsert: 更新插入开关
            :return:
            """
            tb = eval("self.db_client.{}".format(tbname))
            update = tb.update_many(filter=filter_json, update=update_json, upsert=upsert)
            return update.modified_count

        def find_one(self, tbname, filter_json=None, projection_json=None, sort_json={}, skip=0, limit=0):
            """
            查询匹配到的第一条数据
            :param tbname: MongoDB表名
            :param filter_json: 过滤json, _id必须用ObjectId("5ff2c39364efd65eed78597e")方式
            :param projection_json: 显示json
            :param sort_json: 排序json
            :param skip: 跳过行数
            :param limit: 限制行数
            :return:
            """
            tb = eval("self.db_client.{}".format(tbname))
            result = tb.find_one(filter=filter_json, projection=projection_json, sort=list(sort_json.items()),
                                 skip=skip,
                                 limit=limit)
            if result is not None:
                if result.__contains__("_id"):
                    result['_id'] = str(result['_id'])
            return result

        def find(self, tbname, filter_json=None, projection_json=None, sort_json={}, skip=0, limit=0):
            """
            查询多条数据
            :param tbname: MongoDB表名
            :param filter_json: 过滤json, _id必须用ObjectId("5ff2c39364efd65eed78597e")方式
            :param projection_json: 显示json
            :param sort_json: 排序json
            :param skip: 跳过行数
            :param limit: 限制行数
            :return:
            """
            result = []
            tb = eval("self.db_client.{}".format(tbname))
            items = tb.find(filter=filter_json, projection=projection_json, sort=list(sort_json.items()), skip=skip,
                            limit=limit)
            for item in items:
                if item.__contains__("_id"):
                    item['_id'] = str(item['_id'])
                result.append(item)
            return result


class RedisTools(object):
    """
    Redis数据库工具类
    """

    def __init__(self, host, port, dbname, password=None):
        """
         指定所处环境及数据库名称
         :param host: 主机地址
         :param port: 主机端口
         :param dbname: 数据库名称
         :param password: 密码
         """
        pool = redis.ConnectionPool(host=host, port=port, password=password, db=dbname, decode_responses=True)
        self.redisSession = redis.StrictRedis(connection_pool=pool, charset='utf-8')

    @property
    def redis(self):
        """
        获取redis实例
        :return:
        """
        return self.redisSession


class RedisSentinelTools(object):
    def __init__(self, service, password, instances):
        """
        Sentinel哨兵模式配置
        :param service: sentinel服务名称
        :param password: sentinel服务密码
        :param instances: sentinel实例，入参形式如[(host1,port1),(host2,port2)]
        """
        self._service = service
        self._password = password
        self._instances = instances
        self.sentinelSession = Sentinel(sentinels=self._instances, socket_timeout=0.5)

    @property
    def sentinel(self):
        """
        获取sentinel实例
        :return:
        """
        return self.sentinelSession

    def discover_master(self, service_name=None):
        """
        获取Redis主服务器地址
        :param service_name: 主服务名称
        :return:
        """
        return self.sentinelSession.discover_master(
            service_name=self._service if service_name is None else service_name)

    def discover_slaves(self, service_name=None):
        """
        获取Redis从服务器地址
        :param service_name：主服务名称
        :return:
        """
        return self.sentinelSession.discover_slaves(
            service_name=self._service if service_name is None else service_name)

    def master_instance(self, dbname, service_name=None, password=None):
        """
        获取主服务器实例，用于操作redis
        :param dbname: 数据库名称
        :param service_name: 主服务名称
        :param password: 主服务密码
        :return:
        """
        return self.sentinelSession.master_for(service_name=self._service if service_name is None else service_name,
                                               password=self._password if password is None else password,
                                               db=dbname)

    def slave_instance(self, dbname, service_name=None, password=None):
        """
        获取从服务器实例，用于操作redis
        :param dbname: 数据库名称
        :param service_name: 主服务名称
        :param password: 主服务密码
        :return:
        """
        return self.sentinelSession.slave_for(service_name=self._service if service_name is None else service_name,
                                              password=self._password if password is None else password,
                                              db=dbname)
