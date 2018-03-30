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



#buyer.objects.all().delete()



#читаем файл, перекодируем в utf8
tmp=open('/home/ftp1c/FizLiza.csv').read().decode('cp1251').encode('utf8')

#создаем временный файл
f = tempfile.NamedTemporaryFile(delete=False)
#print f.name
f.write(tmp) #пишем открытый файл во временный
f.close()

with open(f.name) as csvfile:
	reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
	for value in reader:
		b=buyer.objects.filter(id1c=value['Код'])
		
		#пробуем дату рождения
		#print value['ДатаРождения']
		try:
			getdate=datetime.datetime.strptime(value['ДатаРождения'],"%d.%m.%Y %H:%M:%S")
		except:
			getdate=None
		print getdate
		
		#берем согласие на рассылку
		adv=False
		try:
			advtmp=value['Согласие_на_рассылку']
		except:
			pass
		else:
			if advtmp == 'Да':
				adv=True
		#
		
		if b.exists(): #если покупатель существует, заменяем поля
			print "EXISTS BUYER %s %s" % (value['Код'], value['Телефон'])
			b.update(
				id1c=value['Код'],
				f=value['Фамилия'],
				i=value['Имя'],
				o=value['Отчество'],
				bday=getdate,
				male=value['Пол'],
				phone=value['Телефон'],
				dcard=value['КодКарты'],
				adv=adv,
				)
			if value['РазмерБонусаОстаток']:
				b.update(bonus=float(value['РазмерБонусаОстаток'].replace(',','.')))
		else: #иначе создаем нового
			print "CREATE BUYER %s %s" % (value['Код'], value['Телефон'])
			b=buyer(
				id1c=value['Код'],
				f=value['Фамилия'],
				i=value['Имя'],
				o=value['Отчество'],
				bday=getdate,
				male=value['Пол'],
				phone=value['Телефон'],
				dcard=value['КодКарты'],
				adv=adv,
				)
			b.save()

os.unlink(f.name) #удаляем временный файл
print os.path.exists(f.name) #проверяем доступен ли временный файл после удаления