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

from node.models import *

from dj.views import *



'''
$token='XXX';
$crc = md5($ORDER_ID.":".$token);
$addurl = Array('bitrixorderid'=>$ORDER_ID, 'crc'=>$crc);
'''


salt = id_generator() #создаем сессию соль
token = makeapitoken(salt) #подписываем соль
#print salt, token



g=goods.objects.filter(idbitrix__isnull=False).exclude(idbitrix__exact='') #товары только с idbitrix, исключаем пустые
#g=goods.objects.filter(idbitrix=5592) #отладка

#g=g.filter(qinstock__value__gte=1).distinct()

for i in g:
	print i.id, i.idbitrix
	value = i.qinstock.aggregate(s=Sum('value'), c=Count('value'))
	
	if value['s'] >= 1 and not None:
		i.status=True
		i.save()
		print 'col=',value['s'], 
	
		#запрос
		url = 'http://babah24.ru/c/1c/setstatus.php?salt=%s&crc=%s&id=%s&value=%s' % (salt, token, i.idbitrix, 'Y')
		print url
		r = requests.get(url)
		data = r.json()
		print data['res']





