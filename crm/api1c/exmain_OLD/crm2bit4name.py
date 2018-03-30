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

from django.utils.html import escape


'''
$token='XXXXX';
$crc = md5($ORDER_ID.":".$token);
$addurl = Array('bitrixorderid'=>$ORDER_ID, 'crc'=>$crc);
'''


salt = id_generator() #создаем сессию соль
token = makeapitoken(salt) #подписываем соль
#print salt, token


'''
—оздаем новые продукты в битрикс из crm
'''

#g=goods.objects.filter(id1c__in=['ЦБ000000219', 'ЦБ000000223', 'ЦБ000000222', 'ЦБ000000221', 'ЦБ000000220', 'ЦБ000000214', 'ЦБ000000218', 'ЦБ000000217', 'ЦБ000000216', 'ЦБ000000215'])

#g=goods.objects.filter(idbitrix='37933')

#for i in g: print i.namefull, i.idbitrix



for i in g:
	print i.id, i.idbitrix
	if i.namefull:
		name = escape(i.namefull)
		name64=base64.b64encode(name.encode('utf-8'))
	else:
		name64=base64.b64encode('0')
		
	print name64
	print "GOOD name64 name64 %s " % (i.idbitrix)
	#запрос
	url = 'http://babah24.ru/c/1c/setname.php?salt=%s&crc=%s&id=%s&name=%s' % (salt, token, i.idbitrix, name64)
	print url
	r = requests.get(url)
	data = r.json()
	print data['res']




