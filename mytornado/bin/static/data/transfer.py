#!/usr/bin/env python
#encoding=GB18030

import urllib
import  xml.dom.minidom
import datetime 

resp=urllib.urlopen('http://gouwu.sogou.com/shopindex/youhuicuxiao/data/data.xml')
html=resp.read().decode('GB18030').encode('UTF-8').replace('<?xml version="1.0" encoding="GBK"?>','<?xml version="1.0" encoding="UTF-8"?>')
dom=xml.dom.minidom.parseString(html)

site = set([])
cate = set([])
site2 = set([])
cate2 = set([])

sites = {}
cates = {}

now = datetime.datetime.now()
count = 0;
for product in dom.getElementsByTagName('productpa'):
    t_str = product.getElementsByTagName('end_time')[0].firstChild.data
    d=datetime.datetime.strptime(t_str,'%Y-%m-%d %H:%M:%S')
    url = product.getElementsByTagName('url')[0].firstChild.data
    if(count >= 100):
        product.parentNode.removeChild(product)
    elif(d < now):
        product.parentNode.removeChild(product)
    else:
        b_id = product.getElementsByTagName('business_id')[0].firstChild.data
        c_id = '-1'
        if(type(product.getElementsByTagName('cate_name_id')[0].firstChild) != type(None)):
            c_id = product.getElementsByTagName('cate_name_id')[0].firstChild.data
        if(b_id in site and c_id in cate):
            if(b_id in site2 and c_id in cate2):
                product.parentNode.removeChild(product)
            else:
                count+=1
                site2.add(b_id)
                cate2.add(c_id)
        else:
            count+=1
            site.add(b_id)
            cate.add(c_id)
print "COUNT: count=%d" % (count)

'''
f = open('result.xml', 'wb')
result = dom.toxml().encode("GB18030").replace('<?xml version="1.0" ?>','<?xml version="1.0" encoding="GBK"?>')
f.write(result)
f.close()
'''

# split productpa by cate and site
# 需要保留原item和moreurl
ori_item = dom.getElementsByTagName('item')[0]
moreurl = dom.getElementsByTagName('moreurl')[0]
# 新增部分重新重新过滤
dom_2=xml.dom.minidom.parseString(html)
for product in dom_2.getElementsByTagName('productpa'):
    t_str = product.getElementsByTagName('end_time')[0].firstChild.data
    d=datetime.datetime.strptime(t_str,'%Y-%m-%d %H:%M:%S')
    if d < now:
        continue
    b_id = product.getElementsByTagName('business')[0].firstChild.data
    if b_id not in sites:
        sites[b_id] = []
    sites[b_id].append(product)
    url = product.getElementsByTagName('url')[0].firstChild.data
    try:
        c_ids_raw = product.getElementsByTagName('cate_name_and_id_all')[0].firstChild.data.split(';')
    except:
        continue
    c_ids = set([c.split(',')[0] for c in c_ids_raw if len(c) > 0])
    for c_id in c_ids:
        if c_id not in cates:
            cates[c_id] = []
        cates[c_id].append(product)

detail_dom=xml.dom.minidom.parseString('<?xml version="1.0" ?><DOCUMENT></DOCUMENT>')
document = detail_dom.getElementsByTagName('DOCUMENT')[0]
o = detail_dom.importNode(ori_item, True)
document.appendChild(o)
# 按cate分
for cate in cates:
    item = detail_dom.createElement('item')
    key = detail_dom.createElement('key')
    key.appendChild(detail_dom.createCDATASection('%s' % cate.encode('GB18030')))
    display = detail_dom.createElement('display')
    m = detail_dom.importNode(moreurl, True)
    display.appendChild(m)
    count = 0
    for product in cates[cate]:
        if count >= 100:
            break
        p = detail_dom.importNode(product, True)
        display.appendChild(p)
        count += 1
    item.appendChild(key)
    item.appendChild(display)
    document.appendChild(item)
    print "CATE COUNT: cate=%s, count=%d" % (cate, count)
# 按site分
for site in sites:
    item = detail_dom.createElement('item')
    key = detail_dom.createElement('key')
    key.appendChild(detail_dom.createCDATASection('%s' % site))
    display = detail_dom.createElement('display')
    m = detail_dom.importNode(moreurl, True)
    display.appendChild(m)
    count = 0
    for product in sites[site]:
        if count >= 100:
            continue
        p = detail_dom.importNode(product, True)
        display.appendChild(p)
        count += 1
    item.appendChild(key)
    item.appendChild(display)
    document.appendChild(item)
    print "SITE COUNT: site=%s, count=%d" % (site.encode('gb18030'), count)

f = open('result.xml', 'wb')
result = detail_dom.toxml().encode("GB18030").replace('<?xml version="1.0" ?>','<?xml version="1.0" encoding="GBK"?>')
f.write(result)
f.close()
