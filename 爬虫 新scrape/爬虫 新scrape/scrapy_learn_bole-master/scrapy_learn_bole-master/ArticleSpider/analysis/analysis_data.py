# coding = utf-8

"""
@author: sy

@file: analysis_data.py

@time: 2018/11/15 20:36

@desc: 对爬取下来的数据进行数据分析统计

"""
import jieba.analyse
import wordcloud
import pyecharts
from scrapy.utils.project import get_project_settings

from analysis.sql_items import DouBanSqlItems
from .db import MysqlDb
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS

from twisted.internet import reactor


class AnalysisData(object):
    def __init__(self):
        """ 初始化获取mysql数据库中的相对数据"""
        self.word_dict = {}
        setting = get_project_settings()
        mysqlDb = MysqlDb.from_settings(setting)
        douBanSqlItems = DouBanSqlItems()
        query_result = mysqlDb.process_item_interaction(douBanSqlItems)
        query_result.addCallback(self.word_count)
        reactor.run()

    def word_count(self, data):
        """
        词频统计分析
        :param data: mysql传过来的数据，短评论
        :return:
        """
        if data:
            word_list = [data_dict['short_comment'] for data_dict in data]
            short_comments = ';'.join(word_list)
            """ 暂时注释掉"""
            tags = jieba.analyse.extract_tags(short_comments, topK=100, withWeight=True)
            for tag, n in tags:
                # tag : 权重较高的词 ; n权重值
                # 调试用的注释print(f'{tag} {str(int(n*10000))}' )
                self.word_dict[tag] = int(n * 10000)
            reactor.stop()

    def draw_picture(self):
        d = os.path.dirname(__file__)
        alice_mask = np.array(Image.open(os.path.join(d, "xin1.jpg")))

        wc = WordCloud(font_path='C:/Windows/Fonts/STKAITI.TTF',  # 设置字体格式
                       mask=alice_mask,  # 设置背景图
                       background_color='white',
                       max_words=400,  # 最多显示词数
                       max_font_size=150  # 字体最大值)
                       )
        wc.generate_from_frequencies(self.word_dict)  # 从字典生成词云
        image_colors = wordcloud.ImageColorGenerator(alice_mask)  # 从背景图建立颜色方案
        wc.recolor(color_func=image_colors)  # 将词云颜色设置为背景图方案
        plt.imshow(wc,interpolation='bilinear')  # 显示词云
        plt.axis('off')  # 关闭坐标轴
        plt.show()  # 显示图像
        pass
