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
model = discounts
modelname = model().__class__.__name__
ccount = 0 #количество новых

for i in func.getfilelist(212):
	print i
	for value in func.listcsv(i):
	
		###PROCESS###
		try:
			d=model.objects.get(id1c=value['Код'])
		except:
			print "%s %s CREATE" % (modelname, value['Код'])
			ccount = ccount + 1 #+1 новый товар
			d=model.objects.create(id1c=value['Код'], name=value['Наименование'])
		else:
			print "%s %s EXISTS/UPDATE" % (modelname, value['Код'])
		
		d.name=value['Наименование']
		d.save()

		###END_PROCESS###
		
	func.logfile(i)
	
print "count new %s %s" % (modelname, ccount)
	
	
	










