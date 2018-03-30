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

class Form_order(forms.ModelForm):
	class Meta:
		model = order
		fields = ['uname', 'city', 'addr', 'discont', 'comment', 'terminal',]

#print request.POST
#form = Form_order(request.POST)
#if form.is_valid():
#else:
#print "form not valid"
#print form.errors.as_json()
#tmp={'res': 0, 'data': form.errors.as_json(),}

@csrf_exempt
def api_order_update_json(request):
	log.info('api_order_update_json start')
	tmp={'res': 0, 'data': u'error',}
	if request.method == 'POST':
		try:
			data = json.loads(request.body.decode("utf-8"))
		except:
			log.info('json invalid')
			tmp={'res': 0, 'data': u'json error',}
		else:
			crc = makeapitoken(data['orderid'])
			#print crc.lower(), request.POST['crc'].lower()
			#log.info(crc.lower(), '==', data['crc'].lower())
			if crc.lower() == data['crc'].lower():
				log.info('api_order_update2 crc ok')
				log.info(data)
				o=order.objects.filter(bitrixorderid=data['orderid']).first()
				o.sourcejson=json.dumps(data, indent=4)
				o.save()
				o.uname=data['uname']#form.cleaned_data['uname']
				o.city=data['city']#form.cleaned_data['city']
				o.addr=data['addr']#form.cleaned_data['addr']
				o.discont=data['discountcard']#form.cleaned_data['discont']
				o.comment=data['comment']#form.cleaned_data['comment']
				o.terminal=data['terminal']#form.cleaned_data['terminal']
				o.save()
				oe=orderevent.objects.create(order=o, event='update', comment='update script from bitrix (/api2/order/update_json/?id=)')
				#добавляем товар к заказу
				if 'cartlist' in data:
					for i in data['cartlist']:
						ocart = ordercartlist(
							order = o,
							name = i['name'],
							price = i['price'],
							col = i['col'],
							discount_price = i['discount_price'],
							comment = i['comment'],
							#unit = i['unit'],
							#currency = i['currency'],
							#order_price = i['order_price'],
							)
						ocart.save()
						#пишем товар в позицию заказа
						try:
							g=goods.objects.get(idbitrix=i['id'])
						except:
							pass
						else:
							ocart.goods = g
							ocart.save()

				tmp={'res': 1, 'data': u'order_update_good',}
	log.info('api_order_update_json end')
	return HttpResponse(json.dumps(tmp), content_type='application/json')
