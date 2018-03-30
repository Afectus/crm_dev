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

import warnings
warnings.filterwarnings('ignore', r"DateTimeField .* received a naive datetime", RuntimeWarning, r'django\.db\.models\.fields')

import tempfile
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from api1c.models import *


tmppath = '/home/ftp1c/tmp/'


def unzip():
	#os.system('unzip -o -P12345 -d %s /home/ftp1c/upload/*.zip' % tmppath)
	os.system('for z in /home/ftp1c/upload/*.zip; do unzip -o -P12345 -d /home/ftp1c/tmp/ $z; done')
	return True

	
#создает задания в logexchange
def maketask(maketaskpath=tmppath):
	#logexchange.objects.all().delete()
	for folder, subs, files in os.walk(maketaskpath):
		for file in files:	
			lex=logexchange.objects.filter(fname=file)
			if not lex.exists():
				pattern = re.compile("^(?P<code>\d{3})\_(?P<day>\d{2})\_(?P<mon>\d{2})\_(?P<year>\d{4})\_(?P<h>\d{1,2})\_(?P<m>\d{2})\_(?P<s>\d{2})\_.*$")
				res = pattern.match(file)
				date=datetime.datetime(int(res.group('year')), int(res.group('mon')), int(res.group('day')), int(res.group('h')), int(res.group('m')), int(res.group('s')))
				try: #пробуем взять обработку
					pex = procedureexchange.objects.get(code=res.group('code'), status=True)
				except:
					print "EXISTS TASK %s" % file
				else:
					print "MAKE TASK %s" % file
					lex, lexcreated = logexchange.objects.get_or_create(fname=file, success=False, ftime=date, procedureexchange=pex)
					
					
					if res.group('code') != '001': #если не чек, то пишем файл
						#пишем файл отдельными функциями, для сохранности оригинала
						tmp=open('%s%s' % (maketaskpath, file)).read()
						sf = NamedTemporaryFile(delete=True)
						sf.write(tmp)
						sf.flush()
						sf = File(sf)
						lex.sourcefile.save(file, sf)
						sf.close()
					
	
	#закрываем mono задания по старой дате
	print "DISABLE DOUBLES"
	for i in procedureexchange.objects.filter(status=True, mono=True):
		lex = i.logexchange_set.filter()
		if lex.exists() and lex.count() > 1: #если моно событие то берем по последней дате
			print "DISABLE DOUBLE %s" % lex
			lexmono=lex.order_by('-ftime').first() #берем одно задание
			print lexmono.procedureexchange.code, lexmono.ftime
			lex.exclude(id=lexmono.id).update(success=True)
	
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

def listcsv(name):
	fullpath = os.path.join(tmppath, name)
	print fullpath
	#читаем файл, перекодируем в utf8
	tmp=open(fullpath).read().decode('cp1251').encode('utf8')
	
	#создаем временный файл
	f = tempfile.NamedTemporaryFile(delete=False)
	f.write(tmp) #пишем открытый файл во временный
	f.close()

	arcsv = []
	with open(f.name, 'rU') as csvfile:
		reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
		for value in reader:
			arcsv.append(value)
	
	os.unlink(f.name) #удаляем временный файл
	return arcsv
	
	
def logfile(name):
	print 'logfile %s' % (name)
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