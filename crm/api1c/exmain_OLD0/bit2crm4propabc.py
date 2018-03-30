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
$token='XXXX';
$crc = md5($ORDER_ID.":".$token);
$addurl = Array('bitrixorderid'=>$ORDER_ID, 'crc'=>$crc);
'''


salt = id_generator() #создаем сессию соль
token = makeapitoken(salt) #подписываем соль
#print salt, token


g=goods.objects.filter(idbitrix__isnull=False, status=True).exclude(idbitrix__exact='') #товары только с idbitrix, исключаем пустые

for i in g:
	#запрос
	url = 'http://babah24.ru/c/1c/getpropabc.php?salt=%s&crc=%s&id=%s' % (salt, token, i.idbitrix)
	r = requests.get(url)
	#print r.encoding
	#print r.text
	data = r.json()
	print r.status_code, url, data['NEW'], data['HIT'], data['PRICE_GIFT'], data['RECOMMEND'], data['EXCLUSIVE'], data['KOL_RAZ'], data['TIME']
	#ставим значения
	if data['res'] == 1: #если успех
		if data['NEW'] == 'YES':
			try:
				print "ADD PROPERTIES VALUE %s " % (data['NEW'])
				p=properties.objects.get(code='NEW')
				propertiesvalue.objects.create(goods=i, properties=p, value=data['NEW'])
			except:
				print "FAIL"
				
		if data['HIT'] == 'YES':
			try:
				print "ADD PROPERTIES VALUE %s " % (data['HIT'])
				p=properties.objects.get(code='HIT')
				propertiesvalue.objects.create(goods=i, properties=p, value=data['HIT'])
			except:
				print "FAIL"
				
		if data['PRICE_GIFT'] == 'YES':
			try:
				print "ADD PROPERTIES VALUE %s " % (data['PRICE_GIFT'])
				p=properties.objects.get(code='PRICE_GIFT')
				propertiesvalue.objects.create(goods=i, properties=p, value=data['PRICE_GIFT'])
			except:
				print "FAIL"
				
		if data['RECOMMEND'] == 'YES':
			try:
				print "ADD PROPERTIES VALUE %s " % (data['RECOMMEND'])
				p=properties.objects.get(code='RECOMMEND')
				propertiesvalue.objects.create(goods=i, properties=p, value=data['RECOMMEND'])
			except:
				print "FAIL"
				
		if data['EXCLUSIVE'] == 'YES':
			try:
				print "ADD PROPERTIES VALUE %s " % (data['EXCLUSIVE'])
				p=properties.objects.get(code='EXCLUSIVE')
				propertiesvalue.objects.create(goods=i, properties=p, value=data['EXCLUSIVE'])
			except:
				print "FAIL"
				
		if data['KOL_RAZ']:
			try:
				print "ADD PROPERTIES VALUE %s " % (data['KOL_RAZ'])
				i.propa = data['KOL_RAZ']
			except:
				print "FAIL"
		if data['TIME']:
			try:
				print "ADD PROPERTIES VALUE %s " % (data['TIME'])
				i.propb = data['TIME']
			except:
				print "FAIL"
	i.save()

