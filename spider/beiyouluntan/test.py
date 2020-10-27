#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Michael Xu'

"""
爬虫北邮论坛
"""

import requests
from lxml import etree
from urllib.parse import urljoin
import threading

import logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)-8s %(message)s')


user_agent = 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.04'
headers = {'User-Agent': user_agent, 'x-requested-with': 'XMLHttpRequest'}
my_header = {'x-requested-with': 'XMLHttpRequest',  # 该header不能缺
                 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}


def spider_url_content(session, url):
    r = session.get(url, headers=my_header, timeout=5)
    tree = etree.HTML(r.content.decode('gbk'))
    author = tree.xpath('//div[@class="a-wrap corner"][1]//tr[@class="a-head"]/td/span[1]/a/text()')[0]
    user_id = tree.xpath('//div[@class="a-wrap corner"][1]//tr[@class="a-body"]//div[@class="a-u-uid"]/text()')[0]
    update_time = tree.xpath('//div[@class="a-wrap corner"][1]//div[@class="a-content-wrap"]/text()')[2]
    update_time = update_time.split('(')[1].split(')')[0]
    board = tree.xpath('//div[@class="a-wrap corner"][1]//div[@class="a-content-wrap"]/text()')[0]
    board = board.split('信区:')[1]
    title = tree.xpath('//div[@class="a-wrap corner"][1]//div[@class="a-content-wrap"]/text()')[1]
    title = title.split('标\xa0\xa0题:')[1]
    content = tree.xpath('//div[@class="a-wrap corner"][1]//div[@class="a-content-wrap"]')[0]
    content = content.xpath('string(.)')
    print(user_id, author, update_time, board, title, content)


# 模拟登陆北邮论坛，爬取十大内容
def get_shida_url():
    # 这个不是真正请求的url
    # spider_url = 'https://bbs.byr.cn/'
    spider_url = 'https://bbs.byr.cn/default?_uid=onchanging'
    login_url = 'https://bbs.byr.cn/user/ajax_login.json'
    data = {'id': 'onchanging', 'passwd': 'per525xucl'}
    session = requests.session()
    # headers的问题还是很重要的
    session.post(login_url, headers=headers, data=data)
    r = session.get(spider_url, headers=headers)
    tree = etree.HTML(r.text)
    urls = tree.xpath('//li[@id="topten"]//li/a/@href')
    base_url = spider_url
    url_l = [urljoin(base_url, url) for url in urls]
    return session, url_l


def test():
    session, url_l = get_shida_url()
    threads_l = []
    for url in url_l:
        print(url)
        t = threading.Thread(target=spider_url_content, args=(session, url))
        threads_l.append(t)
        break

    for t in threads_l:
        t.start()
        t.join()


if __name__ == '__main__':
    test()

