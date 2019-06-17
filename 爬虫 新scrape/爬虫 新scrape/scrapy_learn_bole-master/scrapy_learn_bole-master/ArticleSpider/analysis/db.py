# coding = utf-8

"""
@author: sy

@file: db.py

@time: 2018/11/15 21:08

@desc: 自定义脱离scrapy 数据库模块

"""

import pymysql
from twisted.enterprise import adbapi


class MysqlDb(object):
    def __init__(self, db_pool):
        self.db_pool = db_pool

    # 声明函数,上层调用scrapy自带utils模块，将settings的文件内容读取进来
    @classmethod
    def from_settings(cls, settings):
        # 将settings中的参数作为dict传入连接池中,dict的key需要和pymysql的Connection对应
        db_params = dict(
            host=settings['MYSQL_HOST'],
            database=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )

        db_pool = adbapi.ConnectionPool('pymysql', **db_params)
        return cls(db_pool)

    # 使用Twisted 将mysql变成异步操作，第一种方式，此方式可以自定义操作，增删改查都可以
    def process_item_interaction(self, item):
        query = self.db_pool.runInteraction(self.do_select, item)
        # 添加自己的处理异常的函数
        query.addErrback(self.handle_error)
        return query

    # 处理执行异常打印踹
    def handle_error(self, failure):
        print(failure)

    # 执行具体自定义的执行sql逻辑
    def do_select(self, cursor, item):
        select_sql = item.get_select_sql()
        cursor.execute(select_sql)
        return cursor.fetchall()

    # 使用Twisted 将mysql变成异步操作,第二种方式查询方式！
    def process_item_query(self, item):
        query = self.db_pool.runQuery(item.get_select_sql())
        # 添加自己的处理异常的函数
        query.addErrback(self.handle_error)
        return query

