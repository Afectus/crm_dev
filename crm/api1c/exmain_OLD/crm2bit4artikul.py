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
$token='XXXXX';
$crc = md5($ORDER_ID.":".$token);
$addurl = Array('bitrixorderid'=>$ORDER_ID, 'crc'=>$crc);
'''


salt = id_generator() #создаем сессию соль
token = makeapitoken(salt) #подписываем соль
#print salt, token


'''
Создаем новые продукты в битрикс из crm
'''

#g=goods.objects.filter(idbitrix=5634)
g=goods.objects.filter(idbitrix__isnull=False, status=True).exclude(idbitrix__exact='') #товары только с idbitrix, исключаем пустые

for i in g:
	print i.id, i.idbitrix
	if i.art:
		#try:
		art64=base64.b64encode(i.art.encode('utf-8'))
		#except e:
			#print 11
	else:
		art64=base64.b64encode('0')
		
	print art64
	print "GOOD BASE64 ARTIKUL %s " % (i.idbitrix)
	#запрос
	url = 'http://babah24.ru/c/1c/setartikul.php?salt=%s&crc=%s&id=%s&art=%s' % (salt, token, i.idbitrix, art64)
	#print url
	r = requests.get(url)
	data = r.json()
	print data['res']




