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

from api1c.models import *
from node.models import *
import func

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
$token='XXX';
$crc = md5($ORDER_ID.":".$token);
$addurl = Array('bitrixorderid'=>$ORDER_ID, 'crc'=>$crc);
'''


salt = id_generator() #создаем сессию соль
token = makeapitoken(salt) #подписываем соль
#print salt, token
procedureexchangeid=56

lex = logexchange.objects.filter(procedureexchange__id=procedureexchangeid, success=False)

if lex.exists():

	#сбрасываем значения
	# print "start stockreset.php"
	# url = 'http://babah24.ru/c/1c/stockreset.php?salt=%s&crc=%s' % (salt, token)
	# print url
	# r = requests.get(url)
	# print r.status_code
	# print r.json()

	
	g=goods.objects.filter(idbitrix__isnull=False).exclude(idbitrix__exact='') #товары только с idbitrix, исключаем пустые
	#g=goods.objects.filter(idbitrix=30722) #отладка

	for i in g:
	
		url = 'http://babah24.ru/c/1c/set_1.php?salt=%s&crc=%s&id=%s' % (salt, token, i.idbitrix)
	
		url = '%s&price=%s' % (url, i.price) #добавляем цену
	
		#общее количество товаров
		col=0
		for ii in i.qinstock.all():
			col = col + ii.value

		if col >= 0:	
			url = '%s&col=%s' % (url, col) #добавляем общее количество
		else:
			url = '%s&col=%s' % (url, 0) #добавляем общее количество
			
			
		#значения на складах		
		for ii in i.qinstock.all():
			ii.value
			if ii.value >= 0:
				url = '%s&col%s=%s' % (url, ii.stock.idbitrix, ii.value)
			else:
				url = '%s&col%s=%s' % (url, ii.stock.idbitrix, 0)

		#CATALOGSHOW
		value = i.qinstock.aggregate(s=Sum('value'), c=Count('value'))
		
		#i.catalogshow = False #отключил, включаю вручную
		if value['s'] >= 1 and not None:
			#i.catalogshow = True #отключил, включаю вручную
			url = '%s&catalogshow=%s' % (url, 1)
		else:
			url = '%s&catalogshow=%s' % (url, 0)

			
		#ШТРИХКОД
		data = i.barcodelist_set.filter(unit='шт')
		if data.exists():
			barcode = data.first().barcode
			url = '%s&barcode=%s' % (url, barcode) #добавляем штрих	
			
		
		#выполнение
		print url
		r = requests.get(url)
		print r.status_code
		#print r.encoding
		#print r.text
		print r.json()


logexchange.objects.filter(procedureexchange__id=procedureexchangeid).update(success=True) #выключаем старые