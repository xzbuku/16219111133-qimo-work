# coding = utf-8

"""
@author: sy

@file: common.py

@time: 2018/6/30 16:50

@desc: 工具类

"""
import hashlib


# 将url转化为MD5长度的唯一标识
def get_md5(url):
    if isinstance(url, str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


if __name__ == '__main__':
    print(get_md5('http://blog.jobbole.com/all-posts/'))
