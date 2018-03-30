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
from func import *

salt=990110
crc = makeapitoken_1c(salt) #подписываем соль


data={'salt': salt, 'crc': crc, 'res': False}


data={
        "salt": 863935,
        "crc": "e7b417c03cda6bd29515369137fe9983",
        "res": True,
        "number": "ЦБИПК000074",
        "date": 1512359413,
        "shop": "ЦБ0000003",
        "kassa": "ЦБ0000004",
        "manager": "         ",
        "otvetstven": "         ",
        "vid_operacii": "Продажа",
        "status": "",
        "smena_kkm": "0",
        "nomer_cheka_kkm": "2 768",
        "client": "",
        "vozvrat_cheka": "",
        "card": "",
        "proveden": True,
        "tovari": {
                "1": {
                        "key": 1,
                        "tovar": "ЦБ000000092",
                        "kol": 1,
                        "ed_izm": "ЦБ0000092",
                        "cena": 900,
                        "skidka": 1
                },
                "2": {
                        "key": 2,
                        "tovar": "ЦБ000000263",
                        "kol": 1,
                        "ed_izm": "ЦБ0000277",
                        "cena": 1400,
                        "skidka": 1
                },
                "3": {
                        "key": 3,
                        "tovar": "ТС000000004",
                        "kol": 1,
                        "ed_izm": "ТС0000004",
                        "cena": 0.01,
                        "skidka": 1
                }
        },
        "skidki": {
                "1": {
                        "key": 1,
                        "skidka": "000000055",
                        "summa": 252
                },
                "2": {
                        "key": 2,
                        "skidka": "000000055",
                        "summa": 392
                }
        },
        "oplati": {
                "1": {
                        "vid_oplati": "000000001",
                        "summa": 1633
                }
        },
        "podarki": {}
}



data={
	"salt": 863935,
	"crc": "e7b417c03cda6bd29515369137fe9983",
	"res": False,
	"number": "ЦБИПК000074",
	"date": 1512359413,
	"shop": u'ЦБ0000003',
	"kassa": "ЦБ0000004",
	"manager": "         ",
	"otvetstven": "         ",
	"vid_operacii": "Продажа",
	"status": "",
	"smena_kkm": "0",
	"nomer_cheka_kkm": "2 768",
	"client": "",
	"vozvrat_cheka": "",
	"card": "",
	"proveden": True,
	"tovari": [
		{
			"tovar": "ЦБ000000092",
			"kol": 1,
			"ed_izm": "ЦБ0000092",
			"cena": 900,
			"skidka": [
				{
						"key": 1,
						"skidka": "000000055",
						"summa": 252
				},
				{
						"key": 2,
						"skidka": "000000055",
						"summa": 392
				}
				],
		},
		{
			"key": 2,
			"tovar": "ЦБ000000263",
			"kol": 1,
			"ed_izm": "ЦБ0000277",
			"cena": 1400,
			"skidka": False
		},
		{
			"key": 3,
			"tovar": "ТС000000004",
			"kol": 1,
			"ed_izm": "ТС0000004",
			"cena": 0.01,
			"skidka": False
		}
		],
        "oplati": {
			"1": {
					"vid_oplati": "000000001",
					"summa": 1633
			}
        },
        "podarki": {}
}





# print "CHECK=%s" % (data['number'])
# for i in data['tovari']:
	# print '-CHECKITEM=%s' % (i['tovar'])
	# if  i['skidka'] != False:
		# for d in i['skidka']:
			# print '--DISCOUNT=%s,%s' % (d['skidka'], d['summa'])


data = """
{
        "salt": 300961,
        "crc": "a2acd96d574959c83ab19770dee3168a",
        "res": false,
        "id1c": "ЦБ000000007",
        "time": 1512569716,
        "shop": "ЦО0000006",
        "cashbox": "ЦО0000010",
        "seller": "000000001",
        "otvetstven": "000000001",
        "operation": "sale",
        "status": false,
        "smena_kkm": 0,
        "nckkm": 4,
        "buyer": false,
        "checkreturn": false,
        "discountcard": false,
        "accept": true,
        "checkitem": [
                {
                        "goods": "ЦБ000000012",
                        "col": 1,
                        "unit": "ЦБ0000012",
                        "price": 21000,
                        "totaldiscount": 0,
                        "sum": 15540,
                        "discountlist": [
                                {
                                        "discount": "000000029",
                                        "sum": 5460
                                }
                        ]
                },
                {
                        "goods": "ЦО000000935",
                        "col": 1,
                        "unit": "ЦО0000932",
                        "price": 25000,
                        "totaldiscount": 0,
                        "sum": 18500,
                        "discountlist": [
                                {
                                        "discount": "000000029",
                                        "sum": 6500
                                }
                        ]
                }
        ],
        "pay": [
                {
                        "paymethod": "000000001",
                        "sum": 34040
                }
        ],
        "gift": []
}
"""	
			
			

data=json.dumps(data)
print data


#запрос
url = 'http://crm.babah24.ru/api/1c/check/add/?salt=%s&crc=%s' % (salt, crc)
print url
r = requests.post(url, data=data)
#print r.encoding
#print r.text
data = r.json()
print data
#print r.status_code, url, data['res'], data['status'], data['demo'], data['video'], data['touchscreen']
