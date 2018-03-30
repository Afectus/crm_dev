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

from dj.views import *


#создаем задание, для засекания времени выгрузки
pe=procedureexchange.objects.get(id=56)
logexchange.objects.filter(procedureexchange=pe).update(success=True) #выключаем старые
lex=logexchange.objects.create(target='goodsinstock', fname='export to bitrix', success=False, ftime=datetime.datetime.now(), procedureexchange=pe) #создаем новое
#



print "delete old file"
os.system('find /home/ftp1c/test/upload/ -mindepth 1 -type f -mmin +360 -delete')
os.system('find /home/ftp1c/test/tmp/ -mindepth 1 -type f -mmin +360 -delete')
print "end delete old file"

print "unzip file"
os.system('for z in /home/ftp1c/test/upload/*.zip; do unzip -o -P12345 -d /home/ftp1c/test/tmp/ $z; done')
print "end unzip file"

base = base1c.objects.get(id=1)

tmppath = '/home/ftp1c/test/tmp'

def maketaskone(code=0):
	print tmppath
	for folder, subs, files in os.walk(tmppath):
		for file in files:
			lex=logexchange.objects.filter(fname=file)
			if not lex.exists():
				pattern = re.compile("^(?P<code>\d{3})\_(?P<day>\d{2})\_(?P<mon>\d{2})\_(?P<year>\d{4})\_(?P<h>\d{1,2})\_(?P<m>\d{2})\_(?P<s>\d{2})\_(?P<target>[A-Za-z0-9\_]+)\.(?P<ext>[A-Za-z0-9]+)$")
				res = pattern.match(file)
				date=datetime.datetime(int(res.group('year')), int(res.group('mon')), int(res.group('day')), int(res.group('h')), int(res.group('m')), int(res.group('s')))
				#print res.group('code'), code, type(res.group('code')), type(code)
				
				if str(res.group('code')) == str(code):
					try: #пробуем взять обработку
						pex = procedureexchange.objects.get(code=res.group('code'), status=True)
					except:
						print "PROCEDUREEXCHANGE NOT FOUND %s" % res.group('code')
					else:
						print "MAKE TASK %s" % file
						lex, lexcreated = logexchange.objects.get_or_create(target=res.group('target'), fname=file, success=False, ftime=date, procedureexchange=pex)
			else:
				print "EXISTS TASK %s" % file
	#закрываем mono задания по старой дате
	print "DISABLE DOUBLES"
	try: #пробуем взять обработку
		pex = procedureexchange.objects.get(code=code, status=True, mono=True)
	except:
		pass
	else:
		#удаляем с пустыми target
		logexchange.objects.filter(procedureexchange=pex, target__exact='').delete()
		#удаляем с target='Centraljnay_ostatki'
		logexchange.objects.filter(procedureexchange=pex, target__exact='Centraljnay_ostatki').update(success=True)
		#
		data = logexchange.objects.filter(procedureexchange=pex).values('target').annotate(a=Count('target')).order_by('target')
		for i in data:
			print i
			lex=logexchange.objects.filter(procedureexchange=pex, target__exact=i['target'])
			if lex.exists(): #если моно событие то берем по последней дате
				print "DISABLE DOUBLE %s" % lex
				lexmono=lex.order_by('-ftime').first() #берем одно задание
				print lexmono.procedureexchange.code, lexmono.ftime
				lex.exclude(id=lexmono.id).update(success=True)
		
	#
	return True


#print "start maketaskone"
maketaskone(203)
#print "endstart maketaskone"



def listcsv(name):
	fullpath = os.path.join('/home/ftp1c/test/tmp', name)
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



	
	
	
	
for i in logexchange.objects.filter(procedureexchange__code=203, success=False):
	#print i.target, i.fname
	
	
	#очистка отстатков складов
	if i.target == 'Svobodnyj_ostatki':
		print i.target
		goodsinstock.objects.filter(stock__id1c='ЦО0000005', goods__base=base).update(value=0)
	if i.target == 'Dommer_ostatki':
		print i.target
		goodsinstock.objects.filter(stock__id1c='ЦО0000004', goods__base=base).update(value=0)
	if i.target == 'Planeta_ostatki':
		print i.target
		goodsinstock.objects.filter(stock__id1c='ЦО0000007', goods__base=base).update(value=0)
	if i.target == 'Mega_ostatki':
		print i.target
		goodsinstock.objects.filter(stock__id1c='ЦО0000002', goods__base=base).update(value=0)
	if i.target == 'Govorova_ostatki':
		print i.target
		goodsinstock.objects.filter(stock__id1c='ЦБ0000004', goods__base=base).update(value=0)
	if i.target == 'Semafornay_ostatki':
		print i.target
		goodsinstock.objects.filter(stock__id1c='ЦО0000001', goods__base=base).update(value=0)
	if i.target == 'Acinsk_ostatki':
		print i.target
		goodsinstock.objects.filter(stock__id1c='ЦБ0000001', goods__base=base).update(value=0)
	#	
	
	for value in listcsv(i.fname):
	
		###PROCESS###
		#value['НоменклатураКод']
		#value['СкладКод']
		#value['СкладНаименование']
		#value['КоличествоОстаток']
		#
		try: #исключение количества
			c = int(value['КоличествоОстаток'])
		except:
			c = 0
		#
		if c > 0: #если количество больше 1
			s=stock.objects.filter(id1c=value['СкладКод'], status=True) #берем склад
			if s.exists(): #если склад сущесвует 
				s=s.first() #берем склад
				try: #пробуем взять товар
					g=goods.objects.get(id1c=value['НоменклатураКод'], base=base)
				except:
					print "%s NOT FOUND" % (value['НоменклатураКод'])
				else: #если товар существует
					pass
					try:
						gin=goodsinstock.objects.get(stock=s, goods=g)
					except:
						print "CREATE goodsinstock %s %s" % (value['НоменклатураКод'], value['СкладНаименование'])
						gin=goodsinstock(stock=s, goods=g, value=c)
						gin.save()
						g.catalogshow=True #включаем показ в каталоге
						g.save()
					else:
						print "UPDATE goodsinstock %s %s" % (value['НоменклатураКод'], value['СкладНаименование'])
						#вяжем количество с товаром
						gin.value=c
						gin.save()
						g.catalogshow=True #включаем показ в каталоге
						g.save()
			else: #если склад не существует
				print "%s %s IGNORE STOCK" % (value['НоменклатураКод'], value['СкладКод'])
			###END_PROCESS###
		
	func.logfile(i.fname)
	
#############################################################
#################### ОТПРАВЛЯЕМ НА САЙТ #####################
#############################################################	


salt = id_generator() #создаем сессию соль
token = makeapitoken(salt) #подписываем соль
g=goods.objects.filter(idbitrix__isnull=False).exclude(idbitrix__exact='') #товары только с idbitrix, исключаем пустые
#g=goods.objects.filter(idbitrix=30722) #отладка

for i in g:
	url = 'http://babah24.ru/c/1c/set_1.php?salt=%s&crc=%s&id=%s' % (salt, token, i.idbitrix)

	url = '%s&price=%s' % (url, i.price) #добавляем цену

	#общее количество товаров
	col=0
	for ii in i.goodsinstock_set.filter().exclude(stock__idbitrix__exact=''):
		col = col + ii.value

	if col >= 0:	
		url = '%s&col=%s' % (url, col) #добавляем общее количество
	else:
		url = '%s&col=%s' % (url, 0) #добавляем общее количество
	
	#значения на складах		
	for ii in i.goodsinstock_set.filter().exclude(stock__idbitrix__exact=''):
		ii.value
		if ii.value >= 0:
			url = '%s&col%s=%s' % (url, ii.stock.idbitrix, ii.value)
		else:
			url = '%s&col%s=%s' % (url, ii.stock.idbitrix, 0)

	#CATALOGSHOW
	value = i.goodsinstock_set.filter().exclude(stock__idbitrix__exact='').aggregate(s=Sum('value'), c=Count('value'))
	
	#i.catalogshow = False #отключил, включаю вручную
	if value['s'] >= 1 and not None:
		#i.catalogshow = True #отключил, включаю вручную
		url = '%s&catalogshow=%s' % (url, 1)
	else:
		url = '%s&catalogshow=%s' % (url, 0)

		
	#ШТРИХКОД
	data = i.barcodelist_set.filter(unit='шт')
	if data.exists():
		barcode = data.first().barcode
		url = '%s&barcode=%s' % (url, barcode) #добавляем штрих	
		
	
	#выполнение
	print url
	r = requests.get(url)
	print r.status_code
	#print r.encoding
	#print r.text
	print r.json()

	
lex.endexectime=datetime.datetime.now()
lex.success=True #закрываем задание
lex.save()
	
