#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, django


import time
import requests
import datetime
import re
import string
import random
import md5
import hashlib
import json

from dj.views import *


#salt = id_generator() #случайность
crc = makeapitoken(id) #подписываем соль

tmp=[]


for folder, subs, files in os.walk('/home/exchange/FTP/videomp4/'):
	for file in files:
		#print file
		pattern = re.compile("^(?P<id>\d+).*$")
		res = pattern.match(file)
		try:
			res.group('id')
		except:
			pass
		else:
			print(res.group('id'))
			
			
			tmp.append({'id': res.group('id'), 'name': file})

		
print(json.dumps(tmp))
#запрос
crc = makeapitoken(res.group('id')) #подписываем соль
url = 'http://crm.babah24.ru/api/goods/video/edit/?id=%s&crc=%s' % (res.group('id'), crc)
print(url)
#r = requests.post(url, data=json.dumps(tmp), timeout=335)
#print r.encoding
#print r.text
data = r.json()
#print data
print(r.status_code)
			


