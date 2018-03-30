#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, django

projecthome = '/var/www/crm/'
if projecthome not in sys.path:
    sys.path.append(projecthome)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj.settings")
django.setup()



from django.core.files import File
from django.core.files.temp import NamedTemporaryFile


import time
import urllib2
import requests
import datetime
from django.utils import timezone

from node.models import *

from dj.views import *


'''
Забираем картинки для каждого товара
'''

'''
$token='XXXXXX';
$crc = md5($ORDER_ID.":".$token);
$addurl = Array('bitrixorderid'=>$ORDER_ID, 'crc'=>$crc);
'''


salt = id_generator() #создаем сессию соль
token = makeapitoken(salt) #подписываем соль
#print salt, token


g=goods.objects.filter(idbitrix__isnull=False).exclude(idbitrix__exact='') 
#g=goods.objects.filter(idbitrix=37663) #TEST
#товары только с idbitrix, исключаем пустые

for i in g:
	#запрос
	url = 'http://babah24.ru/c/1c/getimage.php?salt=%s&crc=%s&id=%s' % (salt, token, i.idbitrix)
	print url
	r = requests.get(url)
	#print r.encoding
	#print r.text
	data = r.json()
	
	#вяжем картинку
	try:
		data['pict']
	except:
		pass
	else:
		if data['pict']:
			print data['pict']
			#print r.status_code, url, data['res'], data['pict']
			img_temp = NamedTemporaryFile(delete=True)
			img_temp.write(urllib2.urlopen('http://babah24.ru%s' % data['pict']).read())
			img_temp.flush()

			f = File(img_temp)
			#f.size
			############i.pict.save(id_generator(), f)
			try:
				i.pict.size #если у товара уже есть картинка
			except: #нет картинки, создаем
				print 'CREATE %s ' % (data['pict'])
				i.pict.save(id_generator(), f)
			else: #если есть картинка
				if i.pict.size != f.size:
					print 'EXIST %s %s' % (i.pict.size, f.size)
					i.pict.save(id_generator(), f)
				else:
					print 'DUPLICATE %s %s' % (i.pict.size, f.size)
			
	
	


