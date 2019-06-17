# coding = utf-8

"""
@author: sy

@file: requests_cookies_zhihu.py

@time: 2018/8/12 22:19

@desc: requests 模拟知乎cookies 登录

"""
# 登录后保存cookie到本地
try:
    import cookielib
except:
    import http.cookiejar as cookielib
import requests

s = requests.session()
s.cookies = cookielib.LWPCookieJar(filename="cookies.txt")
try:
    s.cookies.load(ignore_discard=True)
except BaseException:
    print ("cookie未能加载")
    
def login(username,password):

    url = 'https://www.zhihu.com/api/v3/oauth/sign_in'

