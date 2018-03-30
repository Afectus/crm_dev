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


goods.objects.all().update(catalogshow=False) #отключаем все товары

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
		
		if c > 0: #если количество больше 1
			s=stock.objects.filter(id1c=value['СкладКод'], status=True) #берем склад
			if s.exists(): #если склад сущесвует 
				s=s.first() #берем склад
				try: #пробуем взять товар
					g=goods.objects.get(id1c=value['НоменклатураКод'], base=base)
				except:
					print "%s %s NOT FOUND" % (modelname, value['НоменклатураКод'])
				else: #если товар существует
					ccount = ccount + 1 #+1 новое значение на складе
					print "%s %s QINSTOCK CREATE" % (modelname, value['НоменклатураКод'])
					#вяжем количество с товаром
					data=model(stock=s, value=c)
					data.save()
					g.qinstock.add(data)
					g.catalogshow=True #включаем показ в каталоге
					g.save()
		
			else: #если склад не существует
				print "%s %s %s IGNORE STOCK" % (modelname, value['НоменклатураКод'], value['СкладКод'])
		else:
			print "%s %s %s BAD QUANTITY OR ZERO" % (modelname, value['НоменклатураКод'], c)
		
		###END_PROCESS###
		
	func.logfile(i)
	
	#создаем задание для подчиненных скриптов
	#crm2bit4stock.py
	pe=procedureexchange.objects.get(id=56)
	logexchange.objects.filter(procedureexchange=pe).update(success=True) #выключаем старые
	logexchange.objects.create(fname='export to bitrix', success=False, ftime=datetime.datetime.now(), procedureexchange=pe) #создаем новое

	
print "count new %s %s" % (modelname, ccount)
	
	
	
