
# -*- coding: utf-8 -*-
from app import config
from app import logsql as log

class sqliteDB(object):

    def __init__(self):
        return

    def connect(self):
        import sqlite3, os, platform
        path = os.getcwd()
        if platform.system() == 'Windows':
            path += '\\'
        else:
            path += '/'

        # change root password to yours:
        conn = sqlite3.connect(path + config.sqliteFile)
        return conn

    def search(self, sql):
        log.log().logger.info(sql)
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        values = cursor.fetchall()
        # log.log().logger.info('values:',values)
        cursor.close()
        conn.close()
        return values

    def insert(self, sql):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        log.log().logger.info(sql)
        cursor.close()
        try:
            conn.commit()
        except :
            log.log().logger.info('commit error')
        conn.close()


class mysqlDB(object):

    def __init__(self):
        return

    def connect(self):
        # change root password to yours:
        import mysql.connector
        conn = mysql.connector.connect(host=config.db_host, port=config.db_port, user=config.db_user, password=config.db_password, database=config.database,
                              auth_plugin='mysql_native_password')
        return conn

    def search(self, sql):
        conn = self.connect()
        cursor = conn.cursor()
        # log.log().logger.info(sql)
        cursor.execute(sql)
        values = cursor.fetchall()
        # log.log().logger.info('values1 :', values)
        cursor.close()
        conn.close()
        return values

    def insert(self, sql):
        log.log().logger.debug(sql)
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        cursor.close()
        try:
            conn.commit()
        except :
            log.log().logger.error('commit error')
        conn.close()

    def excutesql(self, sql):
        log.log().logger.debug(sql)
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        cursor.close()
        try:
            conn.commit()
        except:
            log.log().logger.error('commit error')
        conn.close()

    # 测试查询，防止sql注入
    def searchsql(self, sql, args):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(sql, args)
        values = cursor.fetchall()
        cursor.close()
        return values

class useDB(object):

    def __init__(self):
        self.DBtype = config.DBtype
        return

    def insert(self,sql):
        if self.DBtype == '1':
            sqliteDB().insert(sql)
        else:
            mysqlDB().insert(sql)

    def search(self,sql):
        if self.DBtype == '1':
            return sqliteDB().search(sql)
        else:
            return mysqlDB().search(sql)

    def searchsql(self, sql,args):
        if self.DBtype == '1':
            return sqliteDB().search(sql)
        else:
            return mysqlDB().searchsql(sql,args)