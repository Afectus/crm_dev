# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.http import HttpResponsePermanentRedirect

from django.core.exceptions import PermissionDenied


from django.contrib.auth.models import User, Group

import json
from django.core import serializers

from django.http import QueryDict

from django.views.generic import DetailView, ListView, DeleteView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.base import TemplateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator

import datetime, time
from django.utils import timezone

from django.db.models import Sum, Count
from django.db.models import Q

from django import forms

from django.views.decorators.csrf import csrf_exempt

#from node.templatetags.nodetags import node_count

from node.models import *
from dj.views import *

from .func import *

import logging
log = logging.getLogger(__name__)

	
	

def getgoods(value):
	base = base1c.objects.get(id=1)
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
	
	
#http://crm.babah24.ru/api/1c/check/add/?salt=5555&crc=92C2931D23D23148D051F21134E73807
@csrf_exempt
def api_1c_check_add(request):
	log.info('\n')
	log.info('start=%s' % (request.get_full_path()))
	#log.info('request.body=%s' % request.body)
	tmp={'res': False, 'data': 'fail',}
	if request.method == 'POST' or request.method == 'GET':
		crc = makeapitoken_1c(request.GET['salt'])
		if crc.lower() == request.GET['crc'].lower():
			#log.info('crc accept')
			try:
				data =  json.loads(request.body.decode("utf-8"))
				#data =  json.loads(request.body)
			except:
				log.info('json invalid')
				pass
			else:
				#log.info('request.body=%s' % request.body)
				#log.info(type(request.body))
				#log.info(type(data))
				
				log.info('json valid')
				if True: #data['res'] == False: #debug
					#log.info('request.body=%s' % request.body)
					#######################################
					#отбиваемся от старых чеков
					if 'tovari' in data:
						log.info('DROP old check')
						return HttpResponse(json.dumps({'res': True, 'data': 'check is accept',}), content_type='application/json')
					else:
						log.info('ACCEPT new check %s %s' % (data['id1c'], data['uuid']))

					#######################################
					#запись чека
					c=check(
						id1c = data['id1c'],
						uuid = data['uuid'],
						nckkm = getchar(data['nckkm']),
						time = datetime.datetime.fromtimestamp(int(data['time'])),
						#лог
						sourcejson = data, #request.body,
						process = 'invalid',
						methodadd = 'jsonapi',
					)
					#проверяем является ли чек копией/дублем
					log.info('test check on COPY process %s' % (data['uuid']))
					#copytest=check.objects.filter(uuid=data['uuid'], time=datetime.datetime.fromtimestamp(int(data['time'])))
					copytest=check.objects.filter(uuid=data['uuid'])
					if copytest.exists():
						c.process = 'copy'
						c.save()
						log.info('CHECK IS COPY')
						tmp={'res': True, 'data': 'check is accept',}
						return HttpResponse(json.dumps(tmp), content_type='application/json')
					else:
						try:
							c.save()
						except Exception as e:
							tmp={'res': False, 'data': 'check is not accept',}
							#log.info('tmp %s' % (e))
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
							
							#log.info('2')
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
										log.info('ci.save() error: %s' % (e))
									else:
										#log.info('3')
										if i['discountlist']:
											#log.info('4')
											for d in i['discountlist']:
												#log.info('5')
												#log.info(getforeign(discounts, d['discount']))
												#log.info(d['sum'])
												#log.info(d['discount'])
												cd=checkd(
													checkitem = ci,
													discounts = getforeign(discounts, d['discount']),
													discount = d['sum'],
													descdiscount = getchar(d['discount']),
												)
												#log.info('6')
												try:
													cd.save()
												except Exception as e:
													log.info('checkd.save() error: %s' % (e))
							#log.info('7')						
							#пишем оплату
							res = False
							log.info('start pay')
							if data['pay']:
								log.info('in pay')
								for p in data['pay']:
									log.info('item pay %s' % (p['paymethod']))
									if p['paymethod'] == u'000000001':
										c.nal = p['sum']
										c.paym1 = p['sum']
										c.save()
										res = True
										log.info('nal %s' % (p['paymethod']))
									if p['paymethod'] == u'ЦО0000003':
										c.beznal = p['sum']
										c.paym2 = p['sum']
										c.save()
										res = True
										log.info('beznal %s' % (p['paymethod']))
									if p['paymethod'] == u'ЦО0000002':
										c.bonuspay = p['sum']
										c.paym3 = p['sum']
										c.save()
										res = True
										log.info('bonuspay %s' % (p['paymethod']))
									if p['paymethod'] == u'ЦО0000001':
										c.paygiftcert = p['sum']
										c.paym4 = p['sum']
										c.save()
										res = True
										log.info('paygiftcert %s' % (p['paymethod']))
							else:
								log.info('no pay')
								
								
							#если валидный чек то пишем валид
							if res:
								c.process = 'valid' #'test'
								if 'test' in data and data['test'] == True:
									c.process = 'test'
								c.save()
								tmp={'res': True, 'data': 'check is accept',}
								log.info(tmp)

	#log.info('HttpResponse=%s' % tmp)
	log.info('end')
	return HttpResponse(json.dumps(tmp), content_type='application/json')	




@csrf_exempt
def api1c_getcert(request):
	log.info('start=api1c_getcert')
	log.info('url=%s' % request.get_full_path())
	log.info('request.body=%s' % request.body)
	#if request.method == 'GET' and 'crc' in request.GET:
	if request.method == 'POST' or request.method == 'GET':
		data = request.body
		#data = data.split(';')
		data = json.loads(data)
		g=goods.objects.filter(id1c__in=data['id'], base__id=int(data['base']))
		if g.exists():
			log.info('res=%s' % 'exists')
			###mod g text cert
			for i in g:
				if i.goodscert:
					pass
				else: #если нет сертификата, то прописываем от второго товара
					try:
						r=relgoods.objects.get(b=i)
					except:
						pass
					else:
						#log.info('makecertpdf=%s' % r.a)
						#log.info('makecertpdf=%s' % r.a.goodscert)
						if r.a.goodscert:
							#merger.append(r.a.goodscert.pdf.path)
							i.goodscert=r.a.goodscert
						else:
							pass
			
			###
			xlsurl, xlspath, pdfpath = makecertexcel(data['head'], g)

			#print xlsurl
			#print xlspath
			#print pdfpath
			
			pdfurl = makecertpdf(g, pdfpath)
			#print pdfurl
			return HttpResponse('%s' % (pdfurl))
	return HttpResponse('fail')
	

@csrf_exempt
def api1c_getcert_json(request):
	log.info('start=api1c_getcert_json')
	log.info('url=%s' % request.get_full_path())
	log.info('request.body=%s' % request.body)
	tmp={'res': False, 'data': 'fail',}
	#if request.method == 'GET' and 'crc' in request.GET:
	if request.method == 'POST' or request.method == 'GET':
		log.info('api1c_getcert_json=POST')
		data = request.body
		data = json.loads(data)
		log.info('api1c_getcert_json=json parse goods')
		try:
			g=goods.objects.get(id1c=data['id'], base__id=1)
		except:
			tmp={'res': False, 'data': 'goods not found',}
		else:
			#tmp={'res': False, 'data': 'goods found',}
			if g.goodscert:
				tmp={
					'res': True, 
					'number': g.goodscert.name, 
					'period': '%s-%s' % (g.goodscert.datestart.strftime('%d.%m.%Y'), g.goodscert.dateend.strftime('%d.%m.%Y')),
					'author': g.goodscert.org,
					'url': 'http://crm.babah24.ru%s' % g.goodscert.pdf.url,
					}
			else:
				tmp={'res': False, 'data': 'cert not found',}
	return HttpResponse(json.dumps(tmp), content_type='application/json')	

	
	
#http://crm.babah24.ru/api/1c/getcurtime/?salt=5555&crc=92C2931D23D23148D051F21134E73807
@csrf_exempt
def api_1c_getcurtime(request):
	#log.info('start=api_1c_getcurtime')
	tmp={'res': False, 'data': 'fail',}
	if request.method == 'POST' or request.method == 'GET':
		crc = makeapitoken_1c(request.GET['salt'])
		if crc.lower() == request.GET['crc'].lower():
			dtnow=datetime.datetime.now()
			dtiso=dtnow.isoformat()
			dtunix=time.mktime(dtnow.timetuple())
			tmp={'res': True, 'iso': dtiso, 'unix': dtunix,}
	return HttpResponse(json.dumps(tmp), content_type='application/json')	
	
	
	
	

# @csrf_exempt
# def api1c_addc(request):
	# #if request.method == 'GET' and 'crc' in request.GET:
	# if request.method == 'POST' or request.method == 'GET':
		# print "============request==========="
		# print request
		# print "============GET==========="
		# print request.GET
		# print "============POST==========="
		# print request.POST
		# print "============FILES==========="
		# print request.FILES
		# print "============BODY==========="
		# print request.body
		# #crc = makeapitoken(mac)
		# #print crc, request.GET['crc']
		# #if crc == request.GET['crc']:
		# #tmp={'res': 1, 'data': u'set ip good',}
		# #return HttpResponse(json.dumps(tmp), content_type='application/json')
		# return HttpResponse('success')
		
	# #tmp={'res': 0, 'data': u'bad',}
	# #return HttpResponse(json.dumps(tmp), content_type='application/json')
	# return HttpResponse('fail')
