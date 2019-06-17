# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
# 文件操作的库,编码比普通的with open要好用
import codecs
import json
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi
import pymysql
import pymysql.cursors


class ArticleSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    # 自定义json文件的导出
    def __init__(self):
        # 打开json文件,进行写入操作
        self.file = codecs.open('article.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        # 将item转为字典格式在转成str类型的 json格式
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def spider_close(self, spider):
        self.file.close()


"""
spider解析速度超过入库速度,此种方法插入速度太慢,跟不上解析速度,commit时会阻塞
所以不用此种方法 MysqlPipeline
"""


class MysqlPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect('127.0.0.1', 'root', '', 'article_spider', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            INSERT INTO jobbole_article (title,create_time,url,url_obejct_id,front_image_url,
            comment_nums,fav_nums,parise_nums,tags,content) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql, (item['title'], item['create_date'], item['url'],
                                         item['url_object_id'], item['front_image_url'],
                                         item['comments_nums'], item['fav_nums'], item['praise_nums'],
                                         item['tags'], item['content']))
        self.conn.commit()


"""
使用Twisted异步框架,进行mysql的连接,
Twisted本身不提供链接,只是提供了异步容器,mysql链接还是需要自己完成
"""


class MysqlTwistedPipeline(object):
    def __init__(self, db_pool):
        self.db_pool = db_pool

    # 声明函数,scrapy会将settings的文件内容读取进来
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

    # 使用Twisted 将mysql插入变成异步操作
    def process_item(self, item, spider):
        query = self.db_pool.runInteraction(self.do_insert, item)
        # 添加自己的处理异常的函数
        query.addErrback(self.handle_error, item, spider)

    # 处理插入异常
    def handle_error(self, failure, item, spider):
        print(failure)

    # 执行具体的插入逻辑
    def do_insert(self, cursor, item):
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)


class JsonExporterPipeline(object):
    # 调用scrapy 提供的json export 导出json文件
    def __init__(self):
        self.file = open('articleexporter.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class ArticleImagePipeline(ImagesPipeline):
    # 重写该方法可从result中获取到图片的实际下载地址
    def item_completed(self, results, item, info):
        image_file_path = ''
        if "front_image_url" in item:
            for ok, value in results:
                image_file_path = value["path"]
            item['front_image_path'] = image_file_path
        return item
