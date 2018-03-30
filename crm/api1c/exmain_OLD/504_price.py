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
model = pricegoods
modelname = model().__class__.__name__
ccount = 0 #количество новых
base = base1c.objects.get(id=2)

######WARNING####################
model.objects.filter(pricetype__base=base).delete()
#################################

for i in func.getfilelist(504):
	print i
	for value in func.listcsv(i):
	
		###PROCESS###
		#value['НоменклатураКод']
		#value['Цена']
		#value['ТипЦенКод']

		g=goods.objects.filter(id1c=value['НоменклатураКод'], base=base)
		if g.exists():
			#пишем цену в model goods
			pt=func.getforeign(pricetype, value['ТипЦенКод'])
			print pt.id1c
			if pt.id1c == '00-000003':
				print value['НоменклатураКод'], func.getfloat(value['Цена'])
				g.update(price=func.getfloat(value['Цена']))
			#
			ccount = ccount + 1 #+1 новый товар
			print "%s %s CREATE" % (modelname, value['НоменклатураКод'])
			data=model()
			data.goods=g.first()
			data.price=func.getfloat(value['Цена'])
			data.pricetype=func.getforeign(pricetype, value['ТипЦенКод'])
			data.save()
		else:
			print "%s %s NONE/IGNORE" % (modelname, value['НоменклатураКод'])
		###END_PROCESS###
		
	func.logfile(i)
	
print "count new %s %s" % (modelname, ccount)
	
	
	
