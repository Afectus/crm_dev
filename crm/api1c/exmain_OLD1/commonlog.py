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

from log.models import *

import warnings
warnings.filterwarnings('ignore', r"DateTimeField .* received a naive datetime", RuntimeWarning, r'django\.db\.models\.fields')


cl=commonlog.objects.create(name='ex1c', desc='обмен 1с')
cl.save()
