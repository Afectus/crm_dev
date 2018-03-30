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

from dj.views import *

######################################

print("delete old file")
os.system('find /home/ftp1c/test/upload/ -mindepth 1 -type f -mmin +60 -delete')
os.system('find /home/ftp1c/tmp/ -mindepth 1 -type f -mmin +60 -delete')
print("end delete old file")

print("unzip file")
os.system('for z in /home/ftp1c/test/upload/*.zip; do unzip -o -P12345 -d /home/ftp1c/tmp/ $z; done')
os.system('for z in /home/ftp1c/upload/*.zip; do unzip -o -P12345 -d /home/ftp1c/tmp/ $z; done')
print("end unzip file")

tmppath = '/home/ftp1c/tmp'

# for folder, subs, files in os.walk('/home/ftp1c/tmp'):
	# for file in files:
		# print(file)
		# #os.system('/usr/bin/enconv -x UTF-8 %s/%s' % (tmppath, file))
		# #os.system('iconv -f WINDOWS-1251 -t UTF-8 %s/%s -o %s/%s' % (tmppath, file, tmppath, file))




data=procedureexchange.objects.filter(status=True, cron=True)

for i in data:
	print('=', i)
	func.maketask(i.code, tmppath)

#######################################
