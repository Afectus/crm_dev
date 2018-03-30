# -*- coding: utf-8 -*- 
from __future__ import unicode_literals

from django.shortcuts import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse

from django.core.exceptions import PermissionDenied

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django import forms
from django.contrib.auth.models import User, Group

import json
from django.core import serializers

from django.http import QueryDict

from django.views.generic import DetailView, ListView, DeleteView
from django.views.generic.edit import FormView, UpdateView
from django.views.generic.base import TemplateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator

import datetime, time

from django.db.models import Sum, Count, Q, IntegerField
from django.db.models.functions import Cast

from django.views.decorators.csrf import csrf_exempt

import urllib
import re
import requests

from django.conf import settings

from sms.models import *
from sms.views import *

from notify.models import *
from notify.views import *

from django.utils.encoding import force_text

from .models import *
from panel.models import *

from django.core.mail import send_mail


import logging
log = logging.getLogger(__name__)



@csrf_exempt
def api_order_add(request):
	DEBUG=False
	log.info('api_order_add start')
	r='DEBUG' #для отладки sms4b
	if request.method == 'POST':
		tmp={'res': 0, 'data': u'request method is POST',}
	if request.method == 'GET' and 'crc' in request.GET and 'id' in request.GET and 'phone' in request.GET:
		tmp={'res': 0, 'data': u'error',}
		crc = makeapitoken(request.GET['id'])
		#print crc.lower(), request.GET['crc'].lower()
		if crc.lower() == request.GET['crc'].lower():
			#CREATE ORDER
			o=order.objects.create(phone=request.GET['phone'], bitrixorderid=request.GET['id'], )
			oe=orderevent.objects.create(order=o, event='add', comment='add script from bitrix')
			#START SEND SMS TO MANAGERS
			value='Новый заказ на сайте #%s crm.babah24.ru/order/detail/%s' % (o.bitrixorderid, o.id)
			today = datetime.date.today()
			#####################
			######TELEGRAMM#######
			#####################
			om=ordermanager.objects.filter(handler='telegram', schedule=today.isoweekday()).order_by('-sort')
			nh=notifyhandler.objects.get(name='telegram')
			for i in om:
				#print i.handler, i.user, i.schedule, i.sort
				"""
				DEBUGGER
				"""
				if DEBUG == False:
					nq=notifyqueue.objects.create(user=i.user, handler=nh, value=value)
					oe=orderevent.objects.create(order=o, event='telegram', comment='add telegram message for manager %s "%s" in notify queue' % (i, value), info='id %s in notifyqueue' % (nq.id))
				else:
					oe=orderevent.objects.create(order=o, event='telegram', comment='add telegram message for manager %s "%s" in notify queue' % (i, value), info=r)
				"""
				END DEBUGGER
				"""
			#####################
			######SEND SMS#######
			#####################
			#select managers, max 3
			om=ordermanager.objects.filter(handler='sms4b', schedule=today.isoweekday()).order_by('-sort')[:3]
			for i in om:
				#print i.user, i.schedule, i.sort
				#send sms
				mphone=profileuser.objects.get(user=i.user).phone
				"""
				DEBUGGER
				"""
				if DEBUG == False:
					r=sms4b(None, '8%s' % (mphone), value)
				"""
				END DEBUGGER
				"""
				# #create order event on own sms
				oe=orderevent.objects.create(order=o, event='sms', comment='send sms to manager %s "%s"' % (i, value), info=r)
			#####################
			#####################
			#####################
			#START SEND SMS TO BUYER
			value='Ваш заказ #%s принят' % (o.bitrixorderid)
			"""
			DEBUGGER
			"""
			#r=sms4b(None, '8%s' % (o.phone), value)
			"""
			END DEBUGGER
			"""
			# #create order event on own sms
			oe=orderevent.objects.create(order=o, event='sms', comment='send sms to buyer %s "%s"' % (request.GET['phone'], value), info=r)
			# #RESULT
			tmp={'res': 1, 'data': u'order_add_good',}
	log.info('api_order_add end')
	return HttpResponse(json.dumps(tmp), content_type='application/json')



class Form_order(forms.ModelForm):
	class Meta:
		model = order
		fields = ['uname', 'city', 'addr', 'discont', 'comment', 'terminal', 'cart',]

@csrf_exempt
def api_order_update(request):
	tmp={'res': 0, 'data': u'error',}
	if request.method == 'POST' and 'crc' in request.POST and 'id' in request.POST:
		crc = makeapitoken(request.POST['id'])
		#print crc.lower(), request.POST['crc'].lower()
		if crc.lower() == request.POST['crc'].lower():
			#print request.POST
			form = Form_order(request.POST)
			if form.is_valid():
				o=order.objects.filter(bitrixorderid=request.POST['id']).first()
				o.uname=form.cleaned_data['uname']
				o.city=form.cleaned_data['city']
				o.addr=form.cleaned_data['addr']
				o.discont=form.cleaned_data['discont']
				o.comment=form.cleaned_data['comment']
				o.terminal=form.cleaned_data['terminal']
				o.cart=form.cleaned_data['cart']
				o.save()
				oe=orderevent.objects.create(order=o, event='update', comment='update script from bitrix')
				tmp={'res': 1, 'data': u'order_update_good',}
			else:
				#print "form not valid"
				#print form.errors.as_json()
				tmp={'res': 0, 'data': form.errors.as_json(),}
	return HttpResponse(json.dumps(tmp), content_type='application/json')

	

@csrf_exempt
def api_order_callback(request):
	r='1' #для отладки sms4b
	if request.method == 'POST':
		tmp={'res': 0, 'data': u'request method is POST',}
	if request.method == 'GET' and 'crc' in request.GET and 'phone' in request.GET and 'id' in request.GET:
		tmp={'res': 0, 'data': u'error',}
		crc = makeapitoken(request.GET['phone'])
		#print crc.lower(), request.GET['crc'].lower()
		if crc.lower() == request.GET['crc'].lower():
			#CREATE ORDER
			o=order.objects.create(phone=request.GET['phone'], bitrixorderid=request.GET['id'])
			oe=orderevent.objects.create(order=o, event='add', comment='add script from bitrix')
			#START SEND SMS TO MANAGERS
			value='Новый заказ (обратный звонок) на сайте #%s crm.babah24.ru/order/detail/%s' % (o.bitrixorderid, o.id)
			today = datetime.date.today()
			#####################
			######TELEGRAMM#######
			#####################
			om=ordermanager.objects.filter(handler='telegram', schedule=today.isoweekday()).order_by('-sort')
			nh=notifyhandler.objects.get(name='telegram')
			for i in om:
				#print i.handler, i.user, i.schedule, i.sort
				nq=notifyqueue.objects.create(user=i.user, handler=nh, value=value)
				oe=orderevent.objects.create(order=o, event='telegram', comment='add telegram message for manager %s "%s" in notify queue' % (i, value), info='id %s in notifyqueue' % (nq.id))
			#####################
			######SEND SMS#######
			#####################
			#select managers, max 3
			today = datetime.date.today()
			om=ordermanager.objects.filter(handler='sms4b', schedule=today.isoweekday()).order_by('-sort')[:3]
			for i in om:
				#print i.user, i.schedule, i.sort
				#send sms
				mphone=profileuser.objects.get(user=i.user).phone
				r=sms4b(None, '8%s' % (mphone), value)
				#create order event on own sms
				oe=orderevent.objects.create(order=o, event='sms', comment='send sms to manager %s "%s"' % (i, value), info=r)
			#####################
			#####################
			#####################	
			#START SEND SMS TO BUYER #пока не отправляем смс клиенту об обратном звонке
			#value='Ваш заказ #%s принят' % (o.bitrixorderid)
			#r=sms4b(None, '8%s' % (o.phone), value)
			#create order event on own sms
			#oe=orderevent.objects.create(order=o, event='sms', comment='send sms to buyer %s "%s"' % (request.GET['phone'], value), info=r)
			#RESULT
			tmp={'res': 1, 'data': u'order_callback_good',}
	return HttpResponse(json.dumps(tmp), content_type='application/json')







	
	
@csrf_exempt
def api_order_test(request):
	#tmp={'res': 0, 'data': u'error',}
	if request.method == 'GET':
		import subprocess
		r = subprocess.call("/usr/bin/python /var/www/crm/order/test_orderadd.py", shell=True)
		#tmp={'res': 1, 'data': u'order_test_good',}
	return HttpResponseRedirect(reverse('order:list'))
	#return HttpResponse(json.dumps(tmp), content_type='application/json')	
	

'''

@csrf_exempt
def order_add(request):
	tmp={'res': 0, 'data': u'Ошибка',}
	if request.method == 'POST' or request.method == 'GET':	
		#debug
		# form = Form_order(request.GET)
		# print form.is_valid()
		# print form.errors.as_data()
		
		#тут проверим token
		crc = hashlib.md5()
		token = 'XXXXXXXX'
		bitrixorderid = request.POST['bitrixorderid'].strip()
		crc.update("%s:%s" % (request.POST['bitrixorderid'], token,))
		print '=',request.POST['bitrixorderid'],'='
		crc=crc.hexdigest()
		crc2=request.POST['crc'] #пришел шифр
		print "crc =", crc, " - ", "crc2", "=", crc2
		if crc.upper() == crc2.upper():
			print request.POST
			####
			form = Form_order(request.POST)
			if form.is_valid():
				print "form is valid"
				o=order.objects.create(uname=form.cleaned_data['uname'], phone=form.cleaned_data['phone'], city=form.cleaned_data['city'], addr=form.cleaned_data['addr'], discont=form.cleaned_data['discont'], comment=form.cleaned_data['comment'], terminal=form.cleaned_data['terminal'], bitrixorderid=bitrixorderid, )
				tmp={'res': 1, 'form': u'valid', 'crmorderid': o.id,}
			else:
				print "form not valid"
				print form.errors.as_json()
				tmp={'res': 0, 'form': form.errors.as_json(),}
	return HttpResponse(json.dumps(tmp), content_type='application/json')
	
	
@csrf_exempt
def order_update(request, pk):
	tmp={'res': 0, 'data': u'Ошибка',}
	if request.method == 'POST' or request.method == 'GET':
		#print request.GET
		#тут проверим token
		crc = hashlib.md5()
		token = 'XXXXXXXX'
		crc.update("%s:%s" % (request.GET['bitrixorderid'], token,))
		crc=crc.hexdigest()
		crc2=request.GET['crc'] #пришел шифр
		#print "crc =", crc, " - ", "crc2", "=", crc2
		if crc.upper() == crc2.upper():
			#print "CRC IS GOOD"
			data = get_object_or_404(order, id=pk)
			data.bitrixorderid=request.GET['bitrixorderid']
			data.save()
		
			tmp={'res': 1, 'data': u'crc is good and bitrix order id is set',}
		else:
			tmp={'res': 0, 'data': u'crc is bad',}

	return HttpResponse(json.dumps(tmp), content_type='application/json')
	
	
	
@csrf_exempt
def order_notify(request):
	if request.method == 'GET' and 'crc' in request.GET and 'id' in request.GET:
		tmp={'res': 0, 'data': u'error',}
		crc = makeapitoken(request.GET['id'])
		print crc, request.GET['crc']
		if crc == request.GET['crc']:
			try:
				u=User.objects.get(username='smsordereventsend')
			except:
				tmp={'res': 0, 'data': u'NOT FOUND USER smsordereventsend',}
			else:
				phone='9504090320'
				value='Новый заказ на сайте #%s' % (request.GET['id'])
				r=sms4b(u, '8%s' % (phone), value)
				
				orderevent.objects.create(user=u, event='sms', comment='%s - %s' % (value, r))
				#print r
				tmp={'res': 1, 'data': u'order_notify_good',}
	return HttpResponse(json.dumps(tmp), content_type='application/json')
'''




'''
#notify_manager(order, )
def notify_manager(o, message):
	#START SEND SMS TO MANAGERS
	value='Новый заказ (обратный звонок) на сайте #%s crm.babah24.ru/order/detail/%s' % (o.bitrixorderid, o.id)
	today = datetime.date.today()
	#####################
	######TELEGRAMM#######
	#####################
	om=ordermanager.objects.filter(handler='telegram', schedule=today.isoweekday()).order_by('-sort')
	nh=notifyhandler.objects.get(name='telegram')
	for i in om:
		#print i.handler, i.user, i.schedule, i.sort
		nq=notifyqueue.objects.create(user=i.user, handler=nh, value=value)
		oe=orderevent.objects.create(order=o, event='telegram', comment='add telegram message for manager %s "%s" in notify queue' % (i, value), info='id %s in notifyqueue' % (nq.id))
	#####################
	######SEND SMS#######
	#####################
	#select managers, max 3
	today = datetime.date.today()
	om=ordermanager.objects.filter(handler='sms4b', schedule=today.isoweekday()).order_by('-sort')[:3]
	for i in om:
		#print i.user, i.schedule, i.sort
		#send sms
		mphone=profileuser.objects.get(user=i.user).phone
		r=sms4b(None, '8%s' % (mphone), value)
		#create order event on own sms
		oe=orderevent.objects.create(order=o, event='sms', comment='send sms to manager %s "%s"' % (i, value), info=r)
	#####################
	#####################
	#####################	
	#START SEND SMS TO BUYER #пока не отправляем смс клиенту об обратном звонке
	#value='Ваш заказ #%s принят' % (o.bitrixorderid)
	#r=sms4b(None, '8%s' % (o.phone), value)
	#create order event on own sms
	#oe=orderevent.objects.create(order=o, event='sms', comment='send sms to buyer %s "%s"' % (request.GET['phone'], value), info=r)
	#RESULT
'''


