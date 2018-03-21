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

from panel.models import *
from notify.models import *

from dj.views import *

from notify.views import *

#TELEGRAM
data = notifyqueue.objects.filter(during=True, handler__name='telegram')
for i in data:
	print(i)
	try:
		nuk=profileuser.objects.get(user=i.user)
	except Exception as e:
		print(e)
	else:
		#print "send message '%s' key '%s'" % (i.value, nuk.value)
		res = False
		try:
			res=telegram_bot_notify(nuk.telegram, i.value)
		except Exception as e:
			pass
			print('error=', e)
		else:
			res=True
			i.during=False #оповещения отработали
			i.save()
			print(res)
			
	

#TELEGRAM
data = notifyqueue.objects.filter(during=True, handler__name='telegram_chat')
for i in data:
	print(i)
	try:
		nuk=profileuser.objects.get(user__username='telegram_chat2')
	except Exception as e:
		print(e)
	else:
		#print("send message '%s' key '%s'" % (i.value, nuk.telegram))
		res = False
		try:
			res=telegram_bot_chat(nuk.telegram, i.value)
		except Exception as e:
			pass
			print('error=', e)
		else:
			res=True
			i.during=False #оповещения отработали
			i.save()
			print(res)