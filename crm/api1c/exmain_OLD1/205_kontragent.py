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
model = kontragent
modelname = model().__class__.__name__
ccount = 0 #количество новых

for i in func.getfilelist(205):
	print i
	for value in func.listcsv(i):
	
		###PROCESS###
		#value['Код']
		#value['Наименование']
		#value['ОсновнойСкладКод']
		#value['ОсновнаяКассаКод']
		#value['ПометкаУдаления']	
		try:
			data=model.objects.get(id1c=value['Код'])
		except:
			print "%s %s CREATE" % (modelname, value['Код'])
			ccount = ccount + 1 #+1 новый товар
			data=model(id1c = value['Код'])
		else:
			print "%s %s EXISTS/UPDATE" % (modelname, value['Код'])
		
		#SAVE
		data.name = value['Наименование']
		data.namefull = value['НаименованиеПолное']
		data.inn = value['ИНН']
		data.kpp = value['КПП']
		data.kodpookpo = value['КодПоОКПО']
		data.urfizlico = value['ЮрФизЛицо']
		data.bankrek = value['БанковскиеРеквизиты']
		data.gpskod = value['ГруппаПолучателейСкидкиКод']
		data.stbank= value['стБанк']
		data.stbik = value['стБИК']
		data.stks = value['стКС']
		data.strs = value['стРС']
		data.pred = value['Представление']
		data.comment = value['Комментарий']
		data.save()

		###END_PROCESS###
		
	func.logfile(i)
	
print "count new %s %s" % (modelname, ccount)
	
	
	










