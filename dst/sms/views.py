# -*- coding: utf-8 -*- 
from __future__ import unicode_literals

from django.shortcuts import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponsePermanentRedirect

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

from django.utils.encoding import force_text

def sms4b(user, phone, text):
	apilogin = settings.SMS4B_APILOGIN
	apipasswd = settings.SMS4B_APIPASSWD
	apisender = settings.SMS4B_APISENDER
	
	res = 'bad'

	#SOAP 1.2
	mydata=u"""<?xml version="1.0" encoding="utf-8"?><soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope"><soap12:Body><SendSMS xmlns="SMS4B"><Login>%s</Login><Password>%s</Password><Source>%s</Source><Phone>%s</Phone><Text>%s</Text></SendSMS></soap12:Body></soap12:Envelope>""" % (apilogin, apipasswd, apisender, phone, text)

	mydata=mydata.encode('utf-8')
	
	url="https://sms4b.ru/ws/sms.asmx"
	headers = {'Host': 'sms4b.ru', 'Content-Type': 'application/soap+xml; charset=utf-8', 'Content-Length': str(len(mydata))}
	
	r = requests.request('POST', url, data=mydata, headers=headers, verify=False)
	#response = requests.post(url, data=a, headers=headers, verify=False)
	#print response.content

	res = r.text

	
	#POST
	#url1 = 'https://sms4b.ru/ws/sms.asmx/SendSMS'
	#data1 = {'Login': apilogin, 'Password': apipasswd, 'Source': apisender, 'Phone': '89504090320', 'Text': 'test'}
	#r = requests.post(url1, data=data1,)
	#r = requests.request('POST', url1, data=data1, verify=False)
	#r = requests.api.request('post', url1, data=data1, json=None, verify=False)
	#print r.text
	
	#логируем в базу
	csmsreport = smsreport(user=user, phone=phone, text=text, status=res,)
	csmsreport.save()
	
	return res

	
def mobilon(user, phone):
	#{u'callid': u'1489481657.222632', u'code': 0, u'result': u'SUCCESS', u'description': u'Call had been initialised'}
	apitoken = settings.MOBILON_TOKEN
	res = 0
	url = 'https://connect.mobilon.ru/api/call/CallToSubscriber?key=%s&outboundNumber=8%s' % (apitoken, phone)
	r = requests.get(url, verify=False)
	#print r.status_code
	rep = r.json()
	
	#логируем в базу
	ccallreport = callreport(user=user, phone=phone, text=r.status_code, status=rep,)
	ccallreport.save()

	if rep['result'] == 'SUCCESS':
		res = 1
	
	return res
	

#http://crm.babah24.ru/api/sms/send/?phone=9504090320&crc=EE87641127F7D090D0F7DB38B8689775
@csrf_exempt
def apismssend(request):
	if request.method == 'GET' and 'phone' in request.GET and 'crc' in request.GET:
		tmp={'res': 0, 'data': u'error',}
		crc = makeapitoken(request.GET['phone'])
		if crc == request.GET['crc']:
			try:
				u=User.objects.get(username='smsapisend')
			except:
				tmp={'res': 0, 'data': u'NOT FOUND USER smsapisend',}
			else:
				r=sms4b(u, '8%s' % (request.GET['phone']), 'test')
				#print r
				tmp={'res': 1, 'data': u'sms send good',}
	return HttpResponse(json.dumps(tmp), content_type='application/json')