# -*- coding: utf-8 -*- 
from __future__ import unicode_literals

from django.shortcuts import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404, get_list_or_404
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
from acl.models import *
from node.models import *

from django.utils.encoding import force_text

from acl.views import get_object_or_denied


#@method_decorator(permission_required('order.add_order'), name='dispatch')
class call_traceback_list(ListView):
	template_name = 'call_traceback_list.html'
	model = callreportlog
	paginate_by = 10
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'call_traceback', 'L') #проверяем права
		return super(call_traceback_list, self).dispatch(request, *args, **kwargs)
	
	def get_queryset(self):
		data=super(call_traceback_list, self).get_queryset().order_by('-ctime')
		
		data=data.extra(select={'f': "select f from node_buyer where phone=call_callreportlog.phone limit 1"}).extra(select={'i': "select i from node_buyer where phone=call_callreportlog.phone limit 1"}).extra(select={'o': "select o from node_buyer where phone=call_callreportlog.phone limit 1"}).extra(select={'bday': "select bday from node_buyer where phone=call_callreportlog.phone limit 1"}).values('id', 'ctime', 'route', 'incoming_number', 'phone', 'f', 'i', 'o', 'bday').order_by('-ctime')
		
		return data
	
	def get_context_data(self, *args, **kwargs):
		context_data = super(call_traceback_list, self).get_context_data(*args, **kwargs)
		#context_data.update({'projects': projects.objects.filter(status=True)})
		return context_data



class call_traceback_detail(DetailView):
	model = callreportlog
	template_name = 'call_traceback_detail.html'

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'call_traceback', 'R') #проверяем права
		return super(call_traceback_detail, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context_data = super(call_traceback_detail, self).get_context_data(*args, **kwargs)
		self.data=super(call_traceback_detail, self).get_object()
		#log.debug(self.data.phone)
		context_data.update({'buyer': buyer.objects.filter(phone=self.data.phone)})
		context_data.update({'check': check.objects.filter(buyer__phone=self.data.phone).order_by('-time')[:10]})
		return context_data	
		
		

# def mobilon1(user, phone):
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