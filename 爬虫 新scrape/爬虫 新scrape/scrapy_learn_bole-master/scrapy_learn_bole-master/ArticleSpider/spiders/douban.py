# -*- coding: utf-8 -*-
from urllib import parse

import scrapy
from scrapy import Request

from items import DouBanItem, DouBanItemLoad
from utils.common import get_md5


class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["movie.douban.com"]
    start_urls = ['https://movie.douban.com/subject/24852545/comments']

    # start_urls = ['https://movie.douban.com/review/best/']

    def parse(self, response):
        """ 交给parse_details 进行处理 """
        yield Request(url=response.url, callback=self.parse_details, dont_filter=True)

        # 提取下一页交给scrapy进行下载
        next_page = response.css('.next::attr(href)').extract_first('')
        if next_page:
            yield Request(url=parse.urljoin(response.url, next_page), callback=self.parse)

    def parse_details(self, response):
        """ 解析爱情公寓具体短评论 """
        # i = str(response.meta.get('comments_iter_nums', '') + 1) 先注释此参数
        for i in range(len(response.css('.mod-bd .comment-item'))):
            item_loader = DouBanItemLoad(item=DouBanItem(), response=response)
            item_loader.add_xpath('douban_url', f'//*[@id="comments"]/div[{i+1}]/div[2]/h3/span[2]/a/@href')
            user_url = response.xpath(f'//*[@id="comments"]/div[{i+1}]/div[2]/h3/span[2]/a/@href').extract_first('')
            item_loader.add_value('url_hashid', get_md5(user_url))
            item_loader.add_xpath('user_name', f'//*[@id="comments"]/div[{i+1}]/div[2]/h3/span[2]/a/text()')
            item_loader.add_xpath('is_view', f'//*[@id="comments"]/div[{i+1}]/div[2]/h3/span[2]/span[1]/text()')
            item_loader.add_xpath('star_number', f'//*[@id="comments"]/div[{i+1}]/div[2]/h3/span[2]/span[2]/@title')
            item_loader.add_xpath('comment_time', f'//*[@id="comments"]/div[{i+1}]/div[2]/h3/span[2]/span[3]/text()')
            item_loader.add_xpath('votes_numbers', f'//*[@id="comments"]/div[{i+1}]/div[2]/h3/span[1]/span/text()')
            item_loader.add_xpath('short_comment', f'//*[@id="comments"]/div[{i+1}]/div[2]/p/span/text()')
            # 必须调用此步骤
            douban_item = item_loader.load_item()
            ''' 通过item_loader加载item,目的：比原来的item便于维护 end'''

            yield douban_item
