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


yn=raw_input("unzip? Y or N:")

yn=yn.lower()

if yn == 'y':
	func.unzip() #1 - UNZIP ARCHIVE
	
#создаем задания
func.maketask()

	
