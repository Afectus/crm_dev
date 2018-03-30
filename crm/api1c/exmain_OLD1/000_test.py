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
model = logexchange
modelname = model().__class__.__name__
ccount = 0 #количество новых
base = base1c.objects.get(id=1)


for i in func.getfilelist(201):
	print i
	for value in func.listcsv(i):
		ccount = ccount + 1

	func.logfile(i)
	
print "count new %s %s" % (modelname, ccount)
	
	
	
