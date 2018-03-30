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
from django.utils import timezone
import csv
import tempfile

from node.models import *


#читаем файл, перекодируем в utf8
tmp=open('/home/ftp1c/FizLiza.csv').read().decode('cp1251').encode('utf8')

#создаем временный файл
f = tempfile.NamedTemporaryFile(delete=False)
#print f.name
f.write(tmp) #пишем открытый файл во временный
f.close()

with open(f.name) as csvfile:
	reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
	for value in reader:
		parent = value['Код']
		try:
			b = buyer.objects.get(id1c=parent)
		except:
			pass
		else:
			n=[1,2,3,4]
			for i in n:
				cname = value['ФИОРебенка%s' % i]
				cbday = value['ДатаРожденияРебенка%s' % i]
				try:
					cbday=datetime.datetime.strptime(cbday,"%d.%m.%Y").date()
				except:
					cbday=None
			
				#print "PARENT %s %s %s" % (parent, cname, cbday)
				#проверяем есть такой ребенок или нет
				cget = child.objects.filter(buyer=b, name=cname, bday=cbday)
				if cget.exists():
					print "EXIST CHILD %s %s %s" % (parent, cname, cbday)
					
				else:
					print "CREATE CHILD %s %s %s" % (parent, cname, cbday)
					try:
						cc = child.objects.create(buyer=b, name=cname, bday=cbday)
					except:
						pass
				

os.unlink(f.name) #удаляем временный файл
print os.path.exists(f.name) #проверяем доступен ли временный файл после удаления