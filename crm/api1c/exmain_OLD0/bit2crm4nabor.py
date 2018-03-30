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

from node.models import *

from dj.views import *

'''
наборы
'''

'''
$token='XXXX';
$crc = md5($ORDER_ID.":".$token);
$addurl = Array('bitrixorderid'=>$ORDER_ID, 'crc'=>$crc);
'''


salt = id_generator() #создаем сессию соль
token = makeapitoken(salt) #подписываем соль
#print salt, token



#запрашиваем активные наборы
url = 'http://babah24.ru/c/1c/getnabor.php?salt=%s&crc=%s&a=%s' % (salt, token, 1)
print url
r = requests.get(url)
data = r.json()
#print data

for i in data['data']:
	#ставим активность, если товар является набором
	try:
		n=goods.objects.get(idbitrix=i['ID'])
	except:
		print "FAIL NABOR IS NOT CREATE ID=%s" % (i['ID'])
	else:
		print "CREATE LINK NABOR BITRIX TO CRM ID=%s" % (i['ID'])
		n.nabor=True
		n.save()
		
	
	

#убираем связь всех товаров с наборами
goods.objects.all().update(naborparent=None)

#выбираем только наборы
g=goods.objects.filter(idbitrix__isnull=False, status=True, nabor=True).exclude(idbitrix__exact='') #товары только с idbitrix, исключаем пустые, только наборы

for i in g:
	#запрос
	url = 'http://babah24.ru/c/1c/getnabor.php?salt=%s&crc=%s&id=%s' % (salt, token, i.idbitrix)
	print url
	r = requests.get(url)
	# #print r.encoding
	#print r.text
	data = r.json()
	for elementid in data['data']:
		print elementid
		try:
			g=goods.objects.get(idbitrix=elementid)
		except:
			print "FAIL %s -> %s" % (elementid, i)
		else:
			print "LINK %s -> %s" % (elementid, i)
			g.naborparent=i
			g.save()


