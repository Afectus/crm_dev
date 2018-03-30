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

for i in func.getfilelist(214):
	print(i)
	for value in func.listcsv(i):
	
		###PROCESS###
		#value['Код'] #код родителя
		#value['Имя'] #имя Ребенка
		#value['Дата_рождения'] #Дата рождения
		#value['ПолСсылка'] #пока не определен
		#value['Отчество'] #Отчество ребенка
		#value['Код1'] #код 1с
		
		#пустые дети без дней роджения игнорируем
		#if not value['Имя']:
		#	continue

		#берем родителя
		try:
			b = buyer.objects.get(id1c=value['Код'])
		except:
			print("buyer matching query does not exist.")
		else:
			if b:
				try:
					data=model.objects.get(buyer=b, id1c=value['Код1'])
				except:
					print("%s %s CREATE" % (modelname, value['Код']))
					ccount = ccount + 1
					data=model()
					data.id1c=value['Код1']
					data.buyer=b
				else:
					print("%s %s EXISTS/UPDATE" % (modelname, value['Код']))
					
				#SAVE
				data.type='son'
				data.i=value['Имя']
				data.o=value['Отчество']
				data.bday=func.getdate(value['Дата_рождения'])
				#if value['ПолСсылка'] == 'Женский':
				#	data.type='d'
				data.save()
			
		
	func.logfile(i)
	
print("count new %s %s" % (modelname, ccount))
	
	
	
