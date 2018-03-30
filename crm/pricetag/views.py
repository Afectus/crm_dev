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
from django.urls import reverse

from django.db.models import Max, Sum, Count
from django.db.models import Q, F

from ckeditor.widgets import CKEditorWidget

from dj.views import *


from django.core.mail import send_mail


from node.templatetags.nodetag import *

from node.models import *
from panel.form import *
from panel.models import *
from panel.form import *
from .models import *
from acl.views import get_object_or_denied

import logging
log = logging.getLogger(__name__)



class Form_filter_pricequeue_print_list(forms.Form):
	user = forms.ModelMultipleChoiceField(label='Пользователи', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), queryset=profileuser.objects.filter(status='on'), required=False)
	
	#time
	timestart = forms.DateField(label="Время от", help_text='Время от', input_formats=['%d-%m-%y', '%d/%m/%y', '%d.%m.%y', '%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y',], required=False, widget=forms.TextInput(attrs={'class':'form-control datepicker',  'data-dateformat': "dd-mm-yy"}), initial=datetime.date.today())

	timeend = forms.DateField(label="Время до", help_text='Время до', input_formats=['%d-%m-%y', '%d/%m/%y', '%d.%m.%y', '%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y',], required=False, widget=forms.TextInput(attrs={'class':'form-control datepicker',  'data-dateformat': "dd-mm-yy"}))
	#

class pricequeue_print_list(ListView):
	template_name = 'pricequeue_print_list.html'
	model = pricequeue
	#paginate_by = 40
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'pricequeue', 'L') #проверяем права
		return super(pricequeue_print_list, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		self.data=super(pricequeue_print_list, self).get_queryset()
		self.data=self.data.filter(status=True) #выбираем основной запрос
		
		f=Form_filter_pricequeue_print_list(self.request.GET)
		
		
		req = ''
		
		if f.is_valid():
			fdata = f.cleaned_data
			#фильтрация
			if fdata['user']:
				req = '%s&user=%s' % (req, self.request.GET['user'])
				self.data=self.data.filter(user__in=fdata['user'].values_list('user__id')) 
				
			if fdata['timestart']:
				req = '%s&timestart=%s' % (req, self.request.GET['timestart'])
				self.data=self.data.filter(ctime__gt=fdata['timestart'])
			if fdata['timeend']:
				req = '%s&timeend=%s' % (req, self.request.GET['timeend']) 
				self.data=self.data.filter(ctime__lt=fdata['timeend'])
		
		self.req = req
		
		return self.data
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(pricequeue_print_list, self).get_context_data(*args, **kwargs)
		context_data.update({'req': self.req,})
		context_data.update({'form': Form_filter_pricequeue_print_list(self.request.GET)})
		# context_data.update({'itembarcode': printtask.objects.filter(user=self.request.user, barcode__isnull=False).exclude(barcode__exact=''),})
		# context_data.update({'itemprice': printtask.objects.filter(user=self.request.user, imageprice__isnull=False).exclude(imageprice__exact=''),})
		# context_data.update({'stock': stock.objects.filter(status=True),})
		# #sum
		# sum=self.data.aggregate(s=Sum('copies'))
		# context_data.update({'sum': sum['s'],})
		return context_data

			
class pricequeue_print_edit(UpdateView):
	model = pricequeue
	template_name = '_edit2.html'
	success_url = '/'
	fields = ['status', 'copies', 'barcode', ]
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'pricequeue', 'L') #проверяем права
		data = get_object_or_404(self.model, id=self.kwargs['pk'])
		return super(pricequeue_print_edit, self).dispatch(request, *args, **kwargs)	
		
	def get_success_url(self):
		return reverse('pricetag:pricequeue_print_list')	

#@method_decorator(permission_required('workflow.add_printtask'), name='dispatch')
class pricequeue_print_del(DeleteView):
	model = pricequeue
	template_name = '_confirm_delete.html'
	success_url = '/'

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'pricequeue', 'L') #проверяем права
		return super(pricequeue_print_del, self).dispatch(request, *args, **kwargs)
	
	#def get_object(self, queryset=None):
	#	return get_object_or_404(self.model, id=self.kwargs['pk'])
		
	#Django DeleteView without confirmation template
	def get(self, request, *args, **kwargs):
		return self.post(request, *args, **kwargs)
		
	def get_success_url(self):
		return reverse('pricetag:pricequeue_print_list')
		
	def get_context_data(self, **kwargs):
		context = super(pricequeue_print_del, self).get_context_data(**kwargs)
		context['object'] = self.data.id
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = reverse('pricetag:pricequeue_print_list')
		return context


#@method_decorator(permission_required('pricetag.add_pricequeue'), name='dispatch')
class pricequeue_list(ListView):
	template_name = 'pricequeue_list.html'
	model = pricequeue
	#paginate_by = 40
	
	def dispatch(self, request, *args, **kwargs):
		#get_object_or_denied(self.request.user, 'pricequeue', 'L') #проверяем права
		return super(pricequeue_list, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		self.data=super(pricequeue_list, self).get_queryset()
		self.data=self.data.filter(user=self.request.user, status=True) #выбираем основной запрос
		return self.data
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(pricequeue_list, self).get_context_data(*args, **kwargs)
		# context_data.update({'itembarcode': printtask.objects.filter(user=self.request.user, barcode__isnull=False).exclude(barcode__exact=''),})
		# context_data.update({'itemprice': printtask.objects.filter(user=self.request.user, imageprice__isnull=False).exclude(imageprice__exact=''),})
		# context_data.update({'stock': stock.objects.filter(status=True),})
		# #sum
		# sum=self.data.aggregate(s=Sum('copies'))
		# context_data.update({'sum': sum['s'],})
		return context_data
		
	
#@method_decorator(permission_required('workflow.add_printtask'), name='dispatch')
class pricequeue_del(DeleteView):
	model = pricequeue
	template_name = '_confirm_delete.html'
	success_url = '/'

	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(self.model, user=self.request.user, status=True, id=self.kwargs['pk'])
		return super(pricequeue_del, self).dispatch(request, *args, **kwargs)
	
	#def get_object(self, queryset=None):
	#	return get_object_or_404(self.model, id=self.kwargs['pk'])
		
	#Django DeleteView without confirmation template
	def get(self, request, *args, **kwargs):
		return self.post(request, *args, **kwargs)
		
	def get_success_url(self):
		return reverse('pricetag:pricequeue_list')
		
	def get_context_data(self, **kwargs):
		context = super(pricequeue_del, self).get_context_data(**kwargs)
		context['object'] = self.data.id
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = reverse('pricetag:pricequeue_list')
		return context
		

		
#@csrf_exempt
#@permission_required('workflow.add_printtask')
def pricequeue_add(request, pk):
	if request.method == 'GET':
		try:
			data = goods.objects.get(id=pk)
		except:
			pass
		else:
			if pricequeue.objects.filter(user=request.user, goods=data).exists():
				tmp={'res': 2, 'data': 'exist',}
				return HttpResponse(json.dumps(tmp), content_type='application/json')
			else:
				p=pricequeue(user=request.user, goods=data)
				p.save()
				tmp={'res': 1, 'data': p.id,}
				return HttpResponse(json.dumps(tmp), content_type='application/json')
	tmp={'res': 0, 'data': u'bad',}
	return HttpResponse(json.dumps(tmp), content_type='application/json')

#@permission_required('workflow.add_printtask')
def pricequeue_clear(request):
	if request.method == 'GET':
		pricequeue.objects.filter(user=request.user).delete()
	return HttpResponseRedirect(reverse('pricetag:pricequeue_list'))
	
	

class Form_imageprice(forms.ModelForm):
	class Meta:
		model = pricequeue
		fields = ['imageprice',]

#@permission_required('workflow.add_printtask')
@csrf_exempt
def pricequeue_price2image_add(request, pk):
	#вызывается битриксом
	if request.method == 'POST' or request.method == 'GET':
		try:
			instance = pricequeue.objects.get(id=request.GET['queueid'], goods__idbitrix=pk)
		except:
			pass
		else:
			f=Form_imageprice(request.POST, request.FILES, instance=instance)
			if f.is_valid():
				cd = f.cleaned_data
				f.save()
				tmp={'res': 1, 'data': u'pricequeue_price2image_add good',}
				return HttpResponse(json.dumps(tmp), content_type='application/json')
			else:
				tmp={'res': 0, 'data': f.errors,}
				return HttpResponse(json.dumps(tmp), content_type='application/json')
	tmp={'res': 0, 'data': u'pricequeue_price2image_add bad',}
	return HttpResponse(json.dumps(tmp), content_type='application/json')
	
