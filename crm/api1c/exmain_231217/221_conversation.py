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
model = relgoods
modelname = model().__class__.__name__
base = base1c.objects.get(id=1)
base2 = base1c.objects.get(id=2)

######WARNING####################
model.objects.all().delete()
#################################

for i in func.getfilelist(221):
	print i
	for value in func.listcsv(i):
	
		###PROCESS###
		#value['КодРозница']
		#value['КодБухгалтерия']
		
		g=goods.objects.filter(id1c=value['КодРозница'], base=base)
		g2=goods.objects.filter(id1c=value['КодБухгалтерия'], base=base2)
		if g.exists() and g2.exists():
			print "%s %s CREATE" % (modelname, value['КодРозница'])
			data=model()
			data.a=g.first()
			data.b=g2.first()
			data.save()
		else:
			print "%s %s NONE/IGNORE" % (modelname, value['КодРозница'])
		###END_PROCESS###
		
	func.logfile(i)
	
print "end update %s" % (modelname)
	
	
	
