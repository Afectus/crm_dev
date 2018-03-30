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
tmp=open('/home/ftp1c/Skidki.csv').read().decode('cp1251').encode('utf8')

#создаем временный файл
f = tempfile.NamedTemporaryFile(delete=False)
#print f.name
f.write(tmp) #пишем открытый файл во временный
f.close()

with open(f.name) as csvfile:
	reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
	for value in reader:
		try:
			d=discounts.objects.get(id1c=value['Код'])
		except:
			print "DISCOUNT %s CREATE" % value['Код']
			d=discounts.objects.create(id1c=value['Код'], name=value['Наименование'])
			d.save()
		else:
			print "DISCOUNT %s EXISTS" % value['Код']
			
os.unlink(f.name) #удаляем временный файл
print os.path.exists(f.name) #проверяем доступен ли временный файл после удаления