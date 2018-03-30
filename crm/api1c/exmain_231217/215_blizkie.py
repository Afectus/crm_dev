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
model = buyerrel
modelname = model().__class__.__name__
ccount = 0 #количество новых

for i in func.getfilelist(215):
	print i
	for value in func.listcsv(i):
	
		###PROCESS###
		#value['Код'] #код родителя
		#value['Имя']
		#value['СтепеньРодства']
		#value['ДатаРожденияБР']
		#value['Отчество']
		#value['Код1']
		
		try:
			b=buyer.objects.get(id1c=value['Код'])
		except:
			print "buyer matching query does not exist."
		else:
			try:
				data=model.objects.get(buyer=b, id1c=value['Код1'])
			except:
				ccount = ccount + 1
				print "%s %s CREATE" % (modelname, value['Код'])
				data=model()
				data.id1c=value['Код1']
				data.buyer=b
			else:
				print "%s %s EXISTS/UPDATE" % (modelname, value['Код'])
			
			#SAVE
			data.i=value['Имя']
			data.o=value['Отчество']
			data.bday=func.getdate(value['ДатаРожденияБР'])
			#обработка степень родства
			# ('son', 'Сын'),
			# ('d', 'Дочь'),
			# ('f', 'Отец'),
			# ('m', 'Мать'),
			# ('sis', 'Сестра')
			# ('b', 'Брат'),
			# ('other', 'Близкий Родственник'),
			data.type='other'
			if value['СтепеньРодства'].lower() == 'Сын'.lower():
				data.type='son'
			if value['СтепеньРодства'].lower() == 'Дочь'.lower():
				data.type='d'
			if value['СтепеньРодства'].lower() == 'Отец'.lower():
				data.type='f'
			if value['СтепеньРодства'].lower() == 'Мать'.lower() or value['СтепеньРодства'].lower() == 'мама'.lower():
				data.type='m'
			if value['СтепеньРодства'].lower() == 'Сестра'.lower():
				data.type='sis'
			if value['СтепеньРодства'].lower() == 'Брат'.lower():
				data.type='b'
			data.save()


	
	func.logfile(i)
	
print "count new %s %s" % (modelname, ccount)
	
	
	
