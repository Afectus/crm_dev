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
import csv

import warnings
warnings.filterwarnings('ignore', r"DateTimeField .* received a naive datetime", RuntimeWarning, r'django\.db\.models\.fields')

#import tempfile
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from node.models import *

def getdate(value):
	data=None
	try:
		data=datetime.datetime.strptime(value,"%d.%m.%Y %H:%M:%S")
	except:
		return data
	return data


def myfloat(p):
	if bool(p) is False:
		return 0
	p=float(p.replace(',', '.')) #заменяем , на .
	try:
		p = float(p)
	except:
		return 0
	return p

#
root = '/home/ftp1c/tmp/'
onlyfiles = []
for folder, subs, files in os.walk(root):
	for file in files:
		pattern = re.compile("^(?P<code>\d{3})\_(?P<day>\d{2})\_(?P<mon>\d{2})\_(?P<year>\d{4})\_(?P<h>\d{1,2})\_(?P<m>\d{2})\_(?P<s>\d{2})\_.*$")
		res = pattern.match(file)
		fullpath = os.path.join(folder, file)
		if os.path.isfile(fullpath) and res.group('code') == '001':
			tmp={}
			tmp['root'] = folder
			tmp['file'] = file
			onlyfiles.append(tmp)
#print onlyfiles
#

#
total = len(onlyfiles)
count = 0
icount = 0
isum = 0
ireturn = 0
icountreturn = 0

isum2 = 0
ireturn2 = 0

a= 0

for i in onlyfiles:
	count = count+1

	#print 'READ FILE %s' % count, i['file']
	#читаем файл, перекодируем в utf8
	tmp=open('%s/%s' % (i['root'], i['file'])).read().decode('cp1251').encode('utf8')

	#создаем временный файл
	f = NamedTemporaryFile(delete=False)
	f.write(tmp) #пишем открытый файл во временный
	f.close()
	
	
	#
	#print f.name
	#print "step 1"

	with open(f.name) as csvfile:
		reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
		for value in reader:
		
			mydate=getdate(value['Дата'])	
			#print mydate
		
			if value['Магазин'] == '':
				a=a+1
				c=cashbox.objects.get(id1c=value['Касса'])
				print a, i['file'], '=', value['Магазин'], '=', c, c.shop
		
		
			if value['ВидОперации'] == 'Продажа':
				icount = icount + 1
			elif value['ВидОперации'] == 'Возврат':
				icountreturn = icountreturn + 1
			break
	
	#####################################################
	#print "step 2"
	with open(f.name) as csvfile:
		reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
		for value in reader:
		
			#if value['Магазин'] == '':
			#	print i['file'], value['Магазин']
		
			if value['ВидОперации'] == 'Продажа':
				isum = float(isum) + myfloat(value['Сумма'])
			elif value['ВидОперации'] == 'Возврат':
				ireturn = float(ireturn) + myfloat(value['Сумма'])

	#####################################################
	#print "step 3"
	with open(f.name) as csvfile:
		reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
		for value in reader:
			if value['ВидОперации'] == 'Продажа':
				isum2 = float(isum2) + (myfloat(value['Количество']) * myfloat(value['Цена']) - myfloat(value['Скидка']))
			elif value['ВидОперации'] == 'Возврат':
				ireturn2 = float(ireturn2) + (myfloat(value['Количество']) * myfloat(value['Цена']) - myfloat(value['Скидка']))
	
	
	
	
	#print 'count=', count, 'icount=', icount,  'icountreturn=', icountreturn, 'isum=', isum, 'ireturn=', ireturn, 'isum2=', isum2, 'ireturn2=', ireturn2
	
	os.unlink(f.name) #удаляем временный файл
	#print os.path.exists(f.name) #проверяем доступен ли временный файл после удаления
