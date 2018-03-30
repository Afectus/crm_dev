#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, django

projecthome = '/var/www/crm/'
if projecthome not in sys.path:
    sys.path.append(projecthome)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj.settings")
django.setup()



import time
import requests
import datetime
from django.utils import timezone

import xml.etree.ElementTree as ET

from node.models import *

from dj.views import *



'''
$token='XXXX';
$crc = md5($ORDER_ID.":".$token);
$addurl = Array('bitrixorderid'=>$ORDER_ID, 'crc'=>$crc);
'''


salt = id_generator() #создаем сессию соль
token = makeapitoken(salt) #подписываем соль
#print salt, token


'''
Забираем все свойства из битрикс для инфоблока каталог товаров
'''
propertiesvalue.objects.all().delete()



g=goods.objects.filter(idbitrix__isnull=False, status=True).exclude(idbitrix__exact='') #товары только с idbitrix, исключаем пустые
#g=goods.objects.filter(idbitrix=5596)


for i in g:
	#запрос
	url = 'http://babah24.ru/c/1c/getpropval2.php?salt=%s&crc=%s&id=%s' % (salt, token, i.idbitrix)
	print url
	r = requests.get(url)
	tmp=r.text
	tmp=tmp.strip()
	tmp=tmp.encode('utf8')
	root = ET.fromstring(tmp)
	for e in root:
		#print i
		#print e[0].text, e[1].text, e[2].text
		#p=properties.objects.get(code=e[1].text)
		#propertiesvalue.objects.create(goods=i, properties=p, value=e[2].text)
		try:
			print "ADD PROPERTIES VALUE %s %s %s" % (e[0].text, e[1].text, e[2].text)
			p=properties.objects.get(code=e[1].text)
			propertiesvalue.objects.create(goods=i, properties=p, value=e[2].text)
		except:
			print "FAIL"




