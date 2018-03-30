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

os.system('/var/www/crm/api1c/exmain/bit2crm4bname.py')
os.system('/var/www/crm/api1c/exmain/bit2crm4image.py')
os.system('/var/www/crm/api1c/exmain/bit2crm4prop.py')
os.system('/var/www/crm/api1c/exmain/bit2crm4propabc.py')
os.system('/var/www/crm/api1c/exmain/bit2crm4propval.py')
os.system('/var/www/crm/api1c/exmain/bit2crm4section.py')



	
