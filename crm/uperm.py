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


from django.contrib.auth.models import User, Group

u=User.objects.filter(is_superuser=False)

for i in u:
	print "---------------------------------"
	print i.username
	for p in i.get_all_permissions():
		print p







