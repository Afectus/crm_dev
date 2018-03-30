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
from worktask.models import *
from useridea.models import *

import logging
log = logging.getLogger(__name__)


class create_useridea(CreateView):
	model = useridea
	template_name = 'create_useridea.html'
	#form_class = Form_create_nickname
	success_url = '/useridea/list/?success=true'
	fields = ['name', 'message', ]
	
	def dispatch(self, request, *args, **kwargs):
		return super(create_useridea, self).dispatch(request, *args, **kwargs)
		
	def get_success_url(self):
		return '/useridea/detail/%s' % (self.data.id)
	
	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.user = self.request.user
		instance.save()
		self.data = instance
		return super(create_useridea, self).form_valid(form)
		
class create_fileidea(CreateView):
	model = fileidea
	template_name = 'create_fileidea.html'
	#form_class = Form_create_nickname
	success_url = '/useridea/list/?success=true'
	fields = ['name', 'type', 'sourcefile', 'pict', ]
	
	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(useridea, id=self.kwargs['pk'], user=self.request.user)
		return super(create_fileidea, self).dispatch(request, *args, **kwargs)
	
	def get_success_url(self):
		return '/useridea/detail/%s' % (self.data.id)
	
	def get_initial(self):
		return {'type':self.request.GET.get('type', 'file'),}
		
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
			form = super(create_fileidea, self).get_form(form_class)
			form.fields['type'].widget=forms.HiddenInput() #скрываем поле
			if 'type' in self.request.GET:
				if self.request.GET['type'] == 'file':
					form.fields['pict'].widget=forms.HiddenInput()
				else:
					form.fields['sourcefile'].widget=forms.HiddenInput()
				return form
		return form_class(**self.get_form_kwargs())	

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.useridea = self.data
		instance.save()
		return super(create_fileidea, self).form_valid(form)
	
	def get_context_data(self, *args, **kwargs):
		context_data = super(create_fileidea, self).get_context_data(*args, **kwargs)
		context_data.update({'object': self.data,})
		return context_data	
		
		
class remove_fileidea(DeleteView):
	model = fileidea
	template_name = '_confirm_delete.html'
	success_url = '/useridea/list/?success=true'
	
	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(self.model, id=self.kwargs['pk'], useridea__user=self.request.user)
		return super(remove_fileidea, self).dispatch(request, *args, **kwargs)
	
	def get_success_url(self):
		return '/useridea/detail/%s' % (self.data.useridea.id)
		
	def get_context_data(self, **kwargs):
		context = super(remove_fileidea, self).get_context_data(**kwargs)
		#context['object'] = mark_safe('<a href="%s">файл</a>' % self.data.sourcefile.url)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = '/useridea/detail/%s' % (self.data.useridea.id)
		return context
		
		

#@method_decorator(permission_required('useridea.add_useridea'), name='dispatch')	
class useridea_edit(UpdateView):
	model = useridea
	template_name = 'useridea_edit.html'
	success_url = '/useridea/list/'
	fields = [ 'name', 'message', ]
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_404(self.model, id=self.kwargs['pk'], user=request.user)
		return super(useridea_edit, self).dispatch(request, *args, **kwargs)

	def get_success_url(self):
		return '/useridea/detail/%s' % (self.get_object().id)		

		
		

@method_decorator(permission_required('useridea.add_useridea'), name='dispatch')
class useridea_list(ListView):
	template_name = 'useridea_list.html'
	model = useridea
	paginate_by = 20
	
	def dispatch(self, request, *args, **kwargs):
		return super(useridea_list, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(useridea_list, self).get_queryset()
		#self.data = data #for get_context_data
		#data = data.filter()
		return data
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(useridea_list, self).get_context_data(*args, **kwargs)
		#context_data.update({'a': 'a',})
		return context_data		
		
				
	
class useridea_detail(CreateView):
	model = commentidea
	template_name = 'useridea_detail.html'
	#form_class = Form_create_nickname
	success_url = '/useridea/list/?success=true'
	fields = ['message', 'pict', ]
	
	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(useridea, id=self.kwargs['pk'])
		return super(useridea_detail, self).dispatch(request, *args, **kwargs)


	def get_context_data(self, *args, **kwargs):
		context_data = super(useridea_detail, self).get_context_data(*args, **kwargs)
		context_data.update({'liked': likeidea.objects.filter(useridea__id=self.kwargs['pk'], user=self.request.user).exists(),})
		context_data.update({'object': self.data,})
		#
		context_data.update({'file': fileidea.objects.filter(useridea=self.data, type='file'),})
		context_data.update({'image': fileidea.objects.filter(useridea=self.data, type='image'),})
		return context_data		
	
	def get_success_url(self):
		return '/useridea/detail/%s' % (self.data.id)
	
	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.useridea = self.data
		instance.user = self.request.user
		instance.save()
		return super(useridea_detail, self).form_valid(form)
		
		
		
		
		
		
@csrf_exempt
def add_likeidea(request, pk, value):
	if request.method == 'POST' or request.method == 'GET':
		res={'res': 0, 'data': u'Ошибка',}
		try:
			t=useridea.objects.get(id=pk)
		except:
			pass
		else:
			lt=likeidea.objects.filter(useridea__id=pk, user=request.user)
			if lt.exists():
				res = {'res': 1, 'liked': 1,}
				return HttpResponseRedirect('/useridea/detail/%s' % t.pk)
			else:
				likeidea.objects.create(useridea=t, user=request.user, value=value).save()
				res = {'res': 1, 'liked': 0,}
				return HttpResponseRedirect('/useridea/detail/%s' % t.pk)
	return HttpResponse(json.dumps(res), content_type='application/json')
	


		