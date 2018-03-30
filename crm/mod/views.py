# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render_to_response
from django.shortcuts import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponsePermanentRedirect

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.decorators.csrf import csrf_exempt

from django.utils.safestring import mark_safe

from django.core.exceptions import PermissionDenied

from django import forms
from django.core.exceptions import ValidationError
from django.contrib import auth
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


from django.db.models import Max, Sum, Count
from django.db.models import Q, F

from ckeditor.widgets import CKEditorWidget

from dj.views import *


from django.core.mail import send_mail


from node.templatetags.nodetag import *

from node.models import *
from order.models import *
from panel.form import *
from panel.models import *
from panel.form import *
from sms.views import *
from sms.models import *
from bitrix.models import *
from mod.models import *

import logging
log = logging.getLogger(__name__)


class ballgen(TemplateView):
	template_name = 'ballgen.html'
	
	def get_context_data(self, *args, **kwargs):
		context_data = super(ballgen, self).get_context_data(*args, **kwargs)
		context_data.update({'ballconf': ballconfitem.objects.values('name').annotate(Count('name')).order_by('name'),})
		return context_data
	
	
	
@csrf_exempt
def ballgenconf(request):
	if request.method == 'POST':
		b=ballconfitem.objects.create(name=request.POST['name'], bid=request.POST['bid'], x=request.POST['x'], y=request.POST['y'], radius=request.POST['radius'], color=request.POST['color'], colortext=request.POST['colortext'], background=request.POST['background'])
		res={'res': 1, 'data': b.id}
		return HttpResponse(json.dumps(res), content_type='application/json')
				
	res={'res': 0, 'data': u'Ошибка',}
	return HttpResponse(json.dumps(res), content_type='application/json')
	
	
@csrf_exempt
def ballgetconf(request, name):
	if request.method == 'GET':
		colortext = ''
		background = ''
		try:
			b = ballconfitem.objects.filter(name=name)
		except Exception as e:
			pass
			#print e
		else:
			item = []
			for i in b:
				item.append({'name': i.name, 'id': int(i.bid), 'x': float(i.x), 'y': float(i.y), 'radius': int(i.radius), 'color': i.color, 'colortext': i.colortext,})
				colortext = i.colortext
				background = i.background

			res={'res': 1, 'item': item, 'color': json.loads(colortext), 'background': background, }
			return HttpResponse(json.dumps(res), content_type='application/json')
	res={'res': 0, 'data': u'Ошибка',}
	return HttpResponse(json.dumps(res), content_type='application/json')
	
	
	
	
	
@csrf_exempt
def go(request):
	if request.method == 'GET':
		data = goreport.objects.create(ua=request.META['HTTP_USER_AGENT'], ip=request.META['REMOTE_ADDR'])
		data.save()
		return HttpResponseRedirect('http://babah24.ru')
	res={'res': 0, 'data': u'bad',}
	return HttpResponse(json.dumps(res), content_type='application/json')
	

@csrf_exempt
def qr(request, id):
	if request.method == 'GET':
		url = 'http://babah24.ru/katalog/detail.php?ELEMENT_ID=%s' % (id)
		data = qrcodereport.objects.create(ua=request.META['HTTP_USER_AGENT'], ip=request.META['REMOTE_ADDR'], comment=url)
		data.save()
		return HttpResponseRedirect(url)
	res={'res': 0, 'data': u'bad',}
	return HttpResponse(json.dumps(res), content_type='application/json')
	
	
class templatemail(TemplateView):
	template_name = 'templatemail.html'

