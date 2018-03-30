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
		try: #исключение для цены
			p = float(value['Цена'])
		except:
			print "BAD PRICE 0 %s %s" % (value['Код'], value['ID_сайт'])
			p=0
		g=goods.objects.filter(id1c=value['Код'])
		if g.exists():
			print "EXIST PRICE %s %s" % (value['Код'], value['ID_сайт'])
			g.update(price=p)

os.unlink(f.name) #удаляем временный файл
print os.path.exists(f.name) #проверяем доступен ли временный файл после удаления
