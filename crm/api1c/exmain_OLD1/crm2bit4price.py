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

from api1c.models import *
from node.models import *
import func

from dj.views import *



'''
$token='XXX';
$crc = md5($ORDER_ID.":".$token);
$addurl = Array('bitrixorderid'=>$ORDER_ID, 'crc'=>$crc);
'''


salt = id_generator() #создаем сессию соль
token = makeapitoken(salt) #подписываем соль
#print salt, token
procedureexchangeid=55

'''
Создаем новые продукты в битрикс из crm
'''

lex = logexchange.objects.filter(procedureexchange__id=procedureexchangeid, success=False)

if lex.exists():
	g=goods.objects.filter(idbitrix__isnull=False).exclude(idbitrix__exact='') #товары только с idbitrix, исключаем пустые
	#g=goods.objects.filter(idbitrix=37792)

	for i in g:
		print "SET PRICE %s TO ID %s " % (i.price, i.idbitrix)
		#запрос
		url = 'http://babah24.ru/c/1c/setprice.php?salt=%s&crc=%s&id=%s&price=%s' % (salt, token, i.idbitrix, i.price)
		print url
		r = requests.get(url)
		data = r.json()
		print "RES %s" % data['res']

logexchange.objects.filter(procedureexchange__id=procedureexchangeid).update(success=True) #выключаем старые


