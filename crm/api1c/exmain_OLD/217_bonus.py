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

for i in func.getfilelist(217):
	print i
	for value in func.listcsv(i):
	
		###PROCESS###
		#value['ДККод']
		#value['ДКВладелецКартыКод']
		#value['РазмерБонусаОстаток']
		print value['ДККод'], value['ДКВладелецКартыКод'], value['РазмерБонусаОстаток']
		#data=model.objects.get(id1c=value['ДККод'].strip())
		try:
			data=model.objects.get(id1c=value['ДККод'].strip())
		except:
			print "%s %s IGNORE" % (modelname, value['ДККод'])
			ccount = ccount + 1
		else:
			print "%s %s EXISTS/UPDATE" % (modelname, value['ДККод'])
		#SAVE
		data.bonus=0
		if value['РазмерБонусаОстаток']:
			data.bonus=float(value['РазмерБонусаОстаток'].replace(',','.'))
		data.save()
		
	func.logfile(i)
	
print "count IGNORE %s %s" % (modelname, ccount)
	
	
	
