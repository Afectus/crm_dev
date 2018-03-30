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

from .models import *

from django.utils.encoding import force_text

import logging
log = logging.getLogger(__name__)

@csrf_exempt
def mobilon_webhook_call(request):
	tmp={'res': 0, 'data': 'error',}
	if request.method == 'GET' or request.method == 'POST': #and 'phone' in request.GET and 'crc' in request.GET:
		authkey = settings.WEBHOOKAUTHKEY
		if 'authkey' in request.GET and request.GET['authkey'] == authkey:
			data = request.body.decode('utf-8')

			crl=callreportlog.objects.create(route='external', info=request.body.decode('utf-8'))

			try:
				jsondata=json.loads(data)
			except:
				crl.phone='json error'
				crl.incoming_number='json error'
			else:
				crl.phone=str(jsondata['callerid'])[1:]
				crl.phone8=jsondata['callerid']
				crl.incoming_number=jsondata['incoming_number']
			crl.save()
			tmp={'res': 1, 'data': 'webhook_ok',}
		else:
			tmp={'res': 0, 'data': 'authkey_is_bad',}
	return HttpResponse(json.dumps(tmp), content_type='application/json')

	
	
	
	
	
#http://crm.babah24.ru/mobilon/webhook/callback/?authkey=XXXXXX&callerid={CALLERID}&time={TIME}&innumber={INCOMING_NUMBER}
#http://crm.babah24.ru/mobilon/webhook/callback/?authkey=XXXXXX
#‎2050338 to 4
@csrf_exempt
def mobilon_webhook_callback(request):
	tmp={'res': 0, 'data': 'error',}
	if request.method == 'GET' or request.method == 'POST': #and 'phone' in request.GET and 'crc' in request.GET:
		authkey = settings.WEBHOOKAUTHKEY
		if 'authkey' in request.GET and request.GET['authkey'] == authkey:
			data = request.body.decode('utf-8')
			log.info("========mobilon_webhook_callback=======") 
			log.info(data) 
			crl=callreportlog.objects.create(route='callback', info=request.body.decode('utf-8'))

			try:
				jsondata=json.loads(data)
			except:
				crl.phone='json error'
				crl.incoming_number='json error'
			else:
				crl.phone=str(jsondata['callerid'])[1:]
				crl.phone8=jsondata['callerid']
				crl.incoming_number=jsondata['incoming_number']
			crl.save()
			tmp={'res': 1, 'data': 'webhook_callback_ok',}
		else:
			tmp={'res': 0, 'data': 'authkey_is_bad',}
	return HttpResponse(json.dumps(tmp), content_type='application/json')
	

# def mobilon_webhook_call(user, phone):
	# #{u'callid': u'1489481657.222632', u'code': 0, u'result': u'SUCCESS', u'description': u'Call had been initialised'}
	# apitoken = settings.MOBILON_TOKEN
	# res = 0
	# url = 'https://connect.mobilon.ru/api/call/CallToSubscriber?key=%s&outboundNumber=8%s' % (apitoken, phone)
	# r = requests.get(url, verify=False)
	# #print r.status_code
	# rep = r.json()
	
	# #логируем в базу
	# ccallreport = callreport(user=user, phone=phone, text=r.status_code, status=rep,)
	# ccallreport.save()

	# if rep['result'] == 'SUCCESS':
		# res = 1
	
	# return res
	

#http://crm.babah24.ru/api/sms/send/?phone=9504090320&crc=EE87641127F7D090D0F7DB38B8689775
# @csrf_exempt
# def apismssend(request):
	# if request.method == 'GET' and 'phone' in request.GET and 'crc' in request.GET:
		# tmp={'res': 0, 'data': u'error',}
		# crc = makeapitoken(request.GET['phone'])
		# print crc, request.GET['crc']
		# if crc == request.GET['crc']:
			# try:
				# u=User.objects.get(username='smsapisend')
			# except:
				# tmp={'res': 0, 'data': u'NOT FOUND USER smsapisend',}
			# else:
				# r=sms4b(u, '8%s' % (request.GET['phone']), 'test')
				# #print r
				# tmp={'res': 1, 'data': u'sms send good',}
	# return HttpResponse(json.dumps(tmp), content_type='application/json')