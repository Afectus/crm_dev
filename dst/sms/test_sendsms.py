#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, django

projecthome = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
Забираем имя видео файлов из битрикс для каждого товара
Забираем значение "Показывать в демо" для каждого товара
'''

'''
$token='XXXXXXXXX';
$crc = md5($ORDER_ID.":".$token);
$addurl = Array('bitrixorderid'=>$ORDER_ID, 'crc'=>$crc);
'''


phone = '9504090320' #создаем сессию соль
crc = makeapitoken(phone) #подписываем соль
#print salt, token

#запрос
url = 'http://crm.babah24.ru/api/sms/send/?phone=%s&crc=%s' % (phone, crc)
print url
r = requests.get(url)
#print r.encoding
#print r.text
data = r.json()
#print r.status_code, url, data['res'], data['status'], data['demo'], data['video'], data['touchscreen']


