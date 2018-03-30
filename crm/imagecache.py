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
from django.utils import timezone

from node.models import *
from dj.views import *

for i in goods.objects.all():
    try:
	print i.id, "800\n", i.pict80.url
    except:
	pass
