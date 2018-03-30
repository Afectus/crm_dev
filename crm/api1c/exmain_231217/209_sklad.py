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
model = stock
modelname = model().__class__.__name__
ccount = 0 #количество новых
base = base1c.objects.get(id=1)

for i in func.getfilelist(209):
	print i
	for value in func.listcsv(i):
	
		###PROCESS###
		#value['Код']
		#value['Наименование']
		#value['ТипСклада']
		#value['ОрганизацияКод']
		#value['МагазинКод']
		try:
			data=model.objects.get(id1c=value['Код'], base=base)
		except:
			print "%s %s CREATE" % (modelname, value['Код'])
			ccount = ccount + 1
			data=model.objects.create(id1c=value['Код'], name=value['Наименование'], base=base)
		else:
			print "%s %s EXISTS/UPDATE" % (modelname, value['Код'])
			
		data.shop=func.getforeign(shop, value['МагазинКод'])
		data.organization=func.getforeign(organization, value['ОрганизацияКод'])
		data.save()

		###END_PROCESS###
		
	func.logfile(i)
	
print "count new %s %s" % (modelname, ccount)
	
	
	










