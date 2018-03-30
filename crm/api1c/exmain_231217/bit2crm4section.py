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

from node.models import *

from dj.views import *

'''
Забираем список раздела для каждого товара
'''

'''
$token='XXXXXXX';
$crc = md5($ORDER_ID.":".$token);
$addurl = Array('bitrixorderid'=>$ORDER_ID, 'crc'=>$crc);
'''


salt = id_generator() #создаем сессию соль
token = makeapitoken(salt) #подписываем соль
#print salt, token


g=goods.objects.filter(idbitrix__isnull=False, status=True).exclude(idbitrix__exact='') #товары только с idbitrix, исключаем пустые

#g=goods.objects.filter(idbitrix=5614)


for i in g:
	#запрос
	url = 'http://babah24.ru/c/1c/getsection.php?salt=%s&crc=%s&id=%s' % (salt, token, i.idbitrix)
	r = requests.get(url)
	#print r.encoding
	#print r.text
	data = r.json()
	print r.status_code, url, data['res'], data['data']
	#вяжем категории
	i.tax.clear() #очищаем
	for t in data['data']:
		print t
		datatax = tax.objects.filter(idbitrix=t)
		for ii in datatax:
			i.tax.add(ii)


