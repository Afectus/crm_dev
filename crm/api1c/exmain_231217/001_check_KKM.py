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
import json
import tempfile
from django.utils import timezone
#import tempfile
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from api1c.models import *
from node.models import *
import func
model = check
modelname = model().__class__.__name__
ccount = 0 #количество новых
exist = 0
total = len(func.getfilelist('001')) #числовое значение не может начинаться от 0, передаем в ковычках как строка
iter=0

base = base1c.objects.get(id=1)

def getgoods(value):
	data=None
	if value == False:
		return data
	try:
		data=goods.objects.get(base=base, id1c=value)
	except:
		return data
	return data	
	
def getforeign(model, value):
	data=None
	if value == False:
		return data
	try:
		data=model.objects.get(id1c=value)
	except:
		return data
	return data
	
def getchar(value):
	if value == False:
		value=''
	return value

for iterjson in func.getfilelist('001'): #числовое значение не может начинаться от 0, передаем в ковычках как строка
	print iterjson
	iter=iter+1

	#TEST CHECK IF EXIST
	data=model.objects.filter(fname=iterjson)
	if data.exists(): #если положительно, чек существует, пропускаем его
		print 'EXIST CHECK %s' % iterjson
		exist = exist+1
		print "total=%s, iter=%s, exist=%s, new=%s" % (total, iter, exist, ccount)
	else:
		#get json from file
		tmppath = '/home/ftp1c/tmp/'
		fullpath = os.path.join(tmppath, iterjson)
		jsondata=open(fullpath).read() #json body is here
		#
		try:
			data =  json.loads(jsondata)
		except:
			print 'json invalid'
		else:
			print 'valid'
		
			#print jsondata

			#если отрицательно, создаем чек
			print 'CREATE CHECK %s' % iterjson
			ccount = ccount + 1
			print "total=%s, iter=%s, exist=%s, new=%s" % (total, iter, exist, ccount)
		
			#запись чека
			c=check(
				id1c = data['id1c'],
				uuid = data['uuid'],
				nckkm = getchar(data['nckkm']),
				time = datetime.datetime.fromtimestamp(int(data['time'])),
				#лог
				sourcejson = jsondata,
				process = 'invalid',
				methodadd = 'jsonfile',
				fname=iterjson,
			)

			#проверяем является ли чек копией/дублем
			print 'test check on COPY process %s' % (data['uuid'])
			#copytest=check.objects.filter(uuid=data['uuid'], time=datetime.datetime.fromtimestamp(int(data['time'])))
			copytest=check.objects.filter(uuid=data['uuid'])
			if copytest.exists():
				c.process = 'copy'
				c.save()
				print 'CHECK IS COPY'
			else:
				try:
					c.save()
				except Exception as e:
					print 'check is not accept'
				else:
					c.shop = getforeign(shop, data['shop'])
					c.cashbox = getforeign(cashbox, data['cashbox'])
					c.seller = getchar(data['seller'])
					#c.seller = getforeign(seller, data['seller'])
					c.buyer = getforeign(buyer, data['buyer'])
					c.bonuswho = getchar(data['buyer'])
					c.discountcard = getchar(data['discountcard'])
					c.otvetstven = getchar(data['otvetstven'])
					c.operation = getchar(data['operation'])
					c.status = getchar(data['status'])
					c.smena_kkm = getchar(data['smena_kkm'])
					c.checkreturn = getchar(data['checkreturn'])
					c.accept = data['accept']
					c.save()
					
					#print '2'
					#добавляем позиции чека
					if data['checkitem']:
						for i in data['checkitem']:
							ci=checkitem(
								fcheck = c,
								goods = getgoods(i['goods']),
								col = i['col'],
								unit = getforeign(baseunit, i['unit']),
								price = i['price'],
								totaldiscount = i['totaldiscount'],
								sum = i['sum'],
								operation = getchar(data['operation']),
							)
							try:
								ci.save()
							except Exception as e:
								print 'ci.save() error: %s' % (e)
							else:
								#print '3'
								if i['discountlist']:
									#print '4'
									for d in i['discountlist']:
										#print '5'
										#print getforeign(discounts, d['discount'])
										#print d['sum']
										#print d['discount']
										cd=checkd(
											checkitem = ci,
											discounts = getforeign(discounts, d['discount']),
											discount = d['sum'],
											descdiscount = getchar(d['discount']),
										)
										#print '6'
										try:
											cd.save()
										except Exception as e:
											print 'checkd.save() error: %s' % (e)
					#print '7'					
					#пишем оплату
					res = False
					print 'start pay'
					if data['pay']:
						print 'in pay'
						for p in data['pay']:
							print 'item pay %s' % (p['paymethod'])
							if p['paymethod'] == u'000000001':
								c.nal = p['sum']
								c.paym1 = p['sum']
								c.save()
								res = True
								print 'nal %s' % (p['paymethod'])
							if p['paymethod'] == u'ЦО0000003':
								c.beznal = p['sum']
								c.paym2 = p['sum']
								c.save()
								res = True
								print 'beznal %s' % (p['paymethod'])
							if p['paymethod'] == u'ЦО0000002':
								c.bonuspay = p['sum']
								c.paym3 = p['sum']
								c.save()
								res = True
								print 'bonuspay %s' % (p['paymethod'])
							if p['paymethod'] == u'ЦО0000001':
								c.paygiftcert = p['sum']
								c.paym4 = p['sum']
								c.save()
								res = True
								print 'paygiftcert %s' % (p['paymethod'])
					else:
						print 'no pay'
						
						
					#если валидный чек то пишем валид
					if res:
						c.process = 'valid' #'test'
						if 'test' in data and data['test'] == True:
							c.process = 'test'
						c.save()
						print 'check is accept'
					
	func.logfile(iterjson)
	
print "count new %s %s" % (modelname, ccount)
	
	
	
