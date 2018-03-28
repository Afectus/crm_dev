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

from node.models import *
from order.models import *
from notify.models import *

from dj.views import *

value='test message 111'
o=order.objects.get(id=375)

today = datetime.date.today()
om=ordermanager.objects.filter(handler='telegram', schedule=today.isoweekday()).order_by('-sort')[:3]
nh=notifyhandler.objects.get(name='telegram')
for i in om:
	print i.handler, i.user, i.schedule, i.sort
	nq=notifyqueue.objects.create(user=i.user, handler=nh, value=value)
	oe=orderevent.objects.create(order=o, event='telegram', comment='add telegram message for manager %s "%s" in notify queue' % (i, value), info='id %s in notifyqueue' % (nq.id))
	
	
	

	