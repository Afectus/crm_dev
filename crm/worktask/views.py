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
from acl.views import *

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

import logging
log = logging.getLogger(__name__)


class create_freetask(CreateView):
	model = usertask
	template_name = 'create_freetask.html'
	#form_class = Form_create_nickname
	success_url = '/worktask/list/?success=true'
	fields = ['name', 'message', ]
	
	def dispatch(self, request, *args, **kwargs):
		return super(create_freetask, self).dispatch(request, *args, **kwargs)
		
	def get_success_url(self):
		return '/worktask/detail/%s' % (self.data.id)
	
	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.user = self.request.user
		instance.save()
		self.data = instance
		return super(create_freetask, self).form_valid(form)
	
@method_decorator(permission_required('worktask.add_usertask'), name='dispatch')
class create_usertask(CreateView):
	model = usertask
	template_name = 'create_usertask.html'
	#form_class = Form_create_nickname
	success_url = '/worktask/list/?success=true'
	fields = ['name', 'message', 'priority', 'etime', 'executor', ]
	
	def dispatch(self, request, *args, **kwargs):
		return super(create_usertask, self).dispatch(request, *args, **kwargs)
	
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
			form = super(create_usertask, self).get_form(form_class)
			form.fields['etime'].widget=forms.TextInput(attrs={'class':'mydatepicker1'})
			form.fields['etime'].input_formats=['%d-%m-%y', '%d-%m-%Y',]
			form.fields['etime'].help_text=('формат %d-%m-%Y')
			return form
		return form_class(**self.get_form_kwargs())
	
	def get_success_url(self):
		return '/worktask/detail/%s' % (self.data.id)
	
	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.user = self.request.user
		instance.type = 'user'
		instance.save()
		self.data = instance
		return super(create_usertask, self).form_valid(form)	

		
class create_filetask(CreateView):
	model = filetask
	template_name = 'create_filetask.html'
	#form_class = Form_create_nickname
	success_url = '/worktask/list/?success=true'
	fields = ['name', 'type', 'sourcefile', 'pict', ]
	
	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(usertask, id=self.kwargs['pk'], user=self.request.user)
		return super(create_filetask, self).dispatch(request, *args, **kwargs)
	
	def get_success_url(self):
		return '/worktask/detail/%s' % (self.data.id)
	
	def get_initial(self):
		return {'type':self.request.GET.get('type', 'file'),}
		
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
			form = super(create_filetask, self).get_form(form_class)
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
		instance.usertask = self.data
		instance.save()
		return super(create_filetask, self).form_valid(form)
	
	def get_context_data(self, *args, **kwargs):
		context_data = super(create_filetask, self).get_context_data(*args, **kwargs)
		context_data.update({'object': self.data,})
		return context_data	
		
		
class remove_filetask(DeleteView):
	model = filetask
	template_name = '_confirm_delete.html'
	success_url = '/worktask/list/?success=true'
	
	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(self.model, id=self.kwargs['pk'], usertask__status='open', usertask__user=self.request.user)
		return super(remove_filetask, self).dispatch(request, *args, **kwargs)
	
	def get_success_url(self):
		return '/worktask/detail/%s' % (self.data.usertask.id)
		
	def get_context_data(self, **kwargs):
		context = super(remove_filetask, self).get_context_data(**kwargs)
		#context['object'] = mark_safe('<a href="%s">файл</a>' % self.data.sourcefile.url)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = '/worktask/detail/%s' % (self.data.usertask.id)
		return context
		
		

#@method_decorator(permission_required('worktask.add_usertask'), name='dispatch')	
class task_edit(UpdateView):
	model = usertask
	template_name = 'task_edit.html'
	success_url = '/worktask/list/'
	fields = [ 'name', 'message', ]
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_404(self.model, status='open', id=self.kwargs['pk'], user=request.user)
		return super(task_edit, self).dispatch(request, *args, **kwargs)

	def get_success_url(self):
		return '/worktask/detail/%s' % (self.get_object().id)		

		
		

#@method_decorator(permission_required('worktask.add_usertask'), name='dispatch')
class task_list(ListView):
	template_name = 'task_list.html'
	model = usertask
	paginate_by = 60
	
	def dispatch(self, request, *args, **kwargs):
		return super(task_list, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(task_list, self).get_queryset()
		self.data = data #for get_context_data
		data = data.filter(Q(user=self.request.user, status='close') | Q(type='free', status='close') | Q(executor__user=self.request.user, status='close')).distinct()
		return data
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(task_list, self).get_context_data(*args, **kwargs)
		#список созданных мной задач
		context_data.update({'task_create': self.data.filter(user=self.request.user, status='open'),})
		#мои регламентные задачи + свободные в которых я участвую
		context_data.update({'task_reglamentfree': self.data.filter(executor__user=self.request.user, status='open'),})
		#свободные задачи в которых я не учавствую
		context_data.update({'task_free': self.data.filter(type='free', status='open').exclude(executor__user=self.request.user),})
		#закрытие задачи (мои+свободные+регламентные)
		#context_data.update({'task_close': self.data.filter(type='free', status='close'),})
		return context_data
		
				

#@method_decorator(permission_required('worktask.add_usertask'), name='dispatch')	
class admin_task_edit(UpdateView):
	model = usertask
	template_name = 'admin_task_edit.html'
	success_url = '/worktask/list/'
	fields = ['status', 'name', 'message', 'priority', 'etime', 'executor', 'rating', ]
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'worktask', 'R')
		get_object_or_404(self.model, id=self.kwargs['pk'])
		return super(admin_task_edit, self).dispatch(request, *args, **kwargs)

	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
			form = super(admin_task_edit, self).get_form(form_class)
			form.fields['etime'].widget=forms.TextInput(attrs={'class':'mydatepicker1'})
			form.fields['etime'].input_formats=['%d-%m-%y', '%d-%m-%Y',]
			return form
		return form_class(**self.get_form_kwargs())
		
		
	def get_success_url(self):
		return '/worktask/admin/edit/%s' % (self.get_object().id)
		
		
		
class task_detail(CreateView):
	model = commenttask
	template_name = 'task_detail.html'
	#form_class = Form_create_nickname
	success_url = '/worktask/list/?success=true'
	fields = ['message', 'pict', ]
	
	def dispatch(self, request, *args, **kwargs):
		#проверяем прочитано задание или нет
		try:
			t = usertask.objects.get(id=self.kwargs['pk'], executor__user=request.user, status='open')
		except:
			pass
		else:
			testread=notificationtask.objects.filter(usertask__id=self.kwargs['pk'], usertask__executor__user=request.user, user=request.user)
			if not testread.exists(): #если не прочитано редиректим на прочитано
				return HttpResponseRedirect('/worktask/read/task/%s/' % self.kwargs['pk'])
		###
		res = False
		try:
			self.data = usertask.objects.get(id=self.kwargs['pk'], type='free')
		except:
			pass
		else:
			res = True
		try:
			self.data = usertask.objects.get(id=self.kwargs['pk'], type='user', executor__user=self.request.user)
		except:
			pass
		else:
			res = True
		try:
			self.data = usertask.objects.get(id=self.kwargs['pk'], user=self.request.user)
		except:
			pass
		else:
			res = True
		if res == False:
			raise Http404
		return super(task_detail, self).dispatch(request, *args, **kwargs)


	def get_context_data(self, *args, **kwargs):
		context_data = super(task_detail, self).get_context_data(*args, **kwargs)
		context_data.update({'liked': liketask.objects.filter(usertask__id=self.kwargs['pk'], user=self.request.user).exists(),})
		context_data.update({'object': self.data,})
		context_data.update({'taken': self.data.executor.filter(user=self.request.user).exists(),})
		#
		context_data.update({'file': filetask.objects.filter(usertask=self.data, type='file'),})
		context_data.update({'image': filetask.objects.filter(usertask=self.data, type='image'),})
		return context_data		
	
	def get_success_url(self):
		return '/worktask/detail/%s' % (self.data.id)
	
	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.usertask = self.data
		instance.user = self.request.user
		instance.save()
		return super(task_detail, self).form_valid(form)
		
		
		
		
		
		
@csrf_exempt
def add_liketask(request, pk, value):
	if request.method == 'POST' or request.method == 'GET':
		res={'res': 0, 'data': u'Ошибка',}
		try:
			t=usertask.objects.get(status='open', id=pk)
		except:
			pass
		else:
			lt=liketask.objects.filter(usertask__status='open', usertask__id=pk, user=request.user)
			if lt.exists():
				res = {'res': 1, 'liked': 1,}
				return HttpResponseRedirect('/worktask/detail/%s' % t.pk)
			else:
				liketask.objects.create(usertask=t, user=request.user, value=value).save()
				res = {'res': 1, 'liked': 0,}
				return HttpResponseRedirect('/worktask/detail/%s' % t.pk)
	return HttpResponse(json.dumps(res), content_type='application/json')
	
	
	
@csrf_exempt
def take_task(request, pk):
	if request.method == 'POST' or request.method == 'GET':
		try: #проверяем существует ли задание
			t=usertask.objects.get(status='open', id=pk)
		except:
			pass
		else:
			if t.type == 'free':
				e=t.executor.filter(user=request.user)
				if not e.exists():
					p=profileuser.objects.get(user=request.user)
					t.executor.add(p)
	return HttpResponseRedirect('/worktask/detail/%s' % t.pk)


@csrf_exempt
def read_task(request, pk):
	if request.method == 'POST' or request.method == 'GET':
		try: #проверяем существует ли задание
			t=usertask.objects.get(status='open', id=pk)
		except:
			pass
		else: #задание прочитано
			notificationtask.objects.create(usertask=t, user=request.user)
	return HttpResponseRedirect('/worktask/detail/%s' % t.pk)	
	
	