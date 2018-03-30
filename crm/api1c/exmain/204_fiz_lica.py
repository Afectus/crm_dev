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
model = buyer
modelname = model().__class__.__name__
ccount = 0 #количество новых

for i in func.getfilelist(204):
	print(i)
	for value in func.listcsv(i):
	
		###PROCESS###
		try:
			data=model.objects.get(id1c=value['Код'])
		except:
			ccount = ccount + 1 #+1 новый товар
			print("%s %s CREATE" % (modelname, value['Код']))
			data=model(id1c=value['Код'])
		else:
			print("%s %s EXISTS/UPDATE" % (modelname, value['Код']))
		
		#SAVE
		data.id1c=value['Код']
		data.bday=func.getdate(value['ДатаРождения'])
		data.phone=value['Телефон']
		data.adv=func.getbool(value['Согласие_на_рассылку'])
		if value['Пол'] == 'Женский':
			data.sex='female'
			
		#log 1c
		try:
			data.creator=value['Кто_записалКод']
		except:
			pass
		try:
			data.creator=value['Дата_записи']
		except:
			pass
		try:
			data.creator=value['Кто_изменилКод']
		except:
			pass
		try:
			data.creator=value['Дата_изменения']
		except:
			pass
		
		data.save()

		
	func.logfile(i)
	
print("count new %s %s" % (modelname, ccount))
	
	
	
