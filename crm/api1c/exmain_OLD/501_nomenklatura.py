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
model = goods
modelname = model().__class__.__name__
ccount = 0 #количество новых
base = base1c.objects.get(id=2)

for i in func.getfilelist(501):
	print i
	for value in func.listcsv(i):
	
		###PROCESS###
		#value['Код']
		#value['Наименование']
		#value['НаименованиеПолное']
		#value['Артикул']
		
		try:
			data=model.objects.get(id1c=value['Код'], base1c=base)
		except:
			ccount = ccount + 1 #+1 новый товар
			print "%s %s CREATE" % (modelname, value['Код'])
			data=model(id1c=value['Код'], base1c=base)
		else:
			print "%s %s EXISTS/UPDATE" % (modelname, value['Код'])

		#SAVE
		data.name=value['Наименование']
		data.namefull=value['НаименованиеПолное']
		data.art=value['Артикул']
		data.save()
		###END_PROCESS###
		
	func.logfile(i)
	
print "count new %s %s" % (modelname, ccount)
	
	
	
