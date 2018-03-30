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




for i in procedureexchange.objects.filter(status=True, start=True).order_by('-sort'):
	print i.name, i.fname
	os.system('/var/www/crm/api1c/exmain/%s' % (i.fname))
	
	
	
	
a = (
	'212_skidka.py',
	'210_organization.py',
	'208_shops.py',
	'207_kassa.py',
	'209_sklad.py',
	'220_price_type.py',
	'201_nomenklatura.py',
	'218_price.py',
	'222_ed_izm.py'
	'203_ostatki.py'
	'204_fiz_lica.py'
	'213_fio.py'
	'214_deti.py'
	'215_blizkie.py'
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
	
	
	
