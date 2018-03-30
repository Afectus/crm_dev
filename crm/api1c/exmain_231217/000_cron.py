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


func.unzip()
func.maketask()

#выбираем только родителей выгрузки
for i in procedureexchange.objects.filter(parent__isnull=True, status=True, start=True, cron=True).order_by('-sort'):
	print i.name, i.fname
	os.system('/var/www/crm/api1c/exmain/%s' % (i.fname))
	#выгружаем зависимости, выбираем только подчиненных для выгрузки
	for p in procedureexchange.objects.filter(parent=i, parent__isnull=False, status=True, start=True, cron=True).order_by('-sort'):
		print '- ', p.name, p.fname
		os.system('/var/www/crm/api1c/exmain/%s' % (p.fname))
	
	
	
