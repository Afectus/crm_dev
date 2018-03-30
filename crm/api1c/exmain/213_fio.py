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
model = buyer
modelname = model().__class__.__name__
ccount = 0 #количество новых

for i in func.getfilelist(213):
	print(i)
	for value in func.listcsv(i):
	
		###PROCESS###
		data=model.objects.filter(id1c=value['ФизЛицоКод'])
		if data.exists():
			print("%s %s EXISTS/UPDATE" % (modelname, value['ФизЛицоКод']))
			#SAVE
			data.update(
				f=value['Фамилия'],
				i=value['Имя'],
				o=value['Отчество'],
				)
		
	func.logfile(i)
	
print("count new %s %s" % (modelname, ccount))
	
	
	
