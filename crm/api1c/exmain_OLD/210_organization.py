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
model = organization
modelname = model().__class__.__name__
ccount = 0 #количество новых

for i in func.getfilelist(210):
	print i
	for value in func.listcsv(i):
	
		###PROCESS###
		#value['Код']
		#value['Наименование']
		#value['НаименованиеПолное']
		#value['НаименованиеСокращенное']
		#value['ИНН']
		try:
			data=model.objects.get(id1c=value['Код'])
		except:
			print "%s %s CREATE" % (modelname, value['Код'])
			ccount = ccount + 1
			data=model(id1c=value['Код'])
		else:
			print "%s %s EXISTS/UPDATE" % (modelname, value['Код'])
		
		data.name=value['Наименование']
		data.namefull=value['НаименованиеПолное']
		data.nameshort=value['НаименованиеСокращенное']
		data.inn=value['ИНН']
		data.save()

		###END_PROCESS###
		
	func.logfile(i)
	
print "count new %s %s" % (modelname, ccount)
	
	
	










