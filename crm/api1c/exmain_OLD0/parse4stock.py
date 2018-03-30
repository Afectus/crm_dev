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
import csv
import tempfile


from node.models import *

#удаляем все остатки по складам и товарам
qinstock.objects.all().delete()

'''
g=goods.objects.filter(idbitrix__isnull=False, status=True).exclude(idbitrix__exact='') #товары только с idbitrix, исключаем пустые
for i in g:
	s=stock.objects.filter(status=True)
	for si in s:
		q=qinstock(stock=si, value=0)
		q.save()
		i.qinstock.add(q)
'''



#читаем файл, перекодируем в utf8
tmp=open('/home/ftp1c/NomenklaturaOstatki.csv').read().decode('cp1251').encode('utf8')

#создаем временный файл
f = tempfile.NamedTemporaryFile(delete=False)
#print f.name
f.write(tmp) #пишем открытый файл во временный
f.close()

with open(f.name) as csvfile:
	reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
	for value in reader:
		#проверяем заведен ли данный склад с кодом value['СкладКод'] и включен активен ли он, что бы не грузит система складами которых нет в CRM но есть в выгрузке, если склад НЕ акивен то игнорируем количество по данному складу
		s=stock.objects.filter(id1c=value['СкладКод'], status=True)
		if not s.exists():
			print "IGNORE STOCK %s " % (value['СкладКод'])
			continue
			
		try: #исключение количества
			c = int(value['КоличествоОстаток'])
		except:
			c=0
		
		if c < 1: #если количество меньше 1, то устанавливаем 0
			print "BAD QUANTITY %s " % (c)
			c=0
			#continue
		
		
		#попробуем завести количество товара на складе
		print "CREATE QUANTITY %s %s %s " % (value['НоменклатураКод'], value['СкладКод'], value['КоличествоОстаток'])
		s=s.first() #берем склад
		try:
			g=goods.objects.get(id1c=value['НоменклатураКод']) #берем товар
		except:
			print "BAD PRODUCT"
			continue
		else:
			#вяжем количество с товаром
			q=qinstock(stock=s, value=c)
			q.save()
			g.qinstock.add(q)

			
os.unlink(f.name) #удаляем временный файл
print os.path.exists(f.name) #проверяем доступен ли временный файл после удаления
