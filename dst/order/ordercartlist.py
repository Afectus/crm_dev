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
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.base import TemplateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator

from django.urls import reverse

import datetime, time

from django.db.models import Sum, Count, Q, IntegerField
from django.db.models.functions import Cast

from django.views.decorators.csrf import csrf_exempt

import urllib
import re
import requests

from django.conf import settings

from django.utils.encoding import force_text


from node.models import *
from .models import *

from django.core.mail import send_mail


import logging
log = logging.getLogger(__name__)





#@method_decorator(permission_required('order.add_order'), name='dispatch')
class ordercartlist_edit(UpdateView):
	model = ordercartlist
	template_name = '_edit2.html'
	success_url = '/order/list'
	fields = ['price', 'col', ]
	
	def dispatch(self, request, *args, **kwargs):
		om=get_list_or_404(ordermanager, user=self.request.user)
		return super(ordercartlist_edit, self).dispatch(request, *args, **kwargs)

	# def get_object(self, queryset=None):
		# self.data=super(ordercartlist_edit, self).get_object()
		# return self.data

	def get_success_url(self):
		return reverse('order:detail', args=[self.get_object().order.id])

	def form_valid(self, form):
		#instance = form.save(commit=False)
		#instance.usertask = self.data
		#instance.user = self.request.user
		#instance.save()
		oe=orderevent.objects.create(user=self.request.user, order=self.get_object().order, event='other', comment='Редактирование позиции товара',)
		return super(ordercartlist_edit, self).form_valid(form)

		
		
		
		
class ordercartlist_add(CreateView):
	model = ordercartlist
	template_name = 'ordercartlist_add.html'
	success_url = '/'
	fields = ['goods', 'price', 'col', ]
	
	def dispatch(self, request, *args, **kwargs):
		om=get_list_or_404(ordermanager, user=self.request.user)
		self.o=get_object_or_404(order, status='wait', id=self.kwargs['pk'])
		return super(ordercartlist_add, self).dispatch(request, *args, **kwargs)

	def get_success_url(self):
		return reverse('order:detail', args=[self.o.id])
	
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
			form = super(ordercartlist_add, self).get_form(form_class)
			form.fields['goods'].required=True
			form.fields['goods'].widget=forms.TextInput()
			return form
		return form_class(**self.get_form_kwargs())
	
	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.order = self.o
		instance.save()
		# self.data=instance
		oe=orderevent.objects.create(user=self.request.user, order=instance.order, event='other', comment='Добавление позиции товара',)
		return super(ordercartlist_add, self).form_valid(form)		
		
		
		
		
#@method_decorator(permission_required('workflow.add_printtask'), name='dispatch')
class ordercartlist_del(DeleteView):
	model = ordercartlist
	template_name = '_confirm_delete.html'
	success_url = '/'

	def dispatch(self, request, *args, **kwargs):
		om=get_list_or_404(ordermanager, user=self.request.user)
		#self.o=get_object_or_404(order, status='wait', id=self.kwargs['pk'])
		return super(ordercartlist_del, self).dispatch(request, *args, **kwargs)
	
	#def get_object(self, queryset=None):
	#	return get_object_or_404(self.model, id=self.kwargs['pk'])
		
	def get_success_url(self):
		oe=orderevent.objects.create(user=self.request.user, order=self.get_object().order, event='other', comment='Удаление позиции товара',)
		return reverse('order:detail', args=[self.get_object().order.id])
		
	def get_context_data(self, **kwargs):
		context = super(ordercartlist_del, self).get_context_data(**kwargs)
		context['object'] = self.get_object().name
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = reverse('order:detail', args=[self.get_object().order.id])
		return context