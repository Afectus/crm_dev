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
base = base1c.objects.get(id=1)

for i in func.getfilelist(221):
	print i
	for value in func.listcsv(i):
	
		###PROCESS###
		#value['КодРозница']
		#value['КодБухгалтерия']
		#value['ПометкаУдаления']
		
		data=model.objects.filter(id1c=value['КодРозница'])
		
		if data.exists():
			data.update(id1c2=value['КодБухгалтерия'])
			print "%s %s EXISTS/UPDATE" % (modelname, value['КодРозница'])
		
	func.logfile(i)
	
print "end update %s" % (modelname)
	
	
	
