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
model = buyerevent
modelname = model().__class__.__name__
ccount = 0 #количество новых

for i in func.getfilelist(215):
	print i
	for value in func.listcsv(i):
	
		###PROCESS###
		#value['Код']
		#value['Имя']
		#value['СтепеньРодства']
		#value['ДатаРожденияБР']
		
		b=buyer.objects.get(id1c=value['Код'])
		
		try:
			data=model.objects.get(buyer=b, stime=func.getdate(value['ДатаРожденияБР']))
		except:
			ccount = ccount + 1
			print "%s %s CREATE" % (modelname, value['Код'])
			data=model()
		else:
			print "%s %s EXISTS/UPDATE" % (modelname, value['Код'])
		
		#SAVE
		data.buyer=b
		data.name=value['Имя']
		data.type='1c'
		data.stime=func.getdate(value['ДатаРожденияБР'])
		data.comment='Имя=%s, СтепеньРодства=%s, ДатаРожденияБР=%s' % (value['Имя'], value['СтепеньРодства'], value['ДатаРожденияБР'])
		data.save()

		
	func.logfile(i)
	
print "count new %s %s" % (modelname, ccount)
	
	
	
