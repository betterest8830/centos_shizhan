#!/usr/bin/env python
# coding=utf8

import os, sys
import requests
import time
import datetime
from lxml import etree
import traceback
import random
import logging as L
import queue
import multiprocessing
import threading
from urllib.parse import urljoin
from urllib.parse import urlsplit
import re


L.basicConfig(level=L.INFO, format='[%(asctime)s] %(levelname)-8s %(message)s')


g_ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
headers = {'User-Agent': g_ua}
proxies=None
max_level=1

seed_d = set()
book_d = set()
pat=re.compile(r'http[s]{0,1}://book\.qidian\.com/info/\\d+')


def get_book(seed_q, text_q):
    while True:
        url, level = seed_q.get(True)
        L.info('SEED_SIZE_OUT: %s' % seed_q.qsize())
        if url == None: break
        try:
            r = requests.get(url, verify=False, proxies=proxies, headers=headers, timeout=20)
        except Exception:
            L.info('GET_ERR: %s\t%s' % (url, traceback.format_exc()))
            continue
        text_q.put((r, level), block=True)
        L.info('TEXT_SIZE_IN: %s' % text_q.qsize())


def parse_text(seed_q, text_q):
    while True:
        r, level = text_q.get(True)
        L.info('TEXT_SIZE_OUT: %s' % text_q.qsize())
        if level > max_level:
            L.info('break')
            break
        if level == max_level:
            seed_q.put((None, level+1), block=True)
            continue
        parent_url, text = r.url, r.text
        tree = etree.HTML(text)
        for url in tree.xpath(u"//a/@href"):
            url = url.strip()
            if not url: continue
            if 'javascript' in url: continue
            if '#' in url: continue
            url = urljoin(parent_url, url)
            if url in seed_d: continue
            if 'book.qidian.com' not in url:
                continue
            seed_d.add(url)
            L.info('SEED_INFO: %s\t%s' % (url, level+1))
            if pat.match(url):
                L.info('BOOK_URL: %s' % url)
                book_d.add(url)
            seed_q.put((url, level+1), block=True)
            L.info('SEED_SIZE_IN: %s' % seed_q.qsize())


def main():
    base_url = 'https://www.qidian.com/'
    level = 0
    seed_q = queue.Queue()
    text_q = queue.Queue()
    seed_q.put((base_url, level), block=True)
    seed_d.add(base_url) 
    thread_num = 1
    list1, list2 = [], []
    for i in range(thread_num):
        p1 = threading.Thread(target=get_book, args=(seed_q, text_q,))
        p2 = threading.Thread(target=parse_text, args=(seed_q, text_q,))
        p1.start()
        p2.start()
        list1.append(p1)
        list2.append(p2)
    for i in range(thread_num):
        list1[i].join()
        list2[i].join()

    for line in book_d:
        print(line)


if __name__ == '__main__':
    main()


