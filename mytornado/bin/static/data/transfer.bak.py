#!/usr/bin/env python

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

f = open('result_test.xml', 'wb')
result = dom.toxml().encode("GB18030").replace('<?xml version="1.0" ?>','<?xml version="1.0" encoding="GBK"?>')
f.write(result)
f.close()
