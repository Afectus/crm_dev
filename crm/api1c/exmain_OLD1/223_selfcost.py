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
base = base1c.objects.get(id=1)

######WARNING####################
model.objects.filter(base=base).update(startprice=0)
#################################

for i in func.getfilelist(223):
	print i
	for value in func.listcsv(i):
	
		###PROCESS###
		#value['НоменклатураКод']
		#value['Цена']

		g=goods.objects.filter(id1c=value['НоменклатураКод'], base=base)
		if g.exists():
			#пишем цену в model goods
			print value['НоменклатураКод'], func.getfloat(value['Цена'])
			g.update(startprice=func.getfloat(value['Цена']))
		else:
			print "%s %s NONE/IGNORE" % (modelname, value['НоменклатураКод'])
		###END_PROCESS###
		
	func.logfile(i)
	
print "count new %s %s" % (modelname, ccount)
	
	
	
