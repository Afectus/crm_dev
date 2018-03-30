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
model = barcodelist
modelname = model().__class__.__name__
ccount = 0 #количество новых
base = base1c.objects.get(id=1)

count = 0

for i in func.getfilelist(219):
	print(i)
	for value in func.listcsv(i):
		count = count + 1
		###PROCESS###
		#value['ВладелецКод']
		#value['Штрихкод']
		#value['ЕдиницаИзмерения']
		#value['ТипШтрихкода']
		#value['ТипШтрихкодаКод']
		#value['ТипВладельца']

		#FIRST - GET BARCODE TO GOODS
		print(count, value['ТипВладельца'], value['ВладелецКод'].strip())
		if value['ТипВладельца'] == 'Номенклатура':
			
			pdata = goods.objects.get(id1c=value['ВладелецКод'], base=base)
			#
			try:
				data=model.objects.get(goods=pdata, barcode=value['Штрихкод'])
			except:
				print("%s %s CREATE" % (modelname, value['ВладелецКод']))
				ccount = ccount + 1
				data=model()
				data.goods=pdata
			else:
				print("%s %s EXISTS/UPDATE" % (modelname, value['ВладелецКод']))
			#SAVE
			data.barcode=value['Штрихкод']
			data.unit=value['ЕдиницаИзмерения']
			data.typebar=value['ТипШтрихкода']
			data.typebarcode=value['ТипШтрихкодаКод']
			data.typewho=value['ТипВладельца']
			data.save()
		##################################
		
		#NEXT - GET BARCODE TO DISCOUNTCARD->BUYER

		# if value['ТипВладельца'] == 'Информационные карты':
			# #print value['ТипВладельца'], value['ВладелецКод'].strip()
			# try:
				# pdata = discountcard.objects.get(id1c=value['ВладелецКод'].strip())
			# except:
				# continue
			# #
			# try:
				# data=model.objects.get(discountcard=pdata, barcode=value['Штрихкод'].strip())
			# except:
				# print "%s %s CREATE" % (modelname, value['ВладелецКод'].strip())
				# ccount = ccount + 1
				# data=model()
				# data.discountcard=pdata
			# else:
				# print "%s %s EXISTS/UPDATE" % (modelname, value['ВладелецКод'])
			
			# #SAVE
			# data.barcode=value['Штрихкод']
			# data.unit=value['ЕдиницаИзмерения']
			# data.typebar=value['ТипШтрихкода']
			# data.typebarcode=value['ТипШтрихкодаКод']
			# data.typewho=value['ТипВладельца']
			# data.save()
		
	func.logfile(i)
	
print("count new %s %s" % (modelname, ccount))
	
	
	
