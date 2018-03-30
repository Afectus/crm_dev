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
from order.models import *

from dj.views import *



#удаляем предыдущие заказы
order.objects.filter(phone='9504090320').delete()


id = id_generator() #тестовый номер заказа
phone = '9504090320'
crc = makeapitoken(id) #подписываем соль

#запрос
url = 'http://crm.babah24.ru/api/order/add/?id=%s&phone=%s&crc=%s' % (id, phone, crc)
print(url)
r = requests.get(url)
#print r.encoding
#print r.text
data = r.json()
print(data)
#print r.status_code, url, data['res'], data['status'], data['demo'], data['video'], data['touchscreen']


#update order
url = 'http://crm.babah24.ru/api/order/update/'
print(url)
r = requests.post(url, data={'id':id, 'crc': crc, 'uname': 'Тестовый заказ', 'city': '3912', 'addr': '9 мая 79/2', 'discont': '123456', 'comment': 'Комментарий', 'terminal': True, 'cart': 'Тестовая корзина с товарами', })
#print r.encoding
#print r.text
data = r.json()
print(data)
#print r.status_code, url, data['res'], data['status'], data['demo'], data['video'], data['touchscreen']