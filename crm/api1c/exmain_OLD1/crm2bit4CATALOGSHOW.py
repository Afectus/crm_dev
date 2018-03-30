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

import base64

import xml.etree.ElementTree as ET

from api1c.models import *
from node.models import *
import func

from dj.views import *



'''
$token='XXXXXXX';
$crc = md5($ORDER_ID.":".$token);
$addurl = Array('bitrixorderid'=>$ORDER_ID, 'crc'=>$crc);
'''


salt = id_generator() #������� ������ ����
token = makeapitoken(salt) #����������� ����
#print salt, token
procedureexchangeid=52

lex = logexchange.objects.filter(procedureexchange__id=procedureexchangeid, success=False)

if lex.exists():

	g=goods.objects.filter(idbitrix__isnull=False).exclude(idbitrix__exact='') #������ ������ � idbitrix, ��������� ������
	#g=goods.objects.filter(idbitrix=5592, status=True) #�������

	#g=g.filter(qinstock__value__gte=1).distinct()

	for i in g:
		print i.id, i.idbitrix
		value = i.qinstock.aggregate(s=Sum('value'), c=Count('value'))
		
		i.catalogshow = False
		if value['s'] >= 1 and not None:
			i.catalogshow = True
		
		print value, value['s'], 
		
		#������
		url = 'http://babah24.ru/c/1c/setCATALOGSHOW.php?salt=%s&crc=%s&id=%s&value=%s' % (salt, token, i.idbitrix, 'Y')
		print url
		r = requests.get(url)
		data = r.json()
		print data['res']


	#�������� �� �������
	'''
	for i in g:
		print i.id, i.idbitrix
		
		value = i.qinstock.aggregate(s=Sum('value'), c=Count('value'))
		
		res = 'N'
		if value['s'] >= 1 and not None:
			res = 'Y'
		
		print value, value['s'], res
		
		
		#������
		url = 'http://babah24.ru/c/1c/setCATALOGSHOW.php?salt=%s&crc=%s&id=%s&value=%s' % (salt, token, i.idbitrix, res)
		print url
		r = requests.get(url)
		data = r.json()
		print data['res']
	'''


logexchange.objects.filter(procedureexchange__id=procedureexchangeid).update(success=True) #��������� ������
