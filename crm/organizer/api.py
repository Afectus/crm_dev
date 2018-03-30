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

from .models import *

import logging
log = logging.getLogger(__name__)

@csrf_exempt
def organizer_api_drop(request):
	log.info('organizer_api_drop')
	#log.info('request.body=%s' % request.body)
	tmp={'res': 0, 'data': 'fail',}
	if request.method == 'POST' or request.method == 'GET':
		try:
			data=json.loads(request.body.decode("utf-8"))
		except:
			log.info('json invalid')
			pass
		else:
			log.info('request.body=%s' % request.body)
			try:
				start = datetime.datetime.strptime(data['start'], "%Y-%m-%dT%H:%M:%S")
			except:
				start = datetime.datetime.strptime(data['start'], "%Y-%m-%d")
			#end = datetime.datetime.strptime(data['end'], "%Y-%m-%dT%H:%M:%S")
			log.info(start)
			
			try:
				o=organizer.objects.create(user=request.user, name=data['title'], stime=start, desc=data['desc'], icon=data['icon'], classname=data['classname'])
			except Exception as e:
				tmp={'res': 0, 'data': 'organizer.objects.create fail %s' % (e),}
			else:
				tmp={'res': 1, 'data': 'organizer.objects.create success', 'id': o.id,}
	return HttpResponse(json.dumps(tmp), content_type='application/json')	
	
@csrf_exempt
def organizer_api_eventdrop(request):
	log.info('organizer_api_drop')
	#log.info('request.body=%s' % request.body)
	tmp={'res': 0, 'data': 'fail',}
	if request.method == 'POST' or request.method == 'GET':
		try:
			data=json.loads(request.body.decode("utf-8"))
		except:
			log.info('json invalid')
			pass
		else:
			log.info('request.body=%s' % request.body)
			try:
				start = datetime.datetime.strptime(data['start'], "%Y-%m-%dT%H:%M:%S")
			except:
				start = datetime.datetime.strptime(data['start'], "%Y-%m-%d")
			log.info(start)
			end = None
			if data['end']:
				try:
					end = datetime.datetime.strptime(data['end'], "%Y-%m-%dT%H:%M:%S")
				except:
					end = datetime.datetime.strptime(data['end'], "%Y-%m-%d")
			log.info(start, end)
			
			try:
				o=organizer.objects.get(user=request.user, id=data['id'])
			except Exception as e:
				tmp={'res': 0, 'data': 'organizer.objects.get fail %s' % (e),}
			else:
				o.stime = data['start']
				o.etime = data['end']
				o.save()
				tmp={'res': 1, 'data': 'organizer.objects.get success', 'id': o.id,}

	return HttpResponse(json.dumps(tmp), content_type='application/json')	


	
	
@csrf_exempt
def organizer_api_eventresize(request):
	log.info('organizer_api_eventresize')
	#log.info('request.body=%s' % request.body)
	tmp={'res': 0, 'data': 'fail',}
	if request.method == 'POST' or request.method == 'GET':
		try:
			data=json.loads(request.body.decode("utf-8"))
		except:
			log.info('json invalid')
			pass
		else:
			log.info('request.body=%s' % request.body)
			try:
				start = datetime.datetime.strptime(data['start'], "%Y-%m-%dT%H:%M:%S")
			except:
				start = datetime.datetime.strptime(data['start'], "%Y-%m-%d")
			log.info(start)
			end = None
			if data['end']:
				try:
					end = datetime.datetime.strptime(data['end'], "%Y-%m-%dT%H:%M:%S")
				except:
					end = datetime.datetime.strptime(data['end'], "%Y-%m-%d")
			log.info(start, end)
			
			try:
				o=organizer.objects.get(user=request.user, id=data['id'])
			except Exception as e:
				tmp={'res': 0, 'data': 'organizer.objects.get fail %s' % (e),}
			else:
				o.stime = data['start']
				o.etime = data['end']
				o.save()
				tmp={'res': 1, 'data': 'organizer.objects.get success', 'id': o.id,}

	return HttpResponse(json.dumps(tmp), content_type='application/json')	
	
	
@csrf_exempt
def organizer_api_eventdel(request):
	log.info('organizer_api_eventdel')
	#log.info('request.body=%s' % request.body)
	tmp={'res': 0, 'data': 'fail',}
	if request.method == 'POST' or request.method == 'GET':
		try:
			data=json.loads(request.body.decode("utf-8"))
		except:
			log.info('json invalid')
			pass
		else:
			log.info('request.body=%s' % request.body)
			try:
				o=organizer.objects.get(user=request.user, id=data['id'])
			except Exception as e:
				tmp={'res': 0, 'data': 'organizer.objects.get fail %s' % (e),}
			else:
				o.delete()
				tmp={'res': 1, 'data': 'organizer.objects.get(id=).delete() success', 'id': o.id,}

	return HttpResponse(json.dumps(tmp), content_type='application/json')	