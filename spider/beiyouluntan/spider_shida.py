#!/usr/bin/env python
# -*- coding: utf8 -*-

import time
import json
import traceback
import datetime
import hashlib
import logging as L

from urllib.parse import urljoin

import requests
import lxml
from lxml import etree
import pymysql

L.basicConfig(level=L.DEBUG, format='[%(asctime)s] %(levelname)-8s %(message)s')


#g_ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
g_ua = 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.04'
headers = {'User-Agent': g_ua, 'x-requested-with': 'XMLHttpReQUest'}
user_info = {'id': 'onchanging', 'passwd': 'per525xucl'}
conn = pymysql.connect(host='rm-bp1q5lxw4ek0369kx2o.mysql.rds.aliyuncs.com',user='wap',passwd='1q2w3e4r',db='wap',port=3306, charset='utf8')
conn.ping(True)
cur=conn.cursor()


def login_bylt(url):
    try:
        session = requests.session()
        session.post(url, headers=headers, data=user_info, timeout=10, verify=False)
    except Exception:
        L.info('LOGIN_FAIL: %s' % traceback.format_exc())
        return
    else:
        L.info('LOGIN_SUCC')
        return session

def spider_bylt(session, url):
    if not session: return
    try:
        r = session.get(url, headers=headers, timeout=10, verify=False)
        text = r.text
    except Exception:
        L.info('SPIDER_FAIL: %s' % traceback.format_exc())
        return
    else:
        if r.status_code == 200:
            L.info('SPIDER_SUCC')
            return text
        else:
            L.info('SPIDER_ERR_CODE: url=%s\tcode=%s' % (url, r.status_code))
            return

def parse_bylt(url, text):
    if not text: return
    try:
        tree = etree.HTML(text)
        urls = tree.xpath('//li[@id="topten"]//li/a/@href')
    except Exception:
        L.info('PARSE_FAIL: %s' % traceback.format_exc())
        return
    else:
        L.info('PARSE_SUCC')
        urls = [urljoin(url, sub_url) for sub_url in urls]
        return urls

def spider_parse_shida(session, urls):
    items = []
    for url in urls:
        item = spider_parse_one(session, url)
        if not item: continue
        items.append(item)
    #for item in items:
        #print(item)
    return items

def spider_parse_one(session, url):
    _id, name, title, content, board, update_time = '', '', '', '', '', ''
    try:
        r = session.get(url, timeout=10, verify=False, headers=headers)
        text = r.text
        if r.status_code != 200:
            L.info('SPIDER_ERR_CODE: url=%s\tcode=%s' % (url, r.status_code))
            return
    except Exception:
        L.info('SPIDER_FAIL: url=%s\terr=%s' % (url, traceback.format_exc()))
        return

    try:
        tree = etree.HTML(text)
        user_id = tree.xpath('//div[@class="a-wrap corner"][1]//tr[@class="a-head"]/td/span[1]/a/text()')[0]
        user_name = tree.xpath('//div[@class="a-wrap corner"][1]//tr[@class="a-body"]//div[@class="a-u-uid"]/text()')[0]
        title = tree.xpath('//div[@class="a-wrap corner"][1]//div[@class="a-content-wrap"]/text()')[1]
        title = title.split('标\xa0\xa0题:')[1].strip()
        title = title.replace("'", "‘").replace('"', '“').strip()
        content = tree.xpath('//div[@class="a-wrap corner"][1]//div[@class="a-content-wrap"]')[0]
        content = content.xpath('string(.)').split('※ 来源:·北邮人论坛', 1)[0].rsplit('--', 1)[0].split('站内',)[1]
        content = content.replace("'", "‘").replace('"', '“').strip()
        #content = content.replace("'", "‘").replace('"', '“').replace('\xa0', ' ').strip()
        board = tree.xpath('//div[@class="a-wrap corner"][1]//div[@class="a-content-wrap"]/text()')[0]
        board = board.split('信区:')[1]
        update_time = tree.xpath('//div[@class="a-wrap corner"][1]//div[@class="a-content-wrap"]/text()')[2]
        update_time = update_time.split('(')[1].split(')')[0]
        create_time = datetime.datetime.strptime(update_time, "%a %b %d %H:%M:%S %Y") 
        m = hashlib.md5()
        m.update(''.join([user_id, title, content, update_time]).encode('utf8'))
        md = m.hexdigest()
        spider_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return md, user_id, user_name, title, content, board, create_time, spider_time
    except Exception:
        L.info('PARSE_FAIL: url=%s\terr=%s' % (url, traceback.format_exc()))
        return


def save_mysql(items):
    if len(items) < 10: return
    try:
        for item in items:
            #item_utf8 = [field.encode('utf8') if isinstance(field, (str, lxml.etree._ElementUnicodeResult)) else field for field in item]
            #md, user_id, user_name, title, content, board, create_time, spider_time = item_utf8
            md, user_id, user_name, title, content, board, create_time, spider_time = item
            md =  pymysql.escape_string(md)
            user_id = pymysql.escape_string(user_id)
            user_name = pymysql.escape_string(user_name)
            title = pymysql.escape_string(title)
            conten = pymysql.escape_string(content)
            board = pymysql.escape_string(board)
            sql = """INSERT IGNORE INTO beiyouluntan_top(md, user_id, user_name, title, content, board, create_time, spider_time) VALUES("%s","%s","%s","%s","%s","%s","%s","%s")""" % (md, user_id, user_name, title, content, board, create_time, spider_time) 
            cur.execute(sql)
            conn.commit()
    except Exception:
        L.info('MYSQL_FAIL: %s' % traceback.format_exc())


def main():
    login_url = 'https://bbs.byr.cn/user/ajax_login.json'
    spider_url = 'https://bbs.byr.cn/default?_uid=onchanging'
    session = login_bylt(login_url)
    text = spider_bylt(session, spider_url)
    urls = parse_bylt(spider_url, text)
    #print (urls)
    items = spider_parse_shida(session, urls)
    save_mysql(items)


if __name__ == '__main__':
    main()
