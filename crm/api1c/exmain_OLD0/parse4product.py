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

#goods.objects.all().delete()

ccount = 0 #количество новых товаров


#читаем файл, перекодируем в utf8
tmp=open('/home/ftp1c/Nomenklatura.csv').read().decode('cp1251').encode('utf8')

#создаем временный файл
f = tempfile.NamedTemporaryFile(delete=False)
#print f.name
f.write(tmp) #пишем открытый файл во временный
f.close()

with open(f.name) as csvfile:
	reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
	for value in reader:
		print "TEST %s %s" % (value['Код'], value['ID_сайт'])
		g=goods.objects.filter(id1c=value['Код'])
		try: #исключение для цены
			p = float(value['Цена'])
		except:
			p=0
		if g.exists():
			print "EXIST %s %s" % (value['Код'], value['ID_сайт'])
			g.update(price=p, idbitrix=value['ID_сайт']) #разобраться
			g.update(barcode=value['Штрихкод']) #пишем штрихкод
			g.update(name=value['НаименованиеПолное']) #пишем штрихкод
		else:
			ccount = ccount + 1 #+1 новый товар
			print "CREATE %s %s" % (value['Код'], value['ID_сайт'])
			try: #исключение для цены
				p = float(value['Цена'])
			except:
				pass
			else:
				g.update(price=p)
			g=goods(
				id1c=value['Код'],
				idbitrix=value['ID_сайт'],
				name=value['Ссылка'],
				namefull=value['НаименованиеПолное'],
				art=value['Артикул'],
				desc=value['ДополнительноеОписание'],
				barcode=value['Штрихкод'],
				#video=value['None'],
				#qinstock=value['None'],
				price=p,
				)
			g.save()


os.unlink(f.name) #удаляем временный файл
print os.path.exists(f.name) #проверяем доступен ли временный файл после удаления

print "count new product %s" % ccount