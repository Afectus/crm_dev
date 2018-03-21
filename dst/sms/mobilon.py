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

from django.conf import settings

from node.models import *
from sms.models import *
from sms.views import *

from dj.views import *


# def mobilon(phone):
	# apitoken = settings.MOBILON_TOKEN
	
	# res = 'bad'
	
	# url = 'https://connect.mobilon.ru/api/call/CallToSubscriber?key=%s&outboundNumber=%s' % (apitoken, phone)

	# print "\n"
	# print url
	# print "\n"
	# r = requests.get(url, verify=False)
	# print r.status_code
	# print r.json()
	
	# #логируем в базу
	# #csmsreport = smsreport(user=user, phone=phone, text=text, status=res,)
	# #csmsreport.save()
	# res = r.json()
	
	# print res['result']
	# if res['result'] == 'SUCCESS':
		
	# return res
	
#u=User.objects.get(id=1)
	
#mobilon(u, '895040903201111111')