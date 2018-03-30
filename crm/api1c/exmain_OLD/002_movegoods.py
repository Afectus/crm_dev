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
import csv
import tempfile
from django.utils import timezone

from api1c.models import *
from node.models import *
import func
model = movegoods
modelname = model().__class__.__name__
ccount = 0 #количество новых
base = base1c.objects.get(id=1)

for i in func.getfilelist(002):
	print i
	for value in func.listcsv(i):
	
		###PROCESS###
		#value['Дата']
		#value['Номер']
		#value['КонтрагентКод']
		#value['НоменклатураКод']
		#value['ЕдиницаИзмеренияКод']
		#value['Количество']
		#value['Цена']
		#value['Сумма']
		#value['СкладКод']
		#value['Комментарий']
		#value['ОтветственныйКод']
		#value['Проведен']

		g=goods.objects.get(id1c=value['НоменклатураКод'], base=base)
		
		data=model.objects.filter(id1c=value['Номер'], goods=g)
		if not data.exists():
			print "%s %s CREATE" % (modelname, value['Номер'])
			ccount = ccount + 1
			data=model(id1c=value['Номер'])
			
			#SAVE
			data.hozoperation=func.getforeign(hozoperation, '000000002')
			data.atime=func.getdate(value['Дата'])
			data.fstock=func.getforeign(stock, value['СкладКод'])
			data.kontragent=func.getforeign(kontragent, value['КонтрагентКод'])
			data.goods=g
			data.unit=func.getforeign(baseunit, value['ЕдиницаИзмеренияКод'])
			data.col=func.getfloat(value['Количество'])
			data.price=func.getfloat(value['Цена'])
			data.sum=func.getfloat(value['Сумма'])
			data.comment=value['Комментарий']
			data.who=value['ОтветственныйКод']
			data.carried=func.getbool(value['Проведен'])
			data.save()
		else:
			print "%s %s EXISTS/UPDATE" % (modelname, value['Номер'])
				

	func.logfile(i)
	
print "count new %s %s" % (modelname, ccount)
	
	
	
