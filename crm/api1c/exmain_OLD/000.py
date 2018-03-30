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




for i in procedureexchange.objects.filter(status=True).order_by('-sort'):
	print i.name, i.fname
	os.system('/var/www/crm/api1c/exmain/%s' % (i.fname))
	
	
	
	
a = (
	'bit2crm4status.py',
	'bit2crm4bname.py',
	'bit2crm4nabor.py',
	'bit2crm4demovideotouch.py',
	'bit2crm4section.py',
	'bit2crm4prop.py',
	'bit2crm4propval.py',
	'bit2crm4propabc.py',
	##'crm2bit4artikul.py',
	##'qrcodegen.py',
	'bit2crm4image.py',
	#
	#crm2bit4CATALOGSHOW.py
	#crm2bit4artikul.py
	#crm2bit4name.py
	'crm2bit4price.py',
	'crm2bit4stock.py',
	##log
	'commonlog.py',
	)
	
for i in a:
	print i
	os.system('/var/www/crm/api1c/exmain/%s' % (i))
	
	
