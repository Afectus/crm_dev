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

os.system('/var/www/crm/api1c/exmain/000_maketask.py')



for i in procedureexchange.objects.filter(status=True, cron=True).order_by('-sort'):
	#print(i.name, i.fname)
	os.system('/usr/bin/python /var/www/crm/api1c/exmain/%s' % (i.fname))
	#os.system('/usr/bin/python /var/www/crm/api1c/exmain/218_price.py')
	

	
