# coding = utf-8

"""
@author: sy

@file: sql_items.py

@time: 2018/11/15 21:14

@desc: 根据不同的需求定制不同类的自定义sql

"""


# 豆瓣自定义sql
class DouBanSqlItems(object):
    def get_select_sql(self):
        """ 查询评论的sql """
        select_comments = "SELECT t.short_comment from douban t"
        return select_comments
