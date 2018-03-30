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
import csv
import tempfile
from django.utils import timezone

from api1c.models import *
from node.models import *
import func

from dj.views import *

base = base1c.objects.get(id=1)

#создаем задание, для засекания времени выгрузки
pe=procedureexchange.objects.get(id=56)
logexchange.objects.filter(procedureexchange=pe).update(success=True) #выключаем старые
lex=logexchange.objects.create(target='goodsinstock', fname='export to bitrix', success=False, ftime=datetime.datetime.now(), procedureexchange=pe) #создаем новое
#


for i in logexchange.objects.filter(procedureexchange__code=203, success=False):
	#print i.target, i.fname
	
	
	#очистка отстатков складов
	if i.target == 'Svobodnyj':
		print(i.target)
		goodsinstock.objects.filter(stock__id1c='ЦО0000005', goods__base=base).update(value=0)
	if i.target == 'Dommer':
		print(i.target)
		goodsinstock.objects.filter(stock__id1c='ЦО0000004', goods__base=base).update(value=0)
	if i.target == 'Planeta':
		print(i.target)
		goodsinstock.objects.filter(stock__id1c='ЦО0000007', goods__base=base).update(value=0)
	if i.target == 'Mega':
		print(i.target)
		goodsinstock.objects.filter(stock__id1c='ЦО0000002', goods__base=base).update(value=0)
	if i.target == 'Govorova':
		print(i.target)
		goodsinstock.objects.filter(stock__id1c='ЦБ0000004', goods__base=base).update(value=0)
	if i.target == 'Semafornay':
		print(i.target)
		goodsinstock.objects.filter(stock__id1c='ЦО0000001', goods__base=base).update(value=0)
	if i.target == 'Acinsk':
		print(i.target)
		goodsinstock.objects.filter(stock__id1c='ЦБ0000001', goods__base=base).update(value=0)
	#	
	
	for value in func.listcsv(i.fname):
	
		###PROCESS###
		#value['НоменклатураКод']
		#value['СкладКод']
		#value['СкладНаименование']
		#value['КоличествоОстаток']
		#
		try: #исключение количества
			c = int(value['КоличествоОстаток'])
		except:
			c = 0
		#
		if c > 0: #если количество больше 1
			s=stock.objects.filter(id1c=value['СкладКод'], status=True) #берем склад
			if s.exists(): #если склад сущесвует 
				s=s.first() #берем склад
				try: #пробуем взять товар
					g=goods.objects.get(id1c=value['НоменклатураКод'], base=base)
				except:
					print("%s NOT FOUND" % (value['НоменклатураКод']))
				else: #если товар существует
					pass
					try:
						gin=goodsinstock.objects.get(stock=s, goods=g)
					except:
						print("CREATE goodsinstock %s %s" % (value['НоменклатураКод'], value['СкладНаименование']))
						gin=goodsinstock(stock=s, goods=g, value=c)
						gin.save()
						g.catalogshow=True #включаем показ в каталоге
						g.save()
					else:
						print("UPDATE goodsinstock %s %s" % (value['НоменклатураКод'], value['СкладНаименование']))
						#вяжем количество с товаром
						gin.value=c
						gin.save()
						g.catalogshow=True #включаем показ в каталоге
						g.save()
			else: #если склад не существует
				print("%s %s IGNORE STOCK" % (value['НоменклатураКод'], value['СкладКод']))
			###END_PROCESS###
		
	func.logfile(i.fname)
	
#############################################################
#################### ОТПРАВЛЯЕМ НА САЙТ #####################
#############################################################	


salt = id_generator() #создаем сессию соль
token = makeapitoken(salt) #подписываем соль
g=goods.objects.filter(idbitrix__isnull=False).exclude(idbitrix__exact='') #товары только с idbitrix, исключаем пустые
#g=goods.objects.filter(idbitrix=30722) #отладка

for i in g:
	url = 'http://babah24.ru/c/1c/set_1.php?salt=%s&crc=%s&id=%s' % (salt, token, i.idbitrix)

	url = '%s&price=%s' % (url, i.price) #добавляем цену

	#общее количество товаров
	col=0
	for ii in i.goodsinstock_set.filter().exclude(stock__idbitrix__exact=''):
		col = col + ii.value

	if col >= 0:	
		url = '%s&col=%s' % (url, col) #добавляем общее количество
	else:
		url = '%s&col=%s' % (url, 0) #добавляем общее количество
	
	#значения на складах		
	for ii in i.goodsinstock_set.filter().exclude(stock__idbitrix__exact=''):
		ii.value
		if ii.value >= 0:
			url = '%s&col%s=%s' % (url, ii.stock.idbitrix, ii.value)
		else:
			url = '%s&col%s=%s' % (url, ii.stock.idbitrix, 0)

	#CATALOGSHOW
	
	
	value = i.goodsinstock_set.filter().exclude(stock__idbitrix__exact='').aggregate(s=Sum('value'), c=Count('value'))
	
	print(i, value)
	
	#i.catalogshow = False #отключил, включаю вручную
	if value['s'] != None and value['s'] >= 1:
		#i.catalogshow = True #отключил, включаю вручную
		url = '%s&catalogshow=%s' % (url, 1)
	else:
		url = '%s&catalogshow=%s' % (url, 0)

		
	#ШТРИХКОД
	data = i.barcodelist_set.filter(unit='шт')
	if data.exists():
		barcode = data.first().barcode
		url = '%s&barcode=%s' % (url, barcode) #добавляем штрих
		
	#СЕРТИФИКАТ
	try:
		data = i.goodscert.name
	except:
		data = ''
	url = '%s&certificatetext=%s' % (url, data) #добавляем сертификат	
	#
		
	
	#выполнение
	##print url #не включать на рабоей версии в консоль сыпить русские буквы и отваливается
	r = requests.get(url)
	print(r.status_code)
	#print r.encoding
	#print r.text
	print(r.json())

	
lex.endexectime=datetime.datetime.now()
lex.success=True #закрываем задание
lex.save()
	
