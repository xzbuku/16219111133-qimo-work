# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import datetime
import re

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def add_jobbole(value):
    return value + '-suyu'


def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, '%Y%m%d').date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date


# 自定义ItemLoad,重载scrapy自带的ItemLoader
class ArticleItemLoad(ItemLoader):
    default_output_processor = TakeFirst()


# 正则提取收藏数字
def get_nums(value):
    match_re = re.match('.*(\d+).*', value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


# tags标签里,去掉提取的评论
def remove_comment_tags(value):
    if "评论" in value:
        return ""
    else:
        return value


def return_value(value):
    return value


# 自定义文章Item
class JobBoleArticleItem(scrapy.Item):
    """
    title = scrapy.Field(
        # 传入item时做的预处理参数
        input_processor=MapCompose(lambda x: x + '-jobbole', add_jobbole)
    )
    """
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert),
        # 此处注释,因为用到了自定义的ItemLoad,里面已经写了输出时的规范,list取出第一行
        # output_processor=TakeFirst()
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(
        # 因为front_image_url返回必须是list,所以不能用ArticleItemLoad中的output_processor
        output_processor=MapCompose(return_value)
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comments_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(",")
    )
    content = scrapy.Field()

    def get_insert_bole_sql(self):
        insert_sql = """
                            INSERT INTO jobbole_article (title,create_time,url,url_obejct_id,front_image_url,
                            comment_nums,fav_nums,parise_nums,tags,content) 
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        """

        params = (
            self['title'], self['create_date'], self['url'],
            self['url_object_id'], self['front_image_url'],
            self['comments_nums'], self['fav_nums'], self['praise_nums'],
            self['tags'], self['content']
        )
        return insert_sql, params


# 自定义ItemLoad,重载scrapy自带的ItemLoader
class LaGouItemLoad(ItemLoader):
    default_output_processor = TakeFirst()


def remove_splash(value):
    """ 去掉工作城市的/ """
    return value.replace('/', '').replace(' ', '')


def handle_addr(value):
    """ 清理工作地点的值 """
    addr_list = value.split('\n')
    addr_list = [item.strip() for item in addr_list if item.strip() != '查看地图']
    return ''.join(addr_list)


SQL_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class LaGouItem(scrapy.Item):
    """ 拉钩网对应入库scrapy字段 """
    url = scrapy.Field()  # 拉钩url地址
    url_object_id = scrapy.Field()  # url的hashid
    title = scrapy.Field()  # 招聘标题
    salary = scrapy.Field()  # 薪资
    job_city = scrapy.Field(  # 工作城市
        input_processor=MapCompose(remove_splash),  # MapCompose,可以对传入的字段进入函数处理
    )
    work_years = scrapy.Field(  # 工作年限
        input_processor=MapCompose(remove_splash),
    )
    degree_need = scrapy.Field(  # 学历要求
        input_processor=MapCompose(remove_splash),
    )
    job_type = scrapy.Field()  # 工作类型(全职/兼职)
    publish_time = scrapy.Field()  # 发布时间
    tags = scrapy.Field(  # 工作标签
        input_processor=Join(',')
    )
    job_advantage = scrapy.Field()  # 福利待遇
    job_desc = scrapy.Field()  # 工作描述
    job_addr = scrapy.Field(  # 工作地点
        input_processor=MapCompose(remove_tags, handle_addr),
    )
    company_url = scrapy.Field()  # 公司网址url
    company_name = scrapy.Field()  # 公司名称
    crawl_time = scrapy.Field()  # 抓取时间
    crawl_update_time = scrapy.Field()  # 更新时间

    def get_insert_sql(self):
        insert_lagou_sql = """
            insert into lagou_job(url,url_object_id,title,salary,job_city,
            work_years,degree_need,job_type,publish_time,tags,job_advantage,
            job_desc,job_addr,company_url,company_name,crawl_time)
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE salary=VALUES(salary),job_desc=VALUES(job_desc)
        """

        params = (
            self['url'], self['url_object_id'], self['title'], self['salary'], self['job_city'],
            self['work_years'], self['degree_need'], self['job_type'], self['publish_time'], self['tags'],
            self['job_advantage'], self['job_desc'], self['job_addr'], self['company_url'], self['company_name'],
            self['crawl_time'].strftime(SQL_DATETIME_FORMAT),
        )

        return insert_lagou_sql, params


# 自定义ItemLoad,重载scrapy自带的ItemLoader
class DouBanItemLoad(ItemLoader):
    default_output_processor = TakeFirst()


def handler_time(value):
    """ 处理时间格式，数据清理时间 """
    date_str = value.strip().replace('\n','')
    return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

def handler_votes(value):
    return int(value)

class DouBanItem(scrapy.Item):
    douban_url = scrapy.Field()  # 地址
    url_hashid = scrapy.Field()  # 唯一值
    user_name = scrapy.Field()  # 用户名
    is_view = scrapy.Field()  # 是否看过电影
    star_number = scrapy.Field()  # 评价星级
    comment_time = scrapy.Field(
        input_processor = MapCompose(handler_time)
    )  # 评价日期
    votes_numbers = scrapy.Field(
        input_processor = MapCompose(handler_votes)
    )  # 投票数,有用
    short_comment = scrapy.Field()  # 段评论



    def get_insert_sql(self):
        insert_douban_sql = """
            insert into douban(url_hashid,douban_url,user_name,is_view,star_number,
            comment_time,votes_numbers,short_comment)
            values (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        params = (
            self['url_hashid'], self['douban_url'], self['user_name'], self['is_view'], self['star_number'],
            self['comment_time'], self['votes_numbers'], self['short_comment']
        )

        return insert_douban_sql, params
