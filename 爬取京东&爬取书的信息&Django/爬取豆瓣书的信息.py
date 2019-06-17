import requests
# from bs4 import BeautifulSoup
import MySQLdb
from lxml import etree


conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='test2', charset='utf8')

cur = conn.cursor()

link = 'https://movie.douban.com/top250'
headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT6.1; enUS; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
r = requests.get(link, headers=headers)
res = requests.get(link)
tree = etree.HTML(res.text)
top250 = tree.xpath('//span[@class="title"][2]/text()')


for eachone in top250:
    title = eachone
    print(title)
    url = link
    print("INSERT INTO urls (url, content) VALUES (\"%s\", \"%s\")" % (url, title))
    cur.execute("INSERT INTO urls (url, content) VALUES (\"%s\", \"%s\")", (url, title))

cur.close()
conn.commit()
conn.close()
