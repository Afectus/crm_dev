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
Забираем свойства товара
'''

'''
$token='XXXXXXX';
$crc = md5($ORDER_ID.":".$token);
$addurl = Array('bitrixorderid'=>$ORDER_ID, 'crc'=>$crc);
'''


salt = id_generator() #создаем сессию соль
token = makeapitoken(salt) #подписываем соль
#print salt, token


g=goods.objects.filter(idbitrix__isnull=False).exclude(idbitrix__exact='') #товары только с idbitrix, исключаем пустые

for i in g:
	#запрос
	url = 'http://babah24.ru/c/1c/getbname.php?salt=%s&crc=%s&id=%s' % (salt, token, i.idbitrix)
	print url
	r = requests.get(url)
	tmp=r.text
	tmp=tmp.strip()
	tmp=tmp.encode('utf8')
	tmp=tmp.replace("&nbsp", "")
	try:
		root = ET.fromstring(tmp)
	except:
		print "EMPTY"
	else:
		print root[0][0].text, root[0][1].text
		i.bname = root[0][1].text
		if(root[0][2].text):
			i.desc = root[0][2].text
		if(root[0][3].text): #pricenameprefix
			i.pricenameprefix = root[0][3].text
		if(root[0][4].text): #pricename
			i.pricename = root[0][4].text
		i.save()
	
	


