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
Забираем все свойства из битрикс для инфоблока каталог товаров
'''

'''
$token='XXXXX';
$crc = md5($ORDER_ID.":".$token);
$addurl = Array('bitrixorderid'=>$ORDER_ID, 'crc'=>$crc);
'''


salt = id_generator() #создаем сессию соль
token = makeapitoken(salt) #подписываем соль
#print salt, token



#запрос
url = 'http://babah24.ru/c/1c/getprop.php?salt=%s&crc=%s' % (salt, token)
print url
r = requests.get(url)
tmp=r.text
tmp=tmp.strip()
tmp=tmp.encode('utf8')
root = ET.fromstring(tmp)
for i in root:
	#test multiple
	multiple=False
	if i[3].text == 'Y':
		multiple=True
	#
	try:
		p=properties.objects.get(idbitrix=i[0].text, code=i[1].text)
	except:
		print "CREATE PROPERTIES %s %s %s" % (i[0].text, i[1].text, i[2].text)
		try:
			properties.objects.create(idbitrix=i[0].text, code=i[1].text, name=i[2].text, multiple=multiple)
		except:
			pass
	else:
		p.multiple=multiple
		p.save()



