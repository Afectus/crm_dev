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
model = discountcard
modelname = model().__class__.__name__
ccount = 0 #количество новых

for i in func.getfilelist(216):
	print(i)
	for value in func.listcsv(i):
	
		###PROCESS###
		#value['Код']
		#value['КодКарты']
		#value['ВладелецКартыКод']

		try:
			pdata = buyer.objects.get(id1c=value['ВладелецКартыКод'].strip())
		except:
			continue
		#
		try:
			data=model.objects.get(name=value['КодКарты'].strip())
		except:
			print("%s %s CREATE" % (modelname, value['КодКарты']))
			ccount = ccount + 1
			data=model(name=value['КодКарты'].strip())
			data.buyer=pdata
		else:
			print("%s %s EXISTS/UPDATE" % (modelname, value['КодКарты']))
		#SAVE
		data.id1c=value['Код'].strip()
		data.buyer=pdata
		data.save()
		##################################
		
	func.logfile(i)
	
print("count new %s %s" % (modelname, ccount))
	
	
	
