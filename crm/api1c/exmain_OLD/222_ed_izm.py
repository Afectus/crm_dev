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
model = baseunit
modelname = model().__class__.__name__
ccount = 0 #количество новых
base = base1c.objects.get(id=1)

for i in func.getfilelist(222):
	print i
	for value in func.listcsv(i):
	
		###PROCESS###
		#value['Код']
		#value['ВладелецКод']
		#value['Наименование']
		#value['Коэффициент']
		print value['ВладелецКод']
		g=goods.objects.get(id1c=value['ВладелецКод'], base=base)

		try:
			data=model.objects.get(id1c=value['Код'])
		except:
			ccount = ccount + 1 #+1 новый товар
			print "%s %s CREATE" % (modelname, value['Код'])
			data=model(id1c=value['Код'])
		else:
			print "%s %s EXISTS/UPDATE" % (modelname, value['Код'])

		#SAVE
		data.goods=g
		data.value=value['Наименование']
		data.factor=value['Коэффициент']
		data.save()
		###END_PROCESS###
		
	func.logfile(i)
	
print "count new %s %s" % (modelname, ccount)
	
	
	
