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
model = qinstock
modelname = model().__class__.__name__
ccount = 0 #количество новых
base = base1c.objects.get(id=1)

######WARNING####################
#удаляем все остатки по складам и товарам
model.objects.filter(goods__base=base).delete()
#################################

for i in func.getfilelist(203):
	print i
	for value in func.listcsv(i):
	
		###PROCESS###
		#value['НоменклатураКод']
		#value['СкладКод']
		#value['СкладНаименование']
		#value['КоличествоОстаток']
		
		try: #исключение количества
			c = int(value['КоличествоОстаток'])
		except:
			c = 0
			continue
		
		if c < 1: #если количество меньше 1, то устанавливаем 0
			print "%s %s %s BAD QUANTITY" % (modelname, value['НоменклатураКод'], c)
			c = 0
			continue
		
		s=stock.objects.filter(id1c=value['СкладКод'], status=True)
		if not s.exists():
			print "%s %s %s IGNORE STOCK" % (modelname, value['НоменклатураКод'], value['СкладКод'])
			continue
		s=s.first() #берем склад
		

		
		g=goods.objects.get(id1c=value['НоменклатураКод'], base=base)
		if g:
			ccount = ccount + 1 #+1 новый товар
			print "%s %s CREATE" % (modelname, value['НоменклатураКод'])
			
			#вяжем количество с товаром
			data=model(stock=s, value=c)
			data.save()
			g.qinstock.add(data)

		###END_PROCESS###
		
	func.logfile(i)
	
	#создаем задание для подчиненных скриптов
	#crm2bit4stock.py
	pe=procedureexchange.objects.get(id=56)
	logexchange.objects.filter(procedureexchange=pe).update(success=True) #выключаем старые
	logexchange.objects.create(fname='export to bitrix', success=False, ftime=datetime.datetime.now(), procedureexchange=pe) #создаем новое

	#crm2bit4CATALOGSHOW.py
	pe=procedureexchange.objects.get(id=52)
	logexchange.objects.filter(procedureexchange=pe).update(success=True) #выключаем старые
	logexchange.objects.create(fname='export to bitrix', success=False, ftime=datetime.datetime.now(), procedureexchange=pe) #создаем новое
	
print "count new %s %s" % (modelname, ccount)
	
	
	
