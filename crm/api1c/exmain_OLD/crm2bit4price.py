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

import xml.etree.ElementTree as ET

from node.models import *

from dj.views import *



'''
$token='XXXXX';
$crc = md5($ORDER_ID.":".$token);
$addurl = Array('bitrixorderid'=>$ORDER_ID, 'crc'=>$crc);
'''


salt = id_generator() #������� ������ ����
token = makeapitoken(salt) #����������� ����
#print salt, token


'''
������� ����� �������� � ������� �� crm
'''

g=goods.objects.filter(idbitrix__isnull=False).exclude(idbitrix__exact='') #������ ������ � idbitrix, ��������� ������
#g=goods.objects.filter(idbitrix=37792)

for i in g:
	print "SET PRICE %s TO ID %s " % (i.price, i.idbitrix)
	#������
	url = 'http://babah24.ru/c/1c/setprice.php?salt=%s&crc=%s&id=%s&price=%s' % (salt, token, i.idbitrix, i.price)
	print url
	r = requests.get(url)
	data = r.json()
	print "RES %s" % data['res']




