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

import warnings
warnings.filterwarnings('ignore', r"DateTimeField .* received a naive datetime", RuntimeWarning, r'django\.db\.models\.fields')

#import tempfile
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from api1c.models import *




def getfilelist(icode):
	root = '/home/ftp1c/tmp/'
	onlyfiles = []
	for folder, subs, files in os.walk(root):
		for file in files:
			fullpath = os.path.join(folder, file)
			pattern = re.compile("^(?P<code>\d{3})\_.*$")
			code = pattern.match(file).group('code')
			if os.path.isfile(fullpath) and code == icode:
				tmp={}
				tmp['root'] = folder
				tmp['file'] = file
				onlyfiles.append(tmp)
				
	return onlyfiles



os.system('unzip -o -P12345 -d /home/ftp1c/tmp/ /home/ftp1c/upload/*.zip')


for i in procedureexchange.objects.filter(status=True).order_by('-sort'):
	print i.name

	for i in getfilelist(i.code):
		print i['file']
	
	
	
	'''
	a=uploadzip.objects.filter(name=i['file'])
	if a.exists(): #если положительно, чек существует, пропускаем его
		print 'EXIST ZIP %s' % i['file']	
		continue
	else: #если отрицательно, распаковываем
		print 'EXTRACT ZIP %s' % i['file']
		os.sys('unzip -P12345 -d /home/ftp1c/tmp/ /home/ftp1c/upload/*.zip' % (i['file']))
		
		
		
		a=uploadzip.objects.create(name=i['file'])
	#
	
	
	print 'READ FILE %s' % count, i['file']
	#читаем файл, перекодируем в utf8
	tmp=open('%s/%s' % (i['root'], i['file'])).read().decode('cp1251').encode('utf8')

	#создаем временный файл
	f = NamedTemporaryFile(delete=True)
	f.write(tmp) #пишем открытый файл во временный
	f.close()
	

	#ПИШЕМ ЗАГОЛОВОК ЧЕКА, ТОЛЬКО ПЕРВУЮ СТРОКУ, ОСТАЛЬНЫЕ ДУБЛЬ
	with open(f.name) as csvfile:
		reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
		for value in reader:
			print "HEADER %s %s %s" % (value['НомерЧекаККМ'], value['Дата'], value['Цена'])
			
			#берем дату
			getdate=datetime.datetime.strptime(value['Дата'],"%d.%m.%Y %H:%M:%S")	
			
			#костыли
			try: #пробуем взять магазины
				shopget=shop.objects.get(id1c=value['Магазин'])
			except:
				shopget=None
			try: #пробуем взять кассу
				cashboxget=cashbox.objects.get(id1c=value['Касса'])
			except:
				cashboxget=None
			try: #ВидОперации
				value['ВидОперации']
			except:
				operation='sale'
			else:
				if value['ВидОперации'] == 'Продажа':
					operation='sale'
				elif value['ВидОперации'] == 'Возврат':
					operation='return'
				else:
					operation='sale'
			
			##
			#дописываем чек
			c.nckkm=value['НомерЧекаККМ']
			c.time=getdate
			c.shop=shopget #shop=value['Магазин']
			c.cashbox=cashboxget #cashbox=value['Касса']
			c.seller=value['Продавец']
			c.bonuswho=value['ВладелецДисконтнойКартыКод']
			c.nal=myfloat(value['ОплатаНаличные'])
			c.beznal=myfloat(value['ОплатаБезНаличные'])
			c.bonuspay=myfloat(value['ОплатаБонусы'])
			c.bonusadd=myfloat(value['НачислениеБонусов'])
			c.discountcard=value['ДисконтнаяКарта']
			c.operation=operation
			c.save()

			#пишем файл отдельными функциями, для сохранности оригинала
			tmp=open('%s/%s' % (i['root'], i['file'])).read()
			sf = NamedTemporaryFile(delete=True)
			sf.write(tmp)
			sf.flush()
			sf = File(sf)
			c.sourcefile.save(id_generator(), sf)
			#
			
			#вяжем чек с покупателем
			if c.bonuswho: #if c.bonuswho and c.discountcard: #если есть дисконт. карта
				try: #пробуем взять покупателя по id1c
					b=buyer.objects.get(id1c=c.bonuswho)
				except:
					pass
				else:
					#print b
					c.buyer = b #вяжем покупателя
					c.save()
			break #обрываем цикл, остальные строки дубли
	#####################################################
	

	#ПИШЕМ ПОЗИЦИИ ЧЕКА СО СКИДКАМИ
	with open(f.name) as csvfile:
		reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
		for value in reader:
			print "CHECKITEM %s %s %s" % (value['НомерЧекаККМ'], value['Дата'], value['Цена'])

			try: #тестируем на наличие товара по коду 1с
				g=goods.objects.filter(id1c=value['НоменклатураКод']).first()
				#g=goods.objects.get(id1c=value['НоменклатураКод'])
			except:
				g=None
			#ВидОперации
			try: #ВидОперации
				value['ВидОперации']
			except:
				operation='sale'
			else:
				if value['ВидОперации'] == 'Продажа':
					operation='sale'
				elif value['ВидОперации'] == 'Возврат':
					operation='return'
				else:
					operation='sale'

			#ЧЕК ВЗЯТ ИЛИ СОЗДАН В ПЕРЕМЕННОЙ C		
			
			try: #пробуем взять позицию товара с чеком
				ci=checkitem.objects.get(fcheck=c, goods=g)
			except:
				#создаем позицию товара к чеку
				ci=checkitem(
					fcheck=c,
					goods=g,
					col=myfloat(value['Количество']),
					unit=value['ЕдиницаИзмеренияКод'],
					price=myfloat(value['Цена']),
					sum=myfloat(value['Сумма']),
					operation=operation,
					)
				ci.save()
			
			#ПОЗИЦИЯ ЧЕКА В ЛЮБОМ СЛУЧАЕ В ПЕРЕМЕННОЙ ci
				
			#ПИШЕМ СКИДКИ В ПОЗИЦИЮ ci
			discountprice = myfloat(value['Скидка'])
			if discountprice > 0:
				try:
					d=discounts.objects.get(id1c=value['ОписаниеСкидки'])
				except:
					d=None
				#создаем скидку к позиции товара с чеком
				cd=checkd(
					checkitem=ci,
					discounts=d,
					discount=myfloat(value['Скидка']),
					descdiscount=value['ОписаниеСкидки']
					)
				cd.save()
				print "discount=", value['Скидка']
			#####################################################
			
		
	os.unlink(f.name) #удаляем временный файл
	#print os.path.exists(f.name) #проверяем доступен ли временный файл после удаления
	'''