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
from django.http import HttpResponseForbidden

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.decorators.csrf import csrf_exempt

from django.utils.safestring import mark_safe

from django.core.exceptions import PermissionDenied

from django import forms
from django.core.exceptions import ValidationError
from django.contrib import auth
from django.contrib.auth.models import User, Group

from django.urls import reverse

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
from .models import *
from log.models import *

import logging
log = logging.getLogger(__name__)

		
class kassir_menu(TemplateView):
	template_name = "kassir_menu.html"

	
def validate_phone(value):
	p = re.compile('^9[0-9]{9}$')
	if not p.match(value):
		raise ValidationError(u'формат телефона должен быть например 9025112233. ')
	
	
class Form_filter_kassir_buyer(forms.Form):
	q = forms.CharField(label='Поиск', help_text='Введите слово для поиска', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'off'}), validators=[validate_phone], required=False)
	
	dcard = forms.CharField(label='Дисконтная карта', help_text='Дисконтная карта', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'off'}), min_length=6, max_length=100, required=False)

	
#@method_decorator(permission_required('node.add_buyer'), name='dispatch')
class kassir_buyer_list(ListView):
	template_name = 'kassir_buyer_list.html'
	model = buyer
	#paginate_by = 10
	
	def dispatch(self, request, *args, **kwargs):
		user = User.objects.get(username=request.user.username)
		grps = user.groups.filter(name='seniorkassir')
		if not grps:
			return HttpResponseRedirect("/?data=forbidden")
		return super(kassir_buyer_list, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(kassir_buyer_list, self).get_queryset()
		
		data=data.all() #выбираем основной запрос
		predata = data.none() 
		
		f=Form_filter_kassir_buyer(self.request.GET)
		
		
		req = ''
		
		if f.is_valid():
			fdata = f.cleaned_data
			#фильтрация
			if fdata['q']:
				req = '%s&q=%s' % (req, fdata['q'])
				predata=data.filter(phone__icontains=fdata['q'])[:10]
	
			if fdata['dcard']:
				req = '%s&dcard=%s' % (req, fdata['dcard'])
				predata=data.filter(discountcard__name__icontains=fdata['dcard'])[:10]

			
		self.req = req

		#paginator
		self.p = Paginator(predata, 20)
		page = self.kwargs['page']
		#print self.p.number()
		try:
			pdata = self.p.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			pdata = self.p.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			pdata = self.p.page(self.p.num_pages)
		
		return pdata
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(kassir_buyer_list, self).get_context_data(*args, **kwargs)
		
		#self.initial.update({'your_field': self.request.user})
		#if "fio" in self.request.GET:
		#	data=data.filter(i__contains=self.request.GET['fio'])
		context_data.update({'req': self.req,})
		context_data.update({'count': self.p.count,})
		context_data.update({'form': Form_filter_kassir_buyer(self.request.GET),})
		return context_data


		
#@method_decorator(permission_required('node.add_buyer'), name='dispatch')
class kassir_buyer_edit(UpdateView):
	model = buyer
	template_name = 'kassir_buyer_edit.html'
	success_url = '/kassir/buyer/list'
	fields = ['anketa', ]
	
	def dispatch(self, request, *args, **kwargs):
		user = User.objects.get(username=request.user.username)
		grps = user.groups.filter(name='seniorkassir')
		if not grps:
			return HttpResponseRedirect("/?data=forbidden")
		return super(kassir_buyer_edit, self).dispatch(request, *args, **kwargs)
	
	#def get_success_url(self):
	#	return '/kassir/buyer/edit/%s' % (self.get_object().id)
	
	def get_context_data(self, **kwargs):
		context = super(kassir_buyer_edit, self).get_context_data(**kwargs)
		context['object'] = self.get_object()
		return context
	
	# def get_initial(self):
		# return {'buyer':self.b, 'user': self.request.user}
	
	# def get_form(self, form_class):
		# form = super(kassir_buyer_edit, self).get_form(form_class)
		# form.fields['buyer'].widget.attrs['readonly'] = True
		# return form
		
		
	# def get_form(self, form_class=None):
		# if form_class is None:
			# form_class = self.get_form_class()
			# form = super(kassir_buyer_edit, self).get_form(form_class)
			# form.fields['buyer'].widget=forms.HiddenInput()
			# return form
		# return form_class(**self.get_form_kwargs())
	
	def form_valid(self, form):
		# self.object = form.save(commit=False)
		# self.object.user = self.request.user
		# self.object.save()
		kassirlog.objects.create(name='kassir update buyer anketa id=%s' % self.get_object().id, user=self.request.user, )
		return super(kassir_buyer_edit, self).form_valid(form)
		
	#def form_invalid(self, form):
		#print form.errors
	#	return super(kassir_buyer_edit, self).form_invalid(form)
		
		
		


#@method_decorator(permission_required('worktask.add_usertask'), name='dispatch')
class kassirvisitorlog_list(ListView):
	template_name = 'kassirvisitorlog_list.html'
	model = kassirvisitorlog
	paginate_by = 60
	
	def dispatch(self, request, *args, **kwargs):
		return super(kassirvisitorlog_list, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(kassirvisitorlog_list, self).get_queryset()
		data = data.filter(user=self.request.user)
		return data
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(kassirvisitorlog_list, self).get_context_data(*args, **kwargs)
		#список созданных мной задач
		#context_data.update({'task_create': self.data.filter(user=self.request.user, status='open'),})
		return context_data






		
	
	
#@method_decorator(permission_required('node.add_buyer'), name='dispatch')
class kassirvisitorlog_add(CreateView):
	model = kassirvisitorlog
	template_name = 'kassirvisitorlog_add.html'
	success_url = '/kassir/visitorlog/list'
	fields = ['shop', 'who', 'period', 'value',]
	
	def dispatch(self, request, *args, **kwargs):
		#user = User.objects.get(username=request.user.username)
		#grps = user.groups.filter(name='seniorkassir')
		#if not grps:
		#	return HttpResponseRedirect("/?data=forbidden")
		return super(kassirvisitorlog_add, self).dispatch(request, *args, **kwargs)
	
	#def get_success_url(self):
	#	return '/kassir/buyer/edit/%s' % (self.get_object().id)
	
	def get_context_data(self, **kwargs):
		context = super(kassirvisitorlog_add, self).get_context_data(**kwargs)
		#context['object'] = self.get_object()
		return context
	
	# def get_initial(self):
		# return {'buyer':self.b, 'user': self.request.user}
		
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
			form = super(kassirvisitorlog_add, self).get_form(form_class)
			form.fields['shop'].queryset = shop.objects.filter(profileuser__user=self.request.user)
			return form
		return form_class(**self.get_form_kwargs())
		
		
	# def get_form(self, form_class=None):
		# if form_class is None:
			# form_class = self.get_form_class()
			# form = super(kassirvisitorlog_add, self).get_form(form_class)
			# form.fields['buyer'].widget=forms.HiddenInput()
			# return form
		# return form_class(**self.get_form_kwargs())
	
	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.save()
		return super(kassirvisitorlog_add, self).form_valid(form)
		
	#def form_invalid(self, form):
		#print form.errors
	#	return super(kassirvisitorlog_add, self).form_invalid(form)