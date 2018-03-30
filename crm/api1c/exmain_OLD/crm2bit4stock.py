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
#Количество товара на складах носит информационный характер и не влияет на расчет остатков товара в битрикс.
#Пишем на сайт в поле "Доступное количество" общее количество (наличие) товара
#со всех складов.
#Пишем на сайт в склады "Торговый каталог"->"Склады" количество товара на складах.
#При покупке покупателем товара на сайте, количество списывается только из поля 
#"Доступное количество", со складов ни чего не списывается, так как реальной
#покупки еще не произошоло, реальная покупка происохдит в 1с, затем выгрузка
#доступного количества на сайт в склады
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
#g=goods.objects.filter(idbitrix=38006, status=True) #отладка

for i in g:

	#сбрасываем количестов на складе
	print i.id, i.idbitrix, 'RESET STOCK'
	#запрос
	url = 'http://babah24.ru/c/1c/stockreset.php?salt=%s&crc=%s&id=%s' % (salt, token, i.idbitrix)
	print url
	r = requests.get(url)
	print r.status_code
	#print r.encoding
	#print r.text
	print r.json()

	col=0
	
	for ii in i.qinstock.all():
		col = col + ii.value
		
		#обновляем количестов на складе
		print i.id, i.idbitrix, ii.value, 'stock update'
		#запрос
		url = 'http://babah24.ru/c/1c/stockupdate.php?salt=%s&crc=%s&id=%s&col=%s&idstock=%s' % (salt, token, i.idbitrix, ii.value, ii.stock.idbitrix)
		print url
		r = requests.get(url)
		print r.status_code
		#print r.encoding
		#print r.text
		print r.json()
		
		
	
	#обновляем общее количество одного товара
	if col >= 0:
		print i.id, i.idbitrix, col, 'col update'
		#запрос
		url = 'http://babah24.ru/c/1c/colupdate.php?salt=%s&crc=%s&id=%s&col=%s' % (salt, token, i.idbitrix, col)
		print url
		r = requests.get(url)
		print r.status_code
		#print r.encoding
		#print r.text
		print r.json()
		
	else:
		print i.id, i.idbitrix, col, 'fail'

