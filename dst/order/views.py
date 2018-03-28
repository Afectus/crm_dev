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


def validate_phone(value):
	p = re.compile('^9[0-9]{9}$')
	if not p.match(value):
		raise ValidationError(u'формат телефона должен быть например 9XXXXXXXXX. ')

#добавление ордера вручную
#@method_decorator(permission_required('order.add_order'), name='dispatch')
class order_add(CreateView):
	model = order
	template_name = '_edit2.html'
	success_url = '/order/list'
	fields = ['status', 'uname', 'phone', 'city', 'area', 'addr', 'discont', 'comment', 'terminal', 'cart',]
	
	def dispatch(self, request, *args, **kwargs):
		om=get_list_or_404(ordermanager, user=self.request.user)
		return super(order_add, self).dispatch(request, *args, **kwargs)

	def get_success_url(self):
		return '/order/detail/%s' % (self.data.id)
	
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
			form = super(order_add, self).get_form(form_class)
			form.fields['phone'].validators=[validate_phone]
			form.fields['status'].initial='accept'
			return form
		return form_class(**self.get_form_kwargs())
	
	def form_valid(self, form):
		instance = form.save(commit=False)
		#instance.user = self.request.user
		instance.save()
		self.data=instance
		oe=orderevent.objects.create(user=self.request.user, order=instance, event='add', comment='manual add oroder on manager',)
		return super(order_add, self).form_valid(form)



		
		
class Form_filter_order(forms.Form):
	sortchoice=(
		('-id', '-id'),
		('id', 'id'),
		('ctime', 'Время (старые)'),
		('-ctime', 'Время (новые)'),
		('-area', 'Район'),
		('-status', 'Статус'),
		)
	
	sort = forms.ChoiceField(label='Сортировка', help_text='Сортировать по полю', widget=forms.Select(attrs={'class': 'form-control'}), choices=sortchoice, required=False)

#@method_decorator(permission_required('order.add_order'), name='dispatch')
class order_list(ListView):
	template_name = 'order_list.html'
	model = order
	#paginate_by = 20
	
	def dispatch(self, request, *args, **kwargs):
		#проверяем права менеджеров интернет магазина
		om=get_list_or_404(ordermanager, user=self.request.user)
		return super(order_list, self).dispatch(request, *args, **kwargs)
	
	def get_queryset(self):
		data=super(order_list, self).get_queryset()
		data=data.exclude(Q(status='success') | Q(status='zabrali') | Q(status='cancel') | Q(status='kupilsam'))
		
		f=Form_filter_order(self.request.GET)
		req = ''
		
		if f.is_valid():
			fdata = f.cleaned_data
			if fdata['sort']:
				#req = '%s&sort=%s' % (req, self.request.GET['sort'])
				data=data.order_by(fdata['sort'])
		
		return data
	
	def get_context_data(self, *args, **kwargs):
		context_data = super(order_list, self).get_context_data(*args, **kwargs)
		context_data.update({'form': Form_filter_order(self.request.GET),})
		#context_data.update({'projects': projects.objects.filter(status=True)})
		return context_data
		
		
#@method_decorator(permission_required('order.add_order'), name='dispatch')
class order_arch_list(ListView):
	template_name = 'order_list.html'
	model = order
	paginate_by = 60
	
	def dispatch(self, request, *args, **kwargs):
		#проверяем права менеджеров интернет магазина
		om=get_list_or_404(ordermanager, user=self.request.user)
		return super(order_arch_list, self).dispatch(request, *args, **kwargs)
	
	def get_queryset(self):
		data=super(order_arch_list, self).get_queryset()
		data=data.filter(Q(status='success') | Q(status='zabrali') | Q(status='cancel') | Q(status='kupilsam'))
		return data
	
	def get_context_data(self, *args, **kwargs):
		context_data = super(order_arch_list, self).get_context_data(*args, **kwargs)
		#context_data.update({'projects': projects.objects.filter(status=True)})
		return context_data
	
	
#@method_decorator(permission_required('order.add_order'), name='dispatch')
class order_edit(UpdateView):
	model = order
	template_name = '_edit2.html'
	success_url = '/order/list'
	fields = ['uname', 'phone', 'city', 'area', 'addr', 'discont', 'comment', 'terminal', 'cart', 'timecomment', 'sum', 'sumreturn', 'total', ]
	
	def dispatch(self, request, *args, **kwargs):
		om=get_list_or_404(ordermanager, user=self.request.user)
		return super(order_edit, self).dispatch(request, *args, **kwargs)

	# def get_object(self, queryset=None):
		# self.data=super(order_edit, self).get_object()
		# return self.data

	def get_success_url(self):
		return '/order/detail/%s' % (self.get_object().id)
		
	def form_valid(self, form):
		#instance = form.save(commit=False)
		#instance.usertask = self.data
		#instance.user = self.request.user
		#instance.save()
		oe=orderevent.objects.create(user=self.request.user, order=self.get_object(), event='edit', comment='edit order on manager',)
		return super(order_edit, self).form_valid(form)
		
		
		
#@method_decorator(permission_required('order.add_order'), name='dispatch')
class order_status_edit(UpdateView):
	model = order
	template_name = '_edit2.html'
	success_url = '/order/list'
	fields = ['status',]
	
	def dispatch(self, request, *args, **kwargs):
		om=get_list_or_404(ordermanager, user=self.request.user)
		return super(order_status_edit, self).dispatch(request, *args, **kwargs)

	# def get_object(self, queryset=None):
		# self.data=super(order_status_edit, self).get_object()
		# return self.data

	def get_success_url(self):
		if 'next' in self.request.GET:
			return self.request.GET['next']
		return '/order/detail/%s' % (self.get_object().id)
		
	def form_valid(self, form):
		#instance = form.save(commit=False)
		#instance.usertask = self.data
		#instance.user = self.request.user
		#instance.save()
		#fdata = form.cleaned_data
		instance = form.save()
		oe=orderevent.objects.create(user=self.request.user, order=self.get_object(), event='statusedit', comment='Изменение статуса заказа на "%s"' % (instance.get_status_display()),)
		return super(order_status_edit, self).form_valid(form)


class order_event_detail(DetailView):
	model = orderevent
	template_name = 'order_event_detail.html'

	def dispatch(self, request, *args, **kwargs):
		om=get_list_or_404(ordermanager, user=self.request.user)
		return super(order_event_detail, self).dispatch(request, *args, **kwargs)
		
		
def order_accept(request, pk):
	om=get_list_or_404(ordermanager, user=request.user)
	data = get_object_or_404(order, id=pk, status='wait')
	data.status='accept'
	data.save()
	oe=orderevent.objects.create(user=request.user, order=data, event='accept', comment='manager accept order',)
	return HttpResponseRedirect(reverse('order:detail', args=[data.id]))

def order_success(request, pk):
	om=get_list_or_404(ordermanager, user=request.user)
	data = get_object_or_404(order, id=pk, status='accept')
	data.status='success'
	data.save()
	oe=orderevent.objects.create(user=request.user, order=data, event='success', comment='manager success order',)
	return HttpResponseRedirect(reverse('order:detail', args=[data.id]))	

#@method_decorator(permission_required('order.add_order'), name='dispatch')
class order_detail(DetailView):
	model = order
	template_name = 'order_detail.html'
	
	def dispatch(self, request, *args, **kwargs):
		om=get_list_or_404(ordermanager, user=self.request.user)
		return super(order_detail, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context_data = super(order_detail, self).get_context_data(*args, **kwargs)
		self.data=super(order_detail, self).get_object()
		log.debug(self.data.phone)
		context_data.update({'buyer': buyer.objects.filter(phone=self.data.phone)})
		context_data.update({'check': check.objects.filter(buyer__phone=self.data.phone).order_by('-time')[:10]})
		context_data.update({'cartsum': ordercartlist.objects.filter(order=self.data).aggregate(s=Sum(F('col')*F('price')))['s']})
		return context_data


#@method_decorator(permission_required('order.add_order'), name='dispatch')
class order_detail_print(DetailView):
	model = order
	template_name = 'order_detail_print.html'
	
	def dispatch(self, request, *args, **kwargs):
		om=get_list_or_404(ordermanager, user=self.request.user)
		return super(order_detail_print, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context_data = super(order_detail_print, self).get_context_data(*args, **kwargs)
		self.data=super(order_detail_print, self).get_object()
		log.debug(self.data.phone)
		context_data.update({'buyer': buyer.objects.filter(phone=self.data.phone)})
		context_data.update({'check': check.objects.filter(buyer__phone=self.data.phone).order_by('-time')[:10]})
		return context_data
		



#@method_decorator(permission_required('order.add_order'), name='dispatch')
class order_inway_xls(ListView):
	model = order
	template_name = 'order_inway_xls.html'
	
	def dispatch(self, request, *args, **kwargs):
		om=get_list_or_404(ordermanager, user=self.request.user)
		return super(order_inway_xls, self).dispatch(request, *args, **kwargs)

	def get_queryset(self):
		data=super(order_inway_xls, self).get_queryset()
		data=data.filter(Q(status='inway'))
		data=data.order_by('-area')
		return data

	def get_context_data(self, *args, **kwargs):
		context_data = super(order_inway_xls, self).get_context_data(*args, **kwargs)
		#self.data=super(order_inway_xls, self).get_object()
		#print self.data
		#log.debug(self.data.phone)
		#context_data.update({'buyer': buyer.objects.filter(phone=self.data.phone)})
		#context_data.update({'check': check.objects.filter(buyer__phone=self.data.phone).order_by('-time')[:10]})
		return context_data

		
		
'''
@csrf_exempt
def order_inway_xls(request):
	#log.info('start=api1c_getcert')
	#log.info('url=%s' % request.get_full_path())
	#log.info('request.body=%s' % request.body)
	#if request.method == 'GET' and 'crc' in request.GET:
	if request.method == 'POST' or request.method == 'GET':
		om=get_list_or_404(ordermanager, user=request.user)
		#data = request.body
		#print data
		#data = data.split(';')
		#data = json.loads(data)
		#g=goods.objects.filter(id1c__in=data['id'], base__id=int(data['base']))
		# if g.exists():
			# log.info('res=%s' % 'exists')
			
			
			# ###mod g text cert
			# for i in g:
				# if i.goodscert:
					# pass
				# else: #если нет сертификата, то прописываем от второго товара
					# try:
						# r=relgoods.objects.get(b=i)
					# except:
						# pass
					# else:
						# #log.info('makecertpdf=%s' % r.a)
						# #log.info('makecertpdf=%s' % r.a.goodscert)
						# if r.a.goodscert:
							# #merger.append(r.a.goodscert.pdf.path)
							# i.goodscert=r.a.goodscert
						# else:
							# pass
			
			# ###
			# xlsurl, xlspath, pdfpath = makecertexcel(data['head'], g)

			# print xlsurl
			# print xlspath
			# print pdfpath
			
			# pdfurl = makecertpdf(g, pdfpath)
			# print pdfurl
		pdfurl = 'pdfurl'
		return HttpResponse('%s' % (pdfurl))
	return HttpResponse('fail')
'''
