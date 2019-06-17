# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy import Request
from urllib import parse
import sys
import os
import datetime
from ArticleSpider.items import JobBoleArticleItem
from ArticleSpider.utils.common import get_md5
from ArticleSpider.items import ArticleItemLoad

# from scrapy.loader import ItemLoader reason:这是scrapy自带的ItemLoad,注释掉不用,如果字段太多,用这种并不方便


sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    # start_urls = ['http://blog.jobbole.com/']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):

        """
        1. 获取文章列表的url进行解析
        2. 获取下一页的url并交给scrapy下载,完成后交给parse
        """
        # 解析列表页中的所有文章url并交给scrapy下载后解析
        post_nodes = response.css('#archive .floated-thumb .post-thumb a')
        for post_node in post_nodes:
            # 抓取所有列表的首页图片
            image_url = post_node.css('img::attr(src)').extract_first('')
            post_url = post_node.css('::attr(href)').extract_first('')

            # 通过yield 交给scrapy处理
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},
                          callback=self.parse_detail)

        # 提取下一页交给scrapy进行下载
        next_url = response.css('.next.page-numbers::attr(href)').extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    # 提取文章具体逻辑(文章详情)
    def parse_detail(self, response):

        """
        # 实例化一个jobboleitem
        article_item = JobBoleArticleItem()

        # 获取meta,获取到Request的封面图提取出来
        front_image_url = response.meta.get('front_image_url', '')

        --------------    css   案例 start    --------------
        # 标题  extract_first()防止数组越界
        article_title_css = response.css('div.entry-header h1::text').extract_first('')

        # 时间
        article_time_css = response.css('p.entry-meta-hide-on-mobile::text').extract_first('').strip().replace(
            '·', '').strip()

        # 点赞数
        article_praise_css = response.css('.vote-post-up h10::text').extract_first('')
        # 正则提取收藏数字
        match_article_praise_css = re.match('.*(\d+).*', article_praise_css)
        if match_article_praise_css:
            article_praise_css = int(match_article_praise_css.group(1))
        else:
            article_praise_css = 0

        # 收藏数
        bookmark_css = response.css(
            '.btn-bluet-bigger.href-style.bookmark-btn.register-user-only::text').extract_first('')
        # 正则提取收藏数字
        match_bookmark_css = re.match('.*(\d+).*', bookmark_css)
        if match_bookmark_css:
            article_bookmark_css = int(match_bookmark_css.group(1))
        else:
            article_bookmark_css = 0

        # 评论数
        comments_css = response.css('a[href="#article-comment"] span::text').extract_first('')
        match_comments_css = re.match('.*(\d+).*', comments_css)
        if match_comments_css:
            article_comments_css = int(match_comments_css.group(1))
        else:
            article_comments_css = 0
        # 文章详情
        article_contents_css = response.css('.entry').extract_first('')

        # 文章标签
        tag_list_css = response.css('p.entry-meta-hide-on-mobile a::text').extract()
        # 去重标签
        tag_list_css = [element for element in tag_list_css if not element.strip().endswith("评论")]
        tags_css = ','.join(tag_list_css)

        --------------    css   案例 end    --------------

        article_item["title"] = article_title_css
        # 将字符串时间转为日期
        try:
            article_time_css = datetime.datetime.strptime(article_time_css, '%Y/%m%d').date()
        except Exception as e:
            article_time_css = datetime.datetime.now().date()
        article_item["create_date"] = article_time_css
        article_item["url"] = response.url
        article_item["url_object_id"] = get_md5(response.url)
        article_item["front_image_url"] = [front_image_url]
        article_item["praise_nums"] = article_praise_css
        article_item["comments_nums"] = article_comments_css
        article_item["fav_nums"] = article_bookmark_css
        article_item["tags"] = tags_css
        article_item["content"] = article_contents_css
        """

        ''' 通过item_loader加载item,目的：比原来的item便于维护 start'''
        # 获取meta,获取到Request的封面图提取出来
        front_image_url = response.meta.get('front_image_url', '')
        item_loader = ArticleItemLoad(item=JobBoleArticleItem(), response=response)
        item_loader.add_css("title", "div.entry-header h1::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("create_date", 'p.entry-meta-hide-on-mobile::text')
        item_loader.add_value("front_image_url", [front_image_url])
        item_loader.add_css("praise_nums", '.vote-post-up h10::text')
        item_loader.add_css("comments_nums", 'a[href="#article-comment"] span::text')
        item_loader.add_css("fav_nums", '.btn-bluet-bigger.href-style.bookmark-btn.register-user-only::text')
        item_loader.add_css("tags", 'p.entry-meta-hide-on-mobile a::text')
        item_loader.add_css("content", '.entry')

        # 必须调用此步骤
        article_item = item_loader.load_item()
        ''' 通过item_loader加载item,目的：比原来的item便于维护 end'''

        yield article_item
