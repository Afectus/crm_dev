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
Забираем имя видео файлов из битрикс для каждого товара
Забираем значение "Показывать в демо" для каждого товара
'''

'''
$token='XXXXX';
$crc = md5($ORDER_ID.":".$token);
$addurl = Array('bitrixorderid'=>$ORDER_ID, 'crc'=>$crc);
'''


salt = id_generator() #создаем сессию соль
token = makeapitoken(salt) #подписываем соль
#print salt, token

#выключаем все
#g=goods.objects.all().update(showondemo=False, touchscreen=False) #товары только с idbitrix, исключаем пустые

g=goods.objects.filter(idbitrix__isnull=False).exclude(idbitrix__exact='') #товары только с idbitrix, исключаем пустые
#g=goods.objects.filter(idbitrix=5592) #отладка

for i in g:
	#запрос
	url = 'http://babah24.ru/c/1c/getcatalogshow.php?salt=%s&crc=%s&id=%s' % (salt, token, i.idbitrix)
	r = requests.get(url)
	#print r.encoding
	#print r.text
	data = r.json()
	print r.status_code, url, data['res'], data['catalogshow']
	#ставим дефолтовые значения
	i.catalogshow = False
	if data['res'] == 1: #если успех
		if data['catalogshow'] == 'Y':
			i.catalogshow = True
	i.save()

