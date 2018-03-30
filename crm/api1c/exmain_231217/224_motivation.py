#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, django

projecthome = '/var/www/crm'
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
base = base1c.objects.get(id=1)

for i in func.getfilelist(224):
	print i
	
	print 'ALL GOODS TO 0 MOTIVATION'
	m=goodsmotivationratiosum.objects.get(ratio=0, percent=0, dpercent=0)
	goods.objects.filter(base=base).update(motivationinpoints1=m)
	
	for value in func.listcsv(i):
	
		###PROCESS###
		#value['НоменклатураКод']
		#value['Категория']
		#value['Бонус']
		#value['Дебонус']
		
		try: #пробуем взять мотивацию
			m=goodsmotivationratiosum.objects.get(ratio=value['Категория'])
		except:
			print "MOTIVATION %s NOT FOUND" % (value['Категория'])
		else:
			######пишем проценты#######
			print "%s EXISTS/UPDATE MOTIVATION %s" % (modelname, m.ratio)
			try: #исключение Бонус
				percent = float(value['Бонус'])
			except:
				percent = 0
			try: #исключение Бонус
				dpercent = float(value['Дебонус'])
			except:
				dpercent = 0
			m.percent=percent
			m.dpercent=dpercent
			m.save()
			###########################
			try:
				g=model.objects.get(id1c=value['НоменклатураКод'], base=base)
			except:
				ccount = ccount + 1 #+1 товар
				print "%s %s GOODS NOT FOUND" % (modelname, value['НоменклатураКод'])
			else:
				print "%s EXISTS/UPDATE MOTIVATION %s -> GOODS %s" % (modelname, m.ratio, g.id1c)
				#SAVE
				g.motivationinpoints1=m
				g.save()
				###END_PROCESS###

	func.logfile(i)
	
print "count new %s %s" % (modelname, ccount)
	
	
	
