# coding = utf-8

"""
@author: sy

@file: main.py

@time: 2018/6/18 17:46

@desc: debug 's Tips

"""
from scrapy.cmdline import execute

import sys
import os

from analysis.analysis_data import AnalysisData

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy", "crawl", "douban"])


if __name__ == '__main__':
    analysisData = AnalysisData()