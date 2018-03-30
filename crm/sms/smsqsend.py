#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, django

projecthome = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if projecthome not in sys.path:
    sys.path.append(projecthome)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj.settings")
django.setup()




import time
import requests
import datetime
from django.utils import timezone

from django.contrib.auth.models import User, Group

from node.models import *
from sms.models import *
from sms.views import *

from dj.views import *



for i in smsqsend.objects.filter(status=True):
	print(i.id, i.status, i.buyer.phone)
	try:
		u=User.objects.get(username='smsqsend')
	except:
		i.result='NOT FOUND USER smsqsend'
		i.save()
	else:
		r=sms4b(u, '8%s' % (i.buyer.phone), i.message)
		i.status=False
		i.send=True
		i.result=r
		i.save()
		print(r)
	
	
	
	
	
	
