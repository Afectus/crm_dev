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
from acl.models import *
from order.models import *
from panel.form import *
from panel.models import *
from sms.views import *
from sms.models import *
from bitrix.models import *
from worktask.models import *
from log.models import *
from acl.views import get_object_or_denied


import logging
log = logging.getLogger(__name__)


####goodsmotivationratiosum
class shop_list(ListView):
	template_name = 'shop_list.html'
	model = shop
	paginate_by = 60
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'motivation_list', 'R') #проверяем права
		return super(shop_list, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(shop_list, self).get_queryset()
		return data
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(shop_list, self).get_context_data(*args, **kwargs)
		#context_data.update({'task_create': self.data.filter(user=self.request.user, status='open'),})
		return context_data
		
class shop_edit(UpdateView):
	model = shop
	template_name = '_edit2.html'
	success_url = '/'
	fields = ['motivationratio', ]
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'motivation_list', 'R') #проверяем права
		get_object_or_404(self.model, id=self.kwargs['pk'])
		return super(shop_edit, self).dispatch(request, *args, **kwargs)

	def get_success_url(self):
		return reverse('panel:shop_list')



####goodsmotivationratiosum
class goodsmotivationratiosum_list(ListView):
	template_name = 'goodsmotivationratiosum_list.html'
	model = goodsmotivationratiosum
	paginate_by = 60
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'motivation_list', 'R') #проверяем права
		return super(goodsmotivationratiosum_list, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(goodsmotivationratiosum_list, self).get_queryset()
		#data=data.filter()
		return data
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(goodsmotivationratiosum_list, self).get_context_data(*args, **kwargs)
		#context_data.update({'task_create': self.data.filter(user=self.request.user, status='open'),})
		return context_data
		
class goodsmotivationratiosum_edit(UpdateView):
	model = goodsmotivationratiosum
	template_name = '_edit2.html'
	success_url = '/'
	fields = ['name', 'percent', 'dpercent', 'sum', 'dsum', ]
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'motivation_list', 'R') #проверяем права
		get_object_or_404(self.model, id=self.kwargs['pk'])
		return super(goodsmotivationratiosum_edit, self).dispatch(request, *args, **kwargs)

	def get_success_url(self):
		return reverse('panel:goodsmotivationratiosum_list')

##################################################

########################################################
class motivation_report_list_table(TemplateView):
	template_name = "motivation_report_list_table.html"

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'motivation_list', 'R') #проверяем права
		return super(motivation_report_list_table, self).dispatch(request, *args, **kwargs)
	
	def get_context_data(self, *args, **kwargs):
		context_data = super(motivation_report_list_table, self).get_context_data(*args, **kwargs)
		return context_data

###################################################


#######СПИСОК ТОВАРОВ ПУБЛИЧНАЯ ВЕРСИЯ ВЕРСИЯ#########
class Form_filter_goods_public(forms.Form):
	q = forms.CharField(label='Поиск', help_text='Введите слово для поиска', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'off'}), max_length=100, required=False)
	
	barcode = forms.CharField(label='Штрих код', help_text='Работа со сканером шрих кода', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'off'}), max_length=100, required=False)
	
	tax = forms.ModelMultipleChoiceField(label='Категория', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), queryset=tax.objects.all(), required=False)

	stock = forms.ModelMultipleChoiceField(label='Склад', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), queryset=stock.objects.filter(status=True), required=False)
	
	motivation = forms.ModelMultipleChoiceField(label='Категория товара', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), queryset=goodsmotivationratiosum.objects.all(), required=False)
	
	pricefrom = forms.FloatField(label="Цена от", required=False,)
	priceto = forms.FloatField(label="Цена до", required=False,)
	
	video = forms.ChoiceField(label='Видео', widget=forms.Select(attrs={'class': 'form-control'}), choices=(('all', 'Все'),('true', 'Да'),('false', 'Нет'),), initial='all', required=False)
		
	paging = forms.BooleanField(label='На одной странице', initial=True, required=False)
	
	select = forms.CharField(label='Режим выбора', widget=forms.HiddenInput(), initial='false', required=False,)
	
#@method_decorator(permission_required('node.add_goods'), name='dispatch')
class goods_list_public(ListView):
	template_name = 'goods_list_public.html'
	model = goods
	#paginate_by = 10
	
	def dispatch(self, request, *args, **kwargs):
		#проверяем права
		#get_object_or_denied(self.request.user, 'goods_list_public', 'L') #проверяем права
		return super(goods_list_public, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(goods_list_public, self).get_queryset()
		
		data=data.all() #выбираем основной запрос

		data=data.filter(base_id=1) #выбираем основной запрос
		
		#data=data.filter(idbitrix__isnull=False).exclude(idbitrix__exact='') #товары только с idbitrix, исключаем пустые
		
		f=Form_filter_goods_public(self.request.GET)
		
		
		req = ''
		paging = 40
		
		if f.is_valid():
			fdata = f.cleaned_data
			#фильтрация
			if fdata['q']:
				req = '%s&q=%s' % (req, fdata['q'])
				data=data.filter(Q(id__icontains=fdata['q']) | Q(id1c__icontains=fdata['q']) | Q(idbitrix__icontains=fdata['q']) | Q(name__icontains=fdata['q']) | Q(name__search=fdata['q']) | Q(namefull__search=fdata['q']) | Q(namefull__icontains=fdata['q']) | Q(art__icontains=fdata['q']) | Q(bname__search=fdata['q']) | Q(bname__icontains=fdata['q']))
				
			if fdata['barcode']:
				req = '%s&barcode=%s' % (req, fdata['barcode'])
				data=data.filter(Q(barcodelist__barcode__search=fdata['barcode']) | Q(barcodelist__barcode__icontains=fdata['barcode']))

			if fdata['tax']:
				req = '%s&tax=%s' % (req, self.request.GET['tax'])
				#########################################
				########обработка дочерних категорий#####
				#########################################
				datatax=tax.objects.filter(id__in=fdata['tax']).values('id')
				taxin=datatax
				#берем дочернии категории, если есть
				taxparent = tax.objects.filter(parent__in=datatax).values('id')
				if taxparent.exists():
					taxin = taxparent
				#########################################
				data=data.filter(tax__in=taxin).distinct() #distinct() если выбирается из нескольких категорий

			if fdata['stock']:
				req = '%s&stock=%s' % (req, self.request.GET['stock'])
				data=data.filter(goodsinstock__value__gte=1, goodsinstock__stock__in=fdata['stock']).distinct()
				
				
			if fdata['motivation']:
				req = '%s&motivation=%s' % (req, self.request.GET['motivation'])
				data=data.filter(motivationinpoints1__in=fdata['motivation'])
				
			if fdata['pricefrom']: #цена gte больше или равно
				req = '%s&pricefrom=%s' % (req, fdata['pricefrom'])
				data=data.filter(price__gte=fdata['pricefrom'])
			if fdata['priceto']: #цена lte маньше или равно
				req = '%s&priceto=%s' % (req, fdata['priceto'])
				data=data.filter(price__lte=fdata['priceto'])
				
			if fdata['paging']:
				req = '%s&paging=%s' % (req, self.request.GET['paging'])
				paging = 1000
				
			if fdata['video']:
				req = '%s&video=%s' % (req, self.request.GET['video'])
				if fdata['video'] == 'true':
					data=data.exclude(videomp4__exact='')
				if fdata['video'] == 'false':
					data=data.filter(videomp4__exact='')

		self.req = req

		data=data.distinct()

		#paginator
		self.p = Paginator(data, paging)
		#page = self.kwargs['page']
		xpage = self.request.GET.get('xpage', default=1)
		#print self.p.number()
		try:
			pdata = self.p.page(xpage)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			pdata = self.p.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			pdata = self.p.page(self.p.num_pages)	

		return pdata
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(goods_list_public, self).get_context_data(*args, **kwargs)
		context_data.update({'req': self.req,})
		context_data.update({'count': self.p.count,})
		context_data.update({'form': Form_filter_goods_public(self.request.GET, initial={'q': '123',})})
		context_data.update({'urlpage': reverse('panel:goods_list_public'),})
		return context_data

#################################################		


#######СПИСОК ТОВАРОВ ОБЛЕГЧЕННАЯ ВЕРСИЯ#########
class Form_filter_goods_light(forms.Form):
	q = forms.CharField(label='Поиск', help_text='Введите слово для поиска', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'off'}), max_length=100, required=False)
	
	barcode = forms.CharField(label='Штрих код', help_text='Работа со сканером шрих кода', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'off'}), max_length=100, required=False)
	
	tax = forms.ModelMultipleChoiceField(label='Категория', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), queryset=tax.objects.all(), required=False)

	paging = forms.BooleanField(label='На одной странице', initial=True, required=False)
	
#@method_decorator(permission_required('node.add_goods'), name='dispatch')
class goods_list_light(ListView):
	template_name = 'goods_list_light.html'
	model = goods
	#paginate_by = 10
	
	def dispatch(self, request, *args, **kwargs):
		#проверяем права
		get_object_or_denied(self.request.user, 'goods_light', 'L') #проверяем права
		return super(goods_list_light, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(goods_list_light, self).get_queryset()
		
		data=data.all() #выбираем основной запрос
		
		data=data.filter(base_id=1) #выбираем основной запрос
		
		data=data.filter(idbitrix__isnull=False).exclude(idbitrix__exact='') #товары только с idbitrix, исключаем пустые
		
		f=Form_filter_goods_light(self.request.GET)
		
		
		req = ''
		paging = 40
		
		if f.is_valid():
			fdata = f.cleaned_data
			#фильтрация
			if fdata['q']:
				req = '%s&q=%s' % (req, fdata['q'])
				data=data.filter(Q(id__icontains=fdata['q']) | Q(id1c__icontains=fdata['q']) | Q(idbitrix__icontains=fdata['q']) | Q(name__icontains=fdata['q']) | Q(name__search=fdata['q']) | Q(namefull__search=fdata['q']) | Q(namefull__icontains=fdata['q']) | Q(art__icontains=fdata['q']) | Q(bname__search=fdata['q']) | Q(bname__icontains=fdata['q']))
				
			if fdata['barcode']:
				req = '%s&barcode=%s' % (req, fdata['barcode'])
				data=data.filter(Q(barcodelist__barcode__search=fdata['barcode']) | Q(barcodelist__barcode__icontains=fdata['barcode']))

			if fdata['tax']:
				req = '%s&tax=%s' % (req, self.request.GET['tax'])
				#########################################
				########обработка дочерних категорий#####
				#########################################
				datatax=tax.objects.filter(id__in=fdata['tax']).values('id')
				taxin=datatax
				#берем дочернии категории, если есть
				taxparent = tax.objects.filter(parent__in=datatax).values('id')
				if taxparent.exists():
					taxin = taxparent
				#########################################
				data=data.filter(tax__in=taxin).distinct() #distinct() если выбирается из нескольких категорий

			if fdata['paging']:
				req = '%s&paging=%s' % (req, self.request.GET['paging'])
				paging = 1000

		self.req = req

		data=data.distinct()

		#paginator
		self.p = Paginator(data, paging)
		#page = self.kwargs['page']
		xpage = self.request.GET.get('xpage', default=1)
		#print self.p.number()
		try:
			pdata = self.p.page(xpage)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			pdata = self.p.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			pdata = self.p.page(self.p.num_pages)	

		return pdata
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(goods_list_light, self).get_context_data(*args, **kwargs)
		context_data.update({'req': self.req,})
		context_data.update({'count': self.p.count,})
		context_data.update({'form': Form_filter_goods_light(self.request.GET, initial={'q': '123',})})
		context_data.update({'urlpage': '/goods/list/light',})
		return context_data

class Form_goods_edit_light(forms.ModelForm):
	#saveonclose = forms.BooleanField(required=False, widget=forms.HiddenInput())
	saveonclose = forms.CharField(widget=forms.HiddenInput(), max_length=10, required=False)
	class Meta:
		model = goods
		fields = ['videomp4',]
		

class goods_edit_light(UpdateView):
	model = goods
	template_name = 'goods_edit_light.html'
	success_url = '/goods/list/light'
	form_class = Form_goods_edit_light
	#fields = ['videomp4',]
	#
	saveonclose = False #Кнопка Сохранить и закрыть
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'goods_light', 'U') #проверяем права
		return super(goods_edit_light, self).dispatch(request, *args, **kwargs)
	
	def get_success_url(self):
		url = '/goods/edit/light/%s' % (self.get_object().id)
		if self.saveonclose:
			url = reverse('panel:saveonclose')
		return url
	
	def get_context_data(self, **kwargs):
		context = super(goods_edit_light, self).get_context_data(**kwargs)
		context['object'] = self.get_object()
		return context
	
	def form_valid(self, form):
		self.object = form.save(commit=False)
		# self.object.user = self.request.user
		# self.object.save()
		if form.cleaned_data['saveonclose'] == 'true':
			self.saveonclose = True
		return super(goods_edit_light, self).form_valid(form)

#################################################		
		
		
		
class Form_filter_goods(forms.Form):
	q = forms.CharField(label='Поиск', help_text='Введите слово для поиска', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'off'}), max_length=100, required=False)
	barcode = forms.CharField(label='Штрих код', help_text='Работа со сканером шрих кода', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'off'}), max_length=100, required=False)
	tax = forms.ModelMultipleChoiceField(label='Категория', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), queryset=tax.objects.all(), required=False)
	#sort = forms.ChoiceField(label='Сортировка', help_text='Сортировать по полю', widget=forms.Select(attrs={'class': 'form-control'}), choices=(('id', 'id'),('bday', 'Д. Рождения'),('f', 'Фамилия'),('i', 'Имя'),('o', 'Отчество')), required=False)
	stock = forms.ModelMultipleChoiceField(label='Склад', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '3',}), queryset=stock.objects.filter(status=True), required=False)
	
	base = forms.ModelMultipleChoiceField(label='База 1с', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '3',}), queryset=base1c.objects.all(), required=False, initial=2)
	
	pricefrom = forms.FloatField(label="Цена от", required=False,)
	priceto = forms.FloatField(label="Цена до", required=False,)
	
	paging = forms.BooleanField(label='На одной странице', initial=True, required=False)
	instock = forms.BooleanField(label='В наличии', initial=True, required=False)
	
	#
	showondemo = forms.BooleanField(label='Показывать в демо', initial=False, required=False)
	touchscreen = forms.BooleanField(label='Отображать на тачскринах', initial=False, required=False)
	
	certexist = forms.ChoiceField(label='Наличие сертификата', widget=forms.Select(attrs={'class': 'form-control'}), choices=(('all', 'Все'),('true', 'Да'),('false', 'Нет'),), initial='all', required=False)
	
#@method_decorator(permission_required('node.add_goods'), name='dispatch')
class goods_list(ListView):
	template_name = 'goods_list.html'
	model = goods
	#paginate_by = 10
	
	def dispatch(self, request, *args, **kwargs):
		#проверяем права
		get_object_or_denied(self.request.user, 'goods', 'L') #проверяем права
		return super(goods_list, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(goods_list, self).get_queryset()
		
		data=data.all() #выбираем основной запрос
		
		f=Form_filter_goods(self.request.GET)
		
		
		req = ''
		paging = 40
		
		if f.is_valid():
			fdata = f.cleaned_data
			#фильтрация
			if fdata['q']:
				req = '%s&q=%s' % (req, fdata['q'])
				data=data.filter(Q(id__icontains=fdata['q']) | Q(id1c__icontains=fdata['q']) | Q(idbitrix__icontains=fdata['q']) | Q(name__icontains=fdata['q']) | Q(name__search=fdata['q']) | Q(namefull__search=fdata['q']) | Q(namefull__icontains=fdata['q']) | Q(art__icontains=fdata['q']) | Q(bname__search=fdata['q']) | Q(bname__icontains=fdata['q']))
				
			if fdata['barcode']:
				req = '%s&barcode=%s' % (req, fdata['barcode'])
				data=data.filter(Q(barcodelist__barcode__search=fdata['barcode']) | Q(barcodelist__barcode__icontains=fdata['barcode']))

			if fdata['tax']:
				req = '%s&tax=%s' % (req, self.request.GET['tax'])
				#########################################
				########обработка дочерних категорий#####
				#########################################
				datatax=tax.objects.filter(id__in=fdata['tax']).values('id')
				taxin=datatax
				#берем дочернии категории, если есть
				taxparent = tax.objects.filter(parent__in=datatax).values('id')
				if taxparent.exists():
					taxin = taxparent
				#########################################
				data=data.filter(tax__in=taxin).distinct() #distinct() если выбирается из нескольких категорий

			if fdata['stock']:
				req = '%s&stock=%s' % (req, self.request.GET['stock'])
				data=data.filter(qinstock__value__gte=1, qinstock__stock__in=fdata['stock']).distinct()
				
			if fdata['base']:
				req = '%s&base=%s' % (req, self.request.GET['base'])
				data=data.filter(base=fdata['base'])
				
			if fdata['pricefrom']: #цена gte больше или равно
				req = '%s&pricefrom=%s' % (req, fdata['pricefrom'])
				data=data.filter(price__gte=fdata['pricefrom'])
			if fdata['priceto']: #цена lte маньше или равно
				req = '%s&priceto=%s' % (req, fdata['priceto'])
				data=data.filter(price__lte=fdata['priceto'])

			#if fdata['sort']:
			#	req = '%s&sort=%s' % (req, self.request.GET['sort'])
			#	data=data.order_by(fdata['sort'])
			
			
			if fdata['paging']:
				req = '%s&paging=%s' % (req, self.request.GET['paging'])
				paging = 1000
				
			if fdata['instock']: #в наличии, количество больше 1
				req = '%s&instock=%s' % (req, self.request.GET['instock'])
				data=data.filter(qinstock__value__gte=1).distinct() #направильное считал, сейчас это лишнее
				
			if fdata['showondemo']:
				req = '%s&showondemo=%s' % (req, self.request.GET['showondemo'])
				data=data.filter(showondemo=True)
			if fdata['touchscreen']:
				req = '%s&touchscreen=%s' % (req, self.request.GET['touchscreen'])
				data=data.filter(touchscreen=True)
				
			if fdata['certexist']:
				req = '%s&certexist=%s' % (req, self.request.GET['certexist'])
				if fdata['certexist'] == 'true':
					data=data.filter(goodscert__isnull=False)
				if fdata['certexist'] == 'false':
					data=data.filter(goodscert__isnull=True)
				
		#подсчет количества по остаткам на складах
		self.sum=data.aggregate(s=Sum('qinstock__value'))

		self.req = req

		################# исключение категории для отладки
		#t = tax.objects.get(id=18)
		#data=data.exclude(tax=t)
		#self.sum=data.exclude(tax=t).aggregate(s=Sum('qinstock__value'))
		#######################
		
		data=data.distinct()
		
		#paginator
		self.p = Paginator(data, paging)
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
		context_data = super(goods_list, self).get_context_data(*args, **kwargs)
		context_data.update({'req': self.req,})
		context_data.update({'count': self.p.count,})
		context_data.update({'form': Form_filter_goods(self.request.GET, initial={'q': '123',})})
		context_data.update({'sum': self.sum})
		
		return context_data


		
		
#@method_decorator(permission_required('node.add_goods'), name='dispatch')
class goods_detail(DetailView):
	model = goods
	template_name = 'goods_detail.html'
	
	def dispatch(self, request, *args, **kwargs):
		#self.data = get_object_or_404(self.model, id=self.kwargs['pk'])
		get_object_or_denied(self.request.user, 'goods', 'R') #проверяем права
		return super(goods_detail, self).dispatch(request, *args, **kwargs)
	
	# def get_object(self, queryset=None):
		# return self.data

	def get_context_data(self, **kwargs):
		context = super(goods_detail, self).get_context_data(**kwargs)
		#context['servername'] = self.data.name
		return context


		
class Form_goods_edit(forms.ModelForm):
	#saveonclose = forms.BooleanField(required=False, widget=forms.HiddenInput())
	saveonclose = forms.CharField(widget=forms.HiddenInput(), max_length=10, required=False)
	class Meta:
		model = goods
		fields = ['status', 'name', 'idbitrix', 'video', 'videomp4', 'goodscert', 'namefull', 'manualstartprice', 'motivationinpoints1', 'art', 'desc', 'price', 'catalogshow', 'showondemo', 'touchscreen', 'tax', 'bname', 'nabor', ]
		
		
#@method_decorator(permission_required('node.add_goods'), name='dispatch')
class goods_edit(UpdateView):
	model = goods
	template_name = 'goods_edit.html'
	success_url = '/goods/list'
	form_class = Form_goods_edit
	#fields = ['status', 'name', 'cert', 'namefull', 'art', 'desc', 'price', 'showondemo', 'touchscreen', 'video', 'tax', 'bname', 'nabor', ]
	#
	saveonclose = False #Кнопка Сохранить и закрыть
	
	
	def dispatch(self, request, *args, **kwargs):
		#self.e = get_object_or_404(self.model, id=self.kwargs['pk'], user=request.user) #ПОТОМ ВКЛЮЧИТЬ
		#проверяем права
		get_object_or_denied(self.request.user, 'goods', 'U') #проверяем права
		return super(goods_edit, self).dispatch(request, *args, **kwargs)
	
	def get_success_url(self):
		url = '/goods/edit/%s' % (self.get_object().id)
		if self.saveonclose:
			url = reverse('panel:saveonclose')
		return url
	
	def get_context_data(self, **kwargs):
		context = super(goods_edit, self).get_context_data(**kwargs)
		context['object'] = self.get_object()
		return context
	
	# def get_initial(self):
		# return {'buyer':self.b, 'user': self.request.user}
	
	# def get_form(self, form_class=None):
		# if form_class is None:
			# form_class = self.get_form_class()
			# form = super(goods_edit, self).get_form(form_class)
			# form.fields['saveonclose'].widget=forms.HiddenInput()
			# return form
		# return form_class(**self.get_form_kwargs())
	
	def form_valid(self, form):
		self.object = form.save(commit=False)
		# self.object.user = self.request.user
		# self.object.save()
		if form.cleaned_data['saveonclose'] == 'true':
			self.saveonclose = True
		return super(goods_edit, self).form_valid(form)
		
	#def form_invalid(self, form):
		#print form.errors
	#	return super(goods_edit, self).form_invalid(form)
		
		

		