#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, django

projecthome = '/var/www/crm/'
if projecthome not in sys.path:
    sys.path.append(projecthome)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj.settings")
django.setup()

from django.db.models import Sum, Count
from django.db.models import Q

import time
import requests
import datetime
from django.utils import timezone
import csv

import codecs

import warnings
warnings.filterwarnings('ignore', r"DateTimeField .* received a naive datetime", RuntimeWarning, r'django\.db\.models\.fields')

import tempfile
from django.core.files import File

from api1c.models import *


def maketask(code=0, filepath='/home/ftp1c/tmp'):
	for folder, subs, files in os.walk(filepath):
		for file in files:
			#print(file)
			lex=logexchange.objects.filter(fname=file)
			if not lex.exists():
				pattern = re.compile("^(?P<code>\d{3})\_(?P<day>\d{2})\_(?P<mon>\d{2})\_(?P<year>\d{4})\_(?P<h>\d{1,2})\_(?P<m>\d{2})\_(?P<s>\d{2})\_(?P<target>[A-Za-z0-9]+)\_(?P<target2>[A-Za-z0-9\-\_]+)\.(?P<ext>[A-Za-z0-9]+)$")
				res = pattern.match(file)
				date=datetime.datetime(int(res.group('year')), int(res.group('mon')), int(res.group('day')), int(res.group('h')), int(res.group('m')), int(res.group('s')))
				#print res.group('code'), code, type(res.group('code')), type(code)
				
				if str(res.group('code')) == str(code):
					try: #пробуем взять обработку
						pex = procedureexchange.objects.get(code=res.group('code'), status=True)
					except:
						print("PROCEDUREEXCHANGE NOT FOUND %s" % res.group('code'))
					else:
						print("MAKE TASK %s" % file)
						lex, lexcreated = logexchange.objects.get_or_create(target=res.group('target'), fname=file, success=False, ftime=date, procedureexchange=pex)
						print(lex, lexcreated)
			else:
				print("EXISTS TASK %s" % file)
	#закрываем mono задания по старой дате
	print("DISABLE DOUBLES")
	try: #пробуем взять обработку
		pex = procedureexchange.objects.get(code=code, status=True, mono=True)
	except:
		pass
	else:
		#удаляем с пустыми target
		#logexchange.objects.filter(procedureexchange=pex, target__exact='').delete()
		#
		#удаляем с target='Centraljnay'
		logexchange.objects.filter(procedureexchange__code=203, target__exact='Centraljnay').delete()#.update(success=True)
		#удаляем все кроме target='Centraljnay'
		logexchange.objects.filter().exclude(procedureexchange__code=203).exclude(target__exact='Centraljnay').delete()#.update(success=True)
		#

		
		data = logexchange.objects.filter(procedureexchange=pex).values('target').annotate(a=Count('target')).order_by('target')
		for i in data:
			print(i)
			lex=logexchange.objects.filter(success=False, procedureexchange=pex, target__exact=i['target'])
			if lex.exists(): #если моно событие то берем по последней дате
				print("DISABLE DOUBLE %s" % lex)
				lexmono=lex.order_by('-ftime').first() #берем одно задание
				print(lexmono.procedureexchange.code, lexmono.ftime)
				lex.exclude(id=lexmono.id).delete()#.update(success=True)
		
	#
	return True


	
	
#читает задания из logexchange
def getfilelist(icode):
	onlyfiles = []
	try: #пробуем взять обработку
		pex = procedureexchange.objects.get(code=icode, status=True)
	except:
		return onlyfiles

	for i in logexchange.objects.filter(procedureexchange=pex, success=False):
		onlyfiles.append(i.fname)
	return onlyfiles

def listcsv(name, filepath='/home/ftp1c/tmp'):
	fullpath = os.path.join(filepath, name)
	print(fullpath)
	#читаем файл, перекодируем в utf8
	#tmp=open(fullpath).read().decode('cp1251').encode('utf8') #python2
	#tmp=codecs.open(fullpath, encoding='cp1251').read()
	#tmp=open(fullpath).read()
	
	#print(tmp)
	
	#создаем временный файл
	# f = tempfile.NamedTemporaryFile(delete=False)
	# f.write(tmp) #пишем открытый файл во временный
	# f.close()

	tmp=codecs.open(fullpath, encoding='cp1251').readlines()
	
	arcsv = []
	
	reader = csv.DictReader(tmp, delimiter=';', quotechar='"')
	for value in reader:
		arcsv.append(value)
	
	# with open(fullpath, 'rU') as csvfile:
		# reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
		# for value in reader:
			# arcsv.append(value)
	
	#os.unlink(f.name) #удаляем временный файл
	return arcsv
	
	
def logfile(name):
	print('logfile %s' % (name))
	lex = logexchange.objects.filter(success=False, fname=name)
	lex.update(success=True)
	return True
	

	
#FIELDS_TRANSFORM_GET
def getforeign(model, value):
	data=None
	try:
		data=model.objects.get(id1c=value)
	except:
		return data
	return data
	
def getdate(value):
	data=None
	try:
		data=datetime.datetime.strptime(value,"%d.%m.%Y %H:%M:%S")
	except:
		return data
	return data

def getbool(value):
	data=False
	if value == 'Да':
		data=True
	return data

def getfloat(value):
	if bool(value) is False:
		return 0
	value=float(value.replace(',', '.')) #заменяем , на .
	try:
		value = float(value)
	except:
		return 0
	return value
	


#####################