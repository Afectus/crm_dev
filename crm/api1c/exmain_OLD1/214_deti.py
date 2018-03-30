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
model = child
modelname = model().__class__.__name__
ccount = 0 #количество новых

for i in func.getfilelist(214):
	print i
	for value in func.listcsv(i):
	
		###PROCESS###
		#value['Код']
		#value['Имя']
		#value['Дата_рождения']
		#value['Пол']
		
		
		#пустые дети без дней роджения игнорируем
		if not value['Имя']:
			continue

		#берем родителя
		b = buyer.objects.get(id1c=value['Код'])
		if b:
			try:
				data=model.objects.get(buyer=b, name=value['Имя'], bday=func.getdate(value['Дата_рождения']))
			except:
				print "%s %s CREATE" % (modelname, value['Код'])
				ccount = ccount + 1
				data=model()
				data.buyer=b
				data.name=value['Имя']
			else:
				print "%s %s EXISTS/UPDATE" % (modelname, value['Код'])
				
			#SAVE
			data.name=value['Имя']
			data.bday=func.getdate(value['Дата_рождения'])
			if value['Пол'] == 'Женский':
				data.sex='female'
			data.save()
			
		
	func.logfile(i)
	
print "count new %s %s" % (modelname, ccount)
	
	
	
