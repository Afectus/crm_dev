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


from django.db.models import Min, Max, Sum, Count, Avg
from django.db.models import Q, F, Func, Value, IntegerField, FloatField, CharField, Case, When

from django.db.models.functions import Cast, Trunc, TruncMonth, ExtractYear, ExtractMonth, ExtractWeek, ExtractWeekDay, ExtractDay

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
from device.models import *
from acl.models import *
from acl.views import get_object_or_denied

import logging
log = logging.getLogger(__name__)


		
class report_list(TemplateView):
	template_name = "report_list.html"




class Form_filter_check(forms.Form):
	q = forms.CharField(label='Поиск', help_text='Введите слово для поиска', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'off'}), max_length=100, required=False)

	goods = forms.ModelMultipleChoiceField(label=u'Товар', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), queryset=goods.objects.all(), required=False)
	
	ncheck = forms.CharField(label='Номер чека', help_text='номер чека по 1c например 5046', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'off'}), max_length=100, required=False)
	barcode = forms.CharField(label='Штрих код', help_text='Работа со сканером шрих кода', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'off'}), max_length=100, required=False)
	
	#time
	timestart = forms.DateField(label="Время от", help_text='Время чека от', input_formats=['%d-%m-%y', '%d/%m/%y', '%d.%m.%y', '%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y',], required=False, widget=forms.TextInput(attrs={'class':'form-control datepicker',  'data-dateformat': "dd-mm-yy"}), initial=datetime.date.today())

	timeend = forms.DateField(label="Время до", help_text='Время чека до', input_formats=['%d-%m-%y', '%d/%m/%y', '%d.%m.%y', '%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y',], required=False, widget=forms.TextInput(attrs={'class':'form-control datepicker',  'data-dateformat': "dd-mm-yy"}))
	timedm = forms.BooleanField(label="Игнорировать год", required=False, initial=False,)
	#

	tax = forms.ModelMultipleChoiceField(label='Категория', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), queryset=tax.objects.all(), required=False)
	
	discount = forms.ModelMultipleChoiceField(label='Скидки', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), queryset=discounts.objects.all(), required=False)
	
	shop = forms.ModelMultipleChoiceField(label='Магазины', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '5',}), queryset=shop.objects.all(), required=False)
	
	cashbox = forms.ModelMultipleChoiceField(label='Касса', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '5',}), queryset=cashbox.objects.all(), required=False)
	
	stock = forms.ModelMultipleChoiceField(label='Склад', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '5',}), queryset=stock.objects.filter(status=True), required=False)
	
	pricefrom = forms.FloatField(label="Цена товара от", required=False,)
	priceto = forms.FloatField(label="Цена товара до", required=False,)
	
	beznal = forms.BooleanField(label='Без наличный расчет', initial=True, required=False)
	checksumfrom = forms.FloatField(label="Сумма чека от", required=False,)
	checksumto = forms.FloatField(label="Сумма чека до", required=False,)
	
	paging = forms.BooleanField(label='На одной странице', required=False)
	instock = forms.BooleanField(label='В наличии', required=False)
	inbuyer = forms.BooleanField(label='Покупатель определен', required=False)
	
	
	sortchoice=(
		('nckkm', 'Номер чека'),
		('time', 'Время (старые)'),
		('-time', 'Время (новые)'),
		('nal', 'Оплата наличные (меньше)'),
		('-nal', 'Оплата наличные (Больше)'),
		('beznal', 'Оплата без наличные (меньше)'),
		('-beznal', 'Оплата без наличные (Больше)'),
		('bonuspay', 'Оплата бонусы (меньше)'),
		('-bonuspay', 'Оплата бонусы (Больше)'),
		('bonusadd', 'Начисление бонусов (меньше)'),
		('-bonusadd', 'Начисление бонусов (Больше)'),
		)
	
	sort = forms.ChoiceField(label='Сортировка', help_text='Сортировать по полю', widget=forms.Select(attrs={'class': 'form-control'}), choices=sortchoice, required=False)
	
	operation = forms.ChoiceField(label='Вид операции', help_text='Вид операции', widget=forms.Select(attrs={'class': 'form-control'}), choices=operationchoice, required=False)
	
	#
	process = forms.ChoiceField(label='Процесс', help_text='Процесс', widget=forms.Select(attrs={'class': 'form-control'}), choices=(('', '-'), ('test', 'Тестовый чек'), ('invalid', 'Не валидный'), ('valid', 'Валидный')), required=False)
	
	methodadd = forms.ChoiceField(label='Откуда загружен', help_text='Откуда загружен', widget=forms.Select(attrs={'class': 'form-control'}), choices=(('', '-'), ('csv', 'CSV'), ('json', 'JSON'),), required=False)

	
	
#@method_decorator(permission_required('node.add_check'), name='dispatch')		
class report_sale_list(ListView):
	template_name = "report_sale_list.html"
	model = check
	#paginate_by = 20
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'report', 'R') #проверяем права
		if "timestart" not in request.GET:
			startdate = datetime.datetime.now() + datetime.timedelta(days=-5)
			enddate = datetime.datetime.now() + datetime.timedelta(days=5)
			return HttpResponseRedirect('/report/sale/list/?timestart=%s&timeend=%s' % (startdate.strftime('%d-%m-%Y'), enddate.strftime('%d-%m-%Y')))
		return super(report_sale_list, self).dispatch(request, *args, **kwargs)
	
	def get_queryset(self):
		data=super(report_sale_list, self).get_queryset()
		
		data=data.all() #выбираем основной запрос
		
		f=Form_filter_check(self.request.GET)
		
		
		req = ''
		paging = 40
		
		self.checkreturn=None
		self.discountreport=None
		self.topgoodssold=None
		self.checkreport=None
		
		if f.is_valid():
			fdata = f.cleaned_data
			#фильтрация
			# if fdata['q']:
				# req = '%s&q=%s' % (req, fdata['q'])
				# data=data.filter(Q(buyer__phone__icontains=fdata['q']) | Q(buyer__f__search=fdata['q']) | Q(buyer__i__icontains=fdata['q']) | Q(buyer__o__icontains=fdata['q']))
			
			# if fdata['goods']:
				# req = '%s&goods=%s' % (req, self.request.GET['goods'])
				# data=data.filter(checkitem__goods__in=fdata['goods']).distinct()
				
			# if fdata['ncheck']:
				# req = '%s&ncheck=%s' % (req, self.request.GET['ncheck'])
				# data=data.filter(nckkm=fdata['ncheck'])
	
			# if fdata['barcode']:
				# req = '%s&barcode=%s' % (req, fdata['barcode'])
				# data=data.filter(checkitem__goods__barcode=fdata['barcode'])
	
			if fdata['timestart'] and fdata['timeend']:
				req = '%s&timestart=%s' % (req, self.request.GET['timestart'])
				req = '%s&timeend=%s' % (req, self.request.GET['timeend'])
				if fdata['timedm'] == True: #фильтр только день месяц, игнорировать год
					req = '%s&timedm=%s' % (req, self.request.GET['timedm'])
					s = fdata['timestart']
					e = fdata['timeend']
					count = (e-s).days
					count=count+1
					dlist = []
					for x in range(0, count):
						dlist.append(s + datetime.timedelta(days=x))
					dindex = []
					for date in dlist:
						dindex.append(date.strftime("%d%m")) 
					data=data.filter(timeindex__in=dindex)	 
				else: #полный фильтр день месяц год
					data=data.filter(time__range=(fdata['timestart'], fdata['timeend']))	

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
				data=data.filter(checkitem__goods__tax__in=taxin).distinct()
			
			# if fdata['discount']:
				# req = '%s&discount=%s' % (req, self.request.GET['discount'])
				# data=data.filter(checkitem__checkd__discounts__in=fdata['discount']).distinct()

			if fdata['shop']:
				req = '%s&shop=%s' % (req, self.request.GET['shop'])
				data=data.filter(shop__in=fdata['shop'])
			
			# if fdata['cashbox']:
				# req = '%s&cashbox=%s' % (req, self.request.GET['cashbox'])
				# data=data.filter(cashbox__in=fdata['cashbox'])
			
			# if fdata['stock']:
				# req = '%s&stock=%s' % (req, self.request.GET['stock'])
				# data=data.filter(checkitem__goods__qinstock__value__gte=1, checkitem__goods__qinstock__stock__in=fdata['stock']).distinct()

			# if fdata['pricefrom']: #цена gte больше или равно
				# req = '%s&pricefrom=%s' % (req, fdata['pricefrom'])
				# data=data.filter(checkitem__goods__price__gte=fdata['pricefrom'])
			# if fdata['priceto']: #цена lte маньше или равно
				# req = '%s&priceto=%s' % (req, fdata['priceto'])
				# data=data.filter(checkitem__goods__price__lte=fdata['priceto'])
				
			#nal
			# if fdata['beznal']:
				# req = '%s&beznal=%s' % (req, fdata['beznal'])
				# if fdata['checksumfrom'] and fdata['checksumto']:
					# if fdata['checksumfrom']: #цена gte больше или равно
						# req = '%s&checksumfrom=%s' % (req, fdata['checksumfrom'])
						# data=data.filter(beznal__gte=fdata['checksumfrom'])
					# if fdata['checksumto']: #цена lte маньше или равно
						# req = '%s&checksumto=%s' % (req, fdata['checksumto'])
						# data=data.filter(beznal__lte=fdata['checksumto'])
				# else:
					# data=data.filter(beznal__gte=1)
			# else:
				# if fdata['checksumfrom']: #цена gte больше или равно
					# req = '%s&checksumfrom=%s' % (req, fdata['checksumfrom'])
					# data=data.filter(nal__gte=fdata['checksumfrom'])
				# if fdata['checksumto']: #цена lte маньше или равно
					# req = '%s&checksumto=%s' % (req, fdata['checksumto'])
					# data=data.filter(nal__lte=fdata['checksumto'])

			# if fdata['paging']:
				# req = '%s&paging=%s' % (req, self.request.GET['paging'])
				# paging = 1000
			
			# if fdata['instock']: #в наличии, количество больше 1
				# req = '%s&instock=%s' % (req, self.request.GET['instock'])
				# data=data.filter(checkitem__goods__qinstock__value__gte=1).distinct() #направильное считал, сейчас это лишнее
				
			if fdata['inbuyer']: #покупатель присутствует
				req = '%s&inbuyer=%s' % (req, self.request.GET['inbuyer'])
				data=data.filter(buyer__isnull=False)

			if fdata['sort']:
				req = '%s&sort=%s' % (req, self.request.GET['sort'])
				data=data.order_by(fdata['sort'])
			
			
			if fdata['operation']:
				req = '%s&operation=%s' % (req, self.request.GET['operation'])
				self.checkreturn=data.filter(operation='return').count()
				data=data.filter(operation=fdata['operation'])
			else:
				self.checkreturn=data.filter(operation='return').count()
				data=data.filter(operation='sale')
				
			#
			if fdata['process']:
				req = '%s&process=%s' % (req, self.request.GET['process'])
				data=data.filter(process=fdata['process'])
				
			if fdata['methodadd']:
				req = '%s&methodadd=%s' % (req, self.request.GET['methodadd'])
				data=data.filter(methodadd=fdata['methodadd'])

	
		self.req = req
		self.data = data.filter().distinct()
		
		#отчет чеки
		self.c_avg_nodiscount = self.data.aggregate(s=Avg('checkitem__sum'))['s']
		self.c_total_nodiscount = self.data.aggregate(s=Sum('checkitem__sum'))['s']
		self.c_min_nodiscount = self.data.aggregate(s=Min('checkitem__sum'))['s']
		self.c_max_nodiscount = self.data.aggregate(s=Max('checkitem__sum'))['s']

		################# исключение категории для отладки
		#t = tax.objects.get(id=18)
		#data=data.exclude(tax=t)
		#self.sum=data.exclude(tax=t).aggregate(s=Sum('qinstock__value'))
		#######################
		
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
		context_data = super(report_sale_list, self).get_context_data(*args, **kwargs)
		context_data.update({'form': Form_filter_check(self.request.GET),})
		context_data.update({'req': self.req,})
		context_data.update({'count': self.p.count,})
		#
		context_data.update({'c_avg_nodiscount': self.c_avg_nodiscount,})
		context_data.update({'c_total_nodiscount': self.c_total_nodiscount,})
		context_data.update({'c_min_nodiscount': self.c_min_nodiscount,})
		context_data.update({'c_max_nodiscount': self.c_max_nodiscount,})
		return context_data
			
	
	
	
	
	
'''
#@method_decorator(permission_required('node.add_check'), name='dispatch')		
class report_sale(ListView):
	template_name = "report_sale.html"
	model = check
	#paginate_by = 20
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'report', 'R')
		if "timestart" not in request.GET:
			startdate = datetime.datetime.now() + datetime.timedelta(days=-60)
			enddate = datetime.datetime.now() + datetime.timedelta(days=60)
			return HttpResponseRedirect('/report/sale/1/?timestart=%s&timeend=%s' % (startdate.strftime('%d-%m-%Y'), enddate.strftime('%d-%m-%Y')))
		return super(report_sale, self).dispatch(request, *args, **kwargs)
	
	def get_queryset(self):
		data=super(report_sale, self).get_queryset()
		
		data=data.all() #выбираем основной запрос
		
		f=Form_filter_check(self.request.GET)
		
		
		req = ''
		paging = 40
		
		self.checkreturn=None
		self.discountreport=None
		self.topgoodssold=None
		self.checkreport=None
		
		if f.is_valid():
			fdata = f.cleaned_data
			#фильтрация
			if fdata['q']:
				req = '%s&q=%s' % (req, fdata['q'])
				data=data.filter(Q(buyer__phone__icontains=fdata['q']) | Q(buyer__f__search=fdata['q']) | Q(buyer__i__icontains=fdata['q']) | Q(buyer__o__icontains=fdata['q']))
			
			if fdata['goods']:
				req = '%s&goods=%s' % (req, self.request.GET['goods'])
				data=data.filter(checkitem__goods__in=fdata['goods']).distinct()
				
			if fdata['ncheck']:
				req = '%s&ncheck=%s' % (req, self.request.GET['ncheck'])
				data=data.filter(nckkm=fdata['ncheck'])
	
			if fdata['barcode']:
				req = '%s&barcode=%s' % (req, fdata['barcode'])
				data=data.filter(checkitem__goods__barcode=fdata['barcode'])
	
			if fdata['timestart'] and fdata['timeend']:
				req = '%s&timestart=%s' % (req, self.request.GET['timestart'])
				req = '%s&timeend=%s' % (req, self.request.GET['timeend'])
				if fdata['timedm'] == True: #фильтр только день месяц, игнорировать год
					req = '%s&timedm=%s' % (req, self.request.GET['timedm'])
					s = fdata['timestart']
					e = fdata['timeend']
					count = (e-s).days
					count=count+1
					dlist = []
					for x in range(0, count):
						dlist.append(s + datetime.timedelta(days=x))
					dindex = []
					for date in dlist:
						dindex.append(date.strftime("%d%m")) 
					data=data.filter(timeindex__in=dindex)	 
				else: #полный фильтр день месяц год
					data=data.filter(time__range=(fdata['timestart'], fdata['timeend']))	

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
				data=data.filter(checkitem__goods__tax__in=taxin).distinct()
			
			if fdata['discount']:
				req = '%s&discount=%s' % (req, self.request.GET['discount'])
				data=data.filter(checkitem__checkd__discounts__in=fdata['discount']).distinct()

			if fdata['shop']:
				req = '%s&shop=%s' % (req, self.request.GET['shop'])
				data=data.filter(shop__in=fdata['shop'])
			
			if fdata['cashbox']:
				req = '%s&cashbox=%s' % (req, self.request.GET['cashbox'])
				data=data.filter(cashbox__in=fdata['cashbox'])
			
			if fdata['stock']:
				req = '%s&stock=%s' % (req, self.request.GET['stock'])
				data=data.filter(checkitem__goods__qinstock__value__gte=1, checkitem__goods__qinstock__stock__in=fdata['stock']).distinct()

			if fdata['pricefrom']: #цена gte больше или равно
				req = '%s&pricefrom=%s' % (req, fdata['pricefrom'])
				data=data.filter(checkitem__goods__price__gte=fdata['pricefrom'])
			if fdata['priceto']: #цена lte маньше или равно
				req = '%s&priceto=%s' % (req, fdata['priceto'])
				data=data.filter(checkitem__goods__price__lte=fdata['priceto'])
				
			#nal
			if fdata['beznal']:
				req = '%s&beznal=%s' % (req, fdata['beznal'])
				if fdata['checksumfrom'] and fdata['checksumto']:
					if fdata['checksumfrom']: #цена gte больше или равно
						req = '%s&checksumfrom=%s' % (req, fdata['checksumfrom'])
						data=data.filter(beznal__gte=fdata['checksumfrom'])
					if fdata['checksumto']: #цена lte маньше или равно
						req = '%s&checksumto=%s' % (req, fdata['checksumto'])
						data=data.filter(beznal__lte=fdata['checksumto'])
				else:
					data=data.filter(beznal__gte=1)
			else:
				if fdata['checksumfrom']: #цена gte больше или равно
					req = '%s&checksumfrom=%s' % (req, fdata['checksumfrom'])
					data=data.filter(nal__gte=fdata['checksumfrom'])
				if fdata['checksumto']: #цена lte маньше или равно
					req = '%s&checksumto=%s' % (req, fdata['checksumto'])
					data=data.filter(nal__lte=fdata['checksumto'])

			if fdata['paging']:
				req = '%s&paging=%s' % (req, self.request.GET['paging'])
				paging = 1000
			
			if fdata['instock']: #в наличии, количество больше 1
				req = '%s&instock=%s' % (req, self.request.GET['instock'])
				data=data.filter(checkitem__goods__qinstock__value__gte=1).distinct() #направильное считал, сейчас это лишнее
				
			if fdata['inbuyer']: #покупатель присутствует
				req = '%s&inbuyer=%s' % (req, self.request.GET['inbuyer'])
				data=data.filter(buyer__isnull=False)

			if fdata['sort']:
				req = '%s&sort=%s' % (req, self.request.GET['sort'])
				data=data.order_by(fdata['sort'])
			
			
			if fdata['operation']:
				req = '%s&operation=%s' % (req, self.request.GET['operation'])
				self.checkreturn=data.filter(operation='return').count()
				data=data.filter(operation=fdata['operation'])
			else:
				self.checkreturn=data.filter(operation='return').count()
				data=data.filter(operation='sale')

				
			
			
				
			#ОТЧЕТ ПО ЧЕКАМ
			self.checkreport=checkitem.objects.filter(fcheck__in=data)	
			#ОТЧЕТ ПО ТОВАРАМ
			self.goodsreportview=False
			if fdata['goods']:
				#print fdata['goods']
				#for i in fdata['goods']:
				#	print i.id

				self.goodsreport=checkitem.objects.filter(goods__id=fdata['goods'], fcheck__in=data)
			
			#ОТЧЕТ ПО СКИДКАМ
			self.discountreport=None
			if fdata['discount']:
				self.discountreport=fdata['discount'].filter(checkd__checkitem__fcheck__in=data).annotate(sum_discount=Sum('checkd__discount'))
		
			#ТОП ПРОДАВАЕМЫХ ТОВАРОВ
			if fdata['tax']:
				self.topgoodssold=goods.objects.filter(checkitem__fcheck__in=data, checkitem__goods__tax__in=taxin).annotate(c=Count('checkitem__col'), s=Sum('checkitem__sum')).order_by('-s')[:30]
			else:
				self.topgoodssold=goods.objects.filter(checkitem__fcheck__in=data).annotate(c=Count('checkitem__col'), s=Sum('checkitem__sum')).order_by('-s')[:30]
	
		
		self.req = req
		self.data = data.filter().distinct()

		################# исключение категории для отладки
		#t = tax.objects.get(id=18)
		#data=data.exclude(tax=t)
		#self.sum=data.exclude(tax=t).aggregate(s=Sum('qinstock__value'))
		#######################
		
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
		context_data = super(report_sale, self).get_context_data(*args, **kwargs)
		context_data.update({'form': Form_filter_check(self.request.GET),})
		context_data.update({'req': self.req,})
		context_data.update({'checkcount': self.p.count,})
		
		context_data.update({'checkreturn': self.checkreturn ,})
		
		context_data.update({'discountreport': self.discountreport,})
		
		#ТОП ПРОДАВАЕМЫХ ТОВАРОВ
		context_data.update({'topgoodssold': self.topgoodssold,})
		
		#ОТЧЕТ ПО ЧЕКАМ
		context_data.update({'checkitems': self.checkreport.count(),})
		context_data.update({'checkitemscol': self.checkreport.aggregate(c=Sum('col'))['c'],})
		
		context_data.update({'c_total_nodiscount': self.checkreport.aggregate(c=Sum(F('price')*F('col')))['c'],})
		context_data.update({'c_total_discount': self.checkreport.aggregate(c=Sum('checkd__discount'))['c'],})
		context_data.update({'c_total_sum': self.checkreport.aggregate(c=Sum('sum'))['c'],})
		context_data.update({'c_total_nal': self.data.aggregate(c=Sum('nal'))['c'],})
		context_data.update({'c_total_beznal': self.data.aggregate(c=Sum('beznal'))['c'],})
		context_data.update({'c_total_bonuspay': self.data.aggregate(c=Sum('bonuspay'))['c'],})
		context_data.update({'c_total_bonusadd': self.data.aggregate(c=Sum('bonusadd'))['c'],})

		context_data.update({'c_min_nodiscount': self.checkreport.aggregate(c=Min(F('price')*F('col')))['c'],})
		context_data.update({'c_min_discount': self.checkreport.aggregate(c=Min('checkd__discount'))['c'],})
		context_data.update({'c_min_sum': self.checkreport.aggregate(c=Min('sum'))['c'],})
		context_data.update({'c_min_nal': self.data.aggregate(c=Min('nal'))['c'],})
		context_data.update({'c_min_beznal': self.data.aggregate(c=Min('beznal'))['c'],})
		context_data.update({'c_min_bonuspay': self.data.aggregate(c=Min('bonuspay'))['c'],})
		context_data.update({'c_min_bonusadd': self.data.aggregate(c=Min('bonusadd'))['c'],})
		
		context_data.update({'c_max_nodiscount': self.checkreport.aggregate(c=Max(F('price')*F('col')))['c'],})
		context_data.update({'c_max_discount': self.checkreport.aggregate(c=Max('checkd__discount'))['c'],})
		context_data.update({'c_max_sum': self.checkreport.aggregate(c=Max('sum'))['c'],})
		context_data.update({'c_max_nal': self.data.aggregate(c=Max('nal'))['c'],})
		context_data.update({'c_max_beznal': self.data.aggregate(c=Max('beznal'))['c'],})
		context_data.update({'c_max_bonuspay': self.data.aggregate(c=Max('bonuspay'))['c'],})
		context_data.update({'c_max_bonusadd': self.data.aggregate(c=Max('bonusadd'))['c'],})
		
		context_data.update({'c_avg_nodiscount': self.checkreport.aggregate(c=Avg(F('price')*F('col')))['c'],})
		context_data.update({'c_avg_discount': self.checkreport.aggregate(c=Avg('checkd__discount'))['c'],})
		context_data.update({'c_avg_sum': self.checkreport.aggregate(c=Avg('sum'))['c'],})
		context_data.update({'c_avg_nal': self.data.aggregate(c=Avg('nal'))['c'],})
		context_data.update({'c_avg_beznal': self.data.aggregate(c=Avg('beznal'))['c'],})
		context_data.update({'c_avg_bonuspay': self.data.aggregate(c=Avg('bonuspay'))['c'],})
		context_data.update({'c_avg_bonusadd': self.data.aggregate(c=Avg('bonusadd'))['c'],})
		
		
		#подсчет отфильтрованного товара
		
		if self.goodsreportview:
			context_data.update({'goodsreportview': self.goodsreportview,})
			context_data.update({'g_total_nodiscount': self.goodsreport.aggregate(c=Sum(F('price')*F('col')))['c'],})
			context_data.update({'g_total_discount': self.goodsreport.aggregate(c=Sum('checkd__discount'))['c'],})

			context_data.update({'g_total_count': self.goodsreport.count(),})
			context_data.update({'g_total_col': self.goodsreport.aggregate(c=Sum('col'))['c'],})
			context_data.update({'g_total_sum': self.goodsreport.aggregate(c=Sum('sum'))['c'],})
		
		
		#top 20 goods sold
		#context_data.update({'topgoodssold': self.data.aggregate(c=Avg('bonusadd'))['c'],})
		
		#подсчет количества покупателей
		context_data.update({'buyertotal': self.data.aggregate(c=Count('buyer', distinct=True))['c'],})
		
		
		return context_data
		
'''
		

#################ОТЧЕТ ПРОДАЖ ПО ПОЗИЦИЯМ ТОВАРОВ
class Form_filter_report_sale_goods(forms.Form):
	goods = forms.ModelMultipleChoiceField(label=u'Товар', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), queryset=goods.objects.all(), required=False)
	
	ncheck = forms.CharField(label='Номер чека', help_text='номер чека по 1c например 5046', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'off'}), max_length=100, required=False)
	barcode = forms.CharField(label='Штрих код', help_text='Работа со сканером шрих кода', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'off'}), max_length=100, required=False)
	
	#time
	timestart = forms.DateField(label="Время от", help_text='Время чека от', input_formats=['%d-%m-%y', '%d/%m/%y', '%d.%m.%y', '%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y',], required=False, widget=forms.TextInput(attrs={'class':'mydatepicker1'}), initial=datetime.date.today())
	timeend = forms.DateField(label="Время до", help_text='Время чека до', input_formats=['%d-%m-%y', '%d/%m/%y', '%d.%m.%y', '%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y',], required=False, widget=forms.TextInput(attrs={'class':'mydatepicker1'}))
	timedm = forms.BooleanField(label="Игнорировать год", required=False, initial=False,)
	#

	tax = forms.ModelMultipleChoiceField(label='Категория', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), queryset=tax.objects.all(), required=False)
	
	discount = forms.ModelMultipleChoiceField(label='Скидки', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), queryset=discounts.objects.all(), required=False)
	
	shop = forms.ModelMultipleChoiceField(label='Магазины', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '5',}), queryset=shop.objects.all(), required=False)
	
	cashbox = forms.ModelMultipleChoiceField(label='Касса', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '5',}), queryset=cashbox.objects.all(), required=False)
	
	stock = forms.ModelMultipleChoiceField(label='Склад', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '5',}), queryset=stock.objects.filter(status=True), required=False)
	
	pricefrom = forms.FloatField(label="Цена товара от", required=False,)
	priceto = forms.FloatField(label="Цена товара до", required=False,)
	
	beznal = forms.BooleanField(label='Без наличный расчет', initial=True, required=False)
	checksumfrom = forms.FloatField(label="Сумма чека от", required=False,)
	checksumto = forms.FloatField(label="Сумма чека до", required=False,)
	
	paging = forms.BooleanField(label='На одной странице', required=False)
	instock = forms.BooleanField(label='В наличии', required=False)
	inbuyer = forms.BooleanField(label='Покупатель определен', required=False)
	
	base = forms.ModelMultipleChoiceField(label='База 1с', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '3',}), queryset=base1c.objects.all(), required=False, initial=2)
	
	
	sortchoice=(
		('nckkm', 'Номер чека'),
		('time', 'Время (старые)'),
		('-time', 'Время (новые)'),
		('nal', 'Оплата наличные (меньше)'),
		('-nal', 'Оплата наличные (Больше)'),
		('beznal', 'Оплата без наличные (меньше)'),
		('-beznal', 'Оплата без наличные (Больше)'),
		('bonuspay', 'Оплата бонусы (меньше)'),
		('-bonuspay', 'Оплата бонусы (Больше)'),
		('bonusadd', 'Начисление бонусов (меньше)'),
		('-bonusadd', 'Начисление бонусов (Больше)'),
		)
	
	sort = forms.ChoiceField(label='Сортировка', help_text='Сортировать по полю', widget=forms.Select(attrs={'class': 'form-control'}), choices=sortchoice, required=False)
	
	operation = forms.ChoiceField(label='Вид операции', help_text='Вид операции', widget=forms.Select(attrs={'class': 'form-control'}), choices=operationchoice, required=False)

#@method_decorator(permission_required('node.add_check'), name='dispatch')		
class report_sale_goods(ListView):
	template_name = "report_sale_goods.html"
	model = check
	#paginate_by = 20
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'report', 'R')
		if "timestart" not in request.GET:
			startdate = datetime.datetime.now() + datetime.timedelta(days=-60)
			enddate = datetime.datetime.now() + datetime.timedelta(days=60)
			return HttpResponseRedirect('/report/salegoods/1/?timestart=%s&timeend=%s' % (startdate.strftime('%d-%m-%Y'), enddate.strftime('%d-%m-%Y')))
		return super(report_sale_goods, self).dispatch(request, *args, **kwargs)
	
	def get_queryset(self):
		data=super(report_sale_goods, self).get_queryset()
		
		data=data.all() #выбираем основной запрос
		
		f=Form_filter_report_sale_goods(self.request.GET)
		
		
		req = ''
		paging = 40
		
		if f.is_valid():
			fdata = f.cleaned_data
			#фильтрация
			if fdata['goods']:
				req = '%s&goods=%s' % (req, self.request.GET['goods'])
				data=data.filter(checkitem__goods__in=fdata['goods']).distinct()
				
			if fdata['ncheck']:
				req = '%s&ncheck=%s' % (req, self.request.GET['ncheck'])
				data=data.filter(nckkm=fdata['ncheck'])
	
			if fdata['barcode']:
				req = '%s&barcode=%s' % (req, fdata['barcode'])
				data=data.filter(checkitem__goods__barcode=fdata['barcode'])
	
			if fdata['timestart'] and fdata['timeend']:
				req = '%s&timestart=%s' % (req, self.request.GET['timestart'])
				req = '%s&timeend=%s' % (req, self.request.GET['timeend'])
				if fdata['timedm'] == True: #фильтр только день месяц, игнорировать год
					req = '%s&timedm=%s' % (req, self.request.GET['timedm'])
					s = fdata['timestart']
					e = fdata['timeend']
					count = (e-s).days
					count=count+1
					dlist = []
					for x in range(0, count):
						dlist.append(s + datetime.timedelta(days=x))
					dindex = []
					for date in dlist:
						dindex.append(date.strftime("%d%m")) 
					data=data.filter(timeindex__in=dindex)	 
				else: #полный фильтр день месяц год
					data=data.filter(time__range=(fdata['timestart'], fdata['timeend']))	

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
				data=data.filter(checkitem__goods__tax__in=taxin)
			
			if fdata['discount']:
				req = '%s&discount=%s' % (req, self.request.GET['discount'])
				data=data.filter(checkitem__checkd__discounts__in=fdata['discount']).distinct()

			if fdata['shop']:
				req = '%s&shop=%s' % (req, self.request.GET['shop'])
				data=data.filter(shop__in=fdata['shop'])
			
			if fdata['cashbox']:
				req = '%s&cashbox=%s' % (req, self.request.GET['cashbox'])
				data=data.filter(cashbox__in=fdata['cashbox'])
			
			if fdata['stock']:
				req = '%s&stock=%s' % (req, self.request.GET['stock'])
				data=data.filter(checkitem__goods__qinstock__value__gte=1, checkitem__goods__qinstock__stock__in=fdata['stock']).distinct()

			if fdata['pricefrom']: #цена gte больше или равно
				req = '%s&pricefrom=%s' % (req, fdata['pricefrom'])
				data=data.filter(checkitem__goods__price__gte=fdata['pricefrom'])
			if fdata['priceto']: #цена lte маньше или равно
				req = '%s&priceto=%s' % (req, fdata['priceto'])
				data=data.filter(checkitem__goods__price__lte=fdata['priceto'])
				
			#nal
			if fdata['beznal']:
				req = '%s&beznal=%s' % (req, fdata['beznal'])
				if fdata['checksumfrom'] and fdata['checksumto']:
					if fdata['checksumfrom']: #цена gte больше или равно
						req = '%s&checksumfrom=%s' % (req, fdata['checksumfrom'])
						data=data.filter(beznal__gte=fdata['checksumfrom'])
					if fdata['checksumto']: #цена lte маньше или равно
						req = '%s&checksumto=%s' % (req, fdata['checksumto'])
						data=data.filter(beznal__lte=fdata['checksumto'])
				else:
					data=data.filter(beznal__gte=1)
			else:
				if fdata['checksumfrom']: #цена gte больше или равно
					req = '%s&checksumfrom=%s' % (req, fdata['checksumfrom'])
					data=data.filter(nal__gte=fdata['checksumfrom'])
				if fdata['checksumto']: #цена lte маньше или равно
					req = '%s&checksumto=%s' % (req, fdata['checksumto'])
					data=data.filter(nal__lte=fdata['checksumto'])

			if fdata['paging']:
				req = '%s&paging=%s' % (req, self.request.GET['paging'])
				paging = 1000
			
			if fdata['instock']: #в наличии, количество больше 1
				req = '%s&instock=%s' % (req, self.request.GET['instock'])
				data=data.filter(checkitem__goods__qinstock__value__gte=1).distinct() #направильное считал, сейчас это лишнее
				
			if fdata['inbuyer']: #покупатель присутствует
				req = '%s&inbuyer=%s' % (req, self.request.GET['inbuyer'])
				data=data.filter(buyer__isnull=False)

			if fdata['sort']:
				req = '%s&sort=%s' % (req, self.request.GET['sort'])
				data=data.order_by(fdata['sort'])
				
			if fdata['operation']:
				req = '%s&operation=%s' % (req, self.request.GET['operation'])
				self.checkreturn=data.filter(operation='return')
				data=data.filter(operation=fdata['operation'])
			else:
				self.checkreturn=data.filter(operation='return')
				data=data.filter(operation='sale')
				
			if fdata['base']:
				req = '%s&base=%s' % (req, self.request.GET['base'])
				data=data.filter(checkitem__goods__base=fdata['base'])

				
			#ОТЧЕТ ПО ЧЕКАМ
			self.checkreport=checkitem.objects.filter(fcheck__in=data)	
			#ОТЧЕТ ПО ТОВАРАМ
			self.goodsreportview=False
			if fdata['goods']:
				self.goodsreport=checkitem.objects.filter(goods__id=fdata['goods'], fcheck__in=data)
			
			#ОТЧЕТ ПО СКИДКАМ
			self.discountreport=None
			if fdata['discount']:
				self.discountreport=fdata['discount'].filter(checkd__checkitem__fcheck__in=data).annotate(sum_discount=Sum('checkd__discount'))
		
			
			
			datareport = goods.objects.filter(checkitem__fcheck__in=data)
			
			#ТОП ПРОДАВАЕМЫХ ТОВАРОВ
			if fdata['tax']:
				datareport = datareport.filter(checkitem__goods__tax__in=taxin)
				
			if fdata['base']:
				datareport=datareport.filter(checkitem__goods__base=fdata['base'])
				
			datareport = datareport.annotate(c=Count('checkitem__col'), s=Sum('checkitem__sum'))
			
			self.topgoodssold=datareport.order_by('-s')[:30]
		
		
		
		self.req = req
		self.data = data

		################# исключение категории для отладки
		#t = tax.objects.get(id=18)
		#data=data.exclude(tax=t)
		#self.sum=data.exclude(tax=t).aggregate(s=Sum('qinstock__value'))
		#######################
		
		
		#paginator
		self.p = Paginator(datareport, paging)
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
		context_data = super(report_sale_goods, self).get_context_data(*args, **kwargs)
		context_data.update({'form': Form_filter_report_sale_goods(self.request.GET),})
		context_data.update({'req': self.req,})
		context_data.update({'checkcount': self.p.count,})
		
		context_data.update({'checkreturn': self.checkreturn.count() ,})
		
		context_data.update({'discountreport': self.discountreport,})
		
		#ТОП ПРОДАВАЕМЫХ ТОВАРОВ
		context_data.update({'topgoodssold': self.topgoodssold,})
		
		#ОТЧЕТ ПО ЧЕКАМ
		context_data.update({'checkitems': self.checkreport.count(),})
		context_data.update({'checkitemscol': self.checkreport.aggregate(c=Sum('col'))['c'],})
		
		context_data.update({'c_total_nodiscount': self.checkreport.aggregate(c=Sum(F('price')*F('col')))['c'],})
		context_data.update({'c_total_discount': self.checkreport.aggregate(c=Sum('checkd__discount'))['c'],})
		context_data.update({'c_total_sum': self.checkreport.aggregate(c=Sum('sum'))['c'],})
		context_data.update({'c_total_nal': self.data.aggregate(c=Sum('nal'))['c'],})
		context_data.update({'c_total_beznal': self.data.aggregate(c=Sum('beznal'))['c'],})
		context_data.update({'c_total_bonuspay': self.data.aggregate(c=Sum('bonuspay'))['c'],})
		context_data.update({'c_total_bonusadd': self.data.aggregate(c=Sum('bonusadd'))['c'],})

		context_data.update({'c_min_nodiscount': self.checkreport.aggregate(c=Min(F('price')*F('col')))['c'],})
		context_data.update({'c_min_discount': self.checkreport.aggregate(c=Min('checkd__discount'))['c'],})
		context_data.update({'c_min_sum': self.checkreport.aggregate(c=Min('sum'))['c'],})
		context_data.update({'c_min_nal': self.data.aggregate(c=Min('nal'))['c'],})
		context_data.update({'c_min_beznal': self.data.aggregate(c=Min('beznal'))['c'],})
		context_data.update({'c_min_bonuspay': self.data.aggregate(c=Min('bonuspay'))['c'],})
		context_data.update({'c_min_bonusadd': self.data.aggregate(c=Min('bonusadd'))['c'],})
		
		context_data.update({'c_max_nodiscount': self.checkreport.aggregate(c=Max(F('price')*F('col')))['c'],})
		context_data.update({'c_max_discount': self.checkreport.aggregate(c=Max('checkd__discount'))['c'],})
		context_data.update({'c_max_sum': self.checkreport.aggregate(c=Max('sum'))['c'],})
		context_data.update({'c_max_nal': self.data.aggregate(c=Max('nal'))['c'],})
		context_data.update({'c_max_beznal': self.data.aggregate(c=Max('beznal'))['c'],})
		context_data.update({'c_max_bonuspay': self.data.aggregate(c=Max('bonuspay'))['c'],})
		context_data.update({'c_max_bonusadd': self.data.aggregate(c=Max('bonusadd'))['c'],})
		
		context_data.update({'c_avg_nodiscount': self.checkreport.aggregate(c=Avg(F('price')*F('col')))['c'],})
		context_data.update({'c_avg_discount': self.checkreport.aggregate(c=Avg('checkd__discount'))['c'],})
		context_data.update({'c_avg_sum': self.checkreport.aggregate(c=Avg('sum'))['c'],})
		context_data.update({'c_avg_nal': self.data.aggregate(c=Avg('nal'))['c'],})
		context_data.update({'c_avg_beznal': self.data.aggregate(c=Avg('beznal'))['c'],})
		context_data.update({'c_avg_bonuspay': self.data.aggregate(c=Avg('bonuspay'))['c'],})
		context_data.update({'c_avg_bonusadd': self.data.aggregate(c=Avg('bonusadd'))['c'],})
		
		#подсчет отфильтрованного товара
		
		if self.goodsreportview:
			context_data.update({'goodsreportview': self.goodsreportview,})
			context_data.update({'g_total_nodiscount': self.goodsreport.aggregate(c=Sum(F('price')*F('col')))['c'],})
			context_data.update({'g_total_discount': self.goodsreport.aggregate(c=Sum('checkd__discount'))['c'],})

			context_data.update({'g_total_count': self.goodsreport.count(),})
			context_data.update({'g_total_col': self.goodsreport.aggregate(c=Sum('col'))['c'],})
			context_data.update({'g_total_sum': self.goodsreport.aggregate(c=Sum('sum'))['c'],})
		
		
		#top 20 goods sold
		#context_data.update({'topgoodssold': self.data.aggregate(c=Avg('bonusadd'))['c'],})
		
		return context_data
		
		

###################################################













		
		
		
#отчет счетчик посетителей
class Form_filter_visitor(forms.Form):
	#time
	timestart = forms.DateTimeField(label="Время от", help_text='Время от %d-%m-%y %H:%M', input_formats=['%d-%m-%y %H:%M', '%d-%m-%Y %H:%M',], required=False, widget=forms.TextInput(attrs={'class':'1mydatepicker1'}), initial=datetime.date.today())
	timeend = forms.DateTimeField(label="Время до", help_text='Время до %d-%m-%y %H:%M', input_formats=['%d-%m-%y %H:%M', '%d-%m-%Y %H:%M',], required=False, widget=forms.TextInput(attrs={'class':'1mydatepicker1'}))
	#

	shop = forms.ModelMultipleChoiceField(label='Магазины', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '5',}), queryset=shop.objects.all(), required=False)
	
	eventchoice=(('all', 'Все'), ('entry', 'Вход'),('exit', 'Выход'),)
	event = forms.ChoiceField(label='Событие', help_text='Событие', widget=forms.Select(attrs={'class': 'form-control'}), choices=eventchoice, initial='all', required=False)
	
#@method_decorator(permission_required('device.add_countvisitor'), name='dispatch')
class report_visitor(ListView):
	template_name = "report_visitor.html"
	model = countvisitor
	#paginate_by = 20
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'report', 'R')
		if "timestart" not in request.GET:
			startdate = datetime.datetime.now() + datetime.timedelta(days=-60)
			enddate = datetime.datetime.now() + datetime.timedelta(days=60)
			return HttpResponseRedirect('/report/visitor/1/?timestart=%s&timeend=%s' % (startdate.strftime('%d-%m-%Y %H:%M'), enddate.strftime('%d-%m-%Y %H:%M')))
		return super(report_visitor, self).dispatch(request, *args, **kwargs)
	
	def get_queryset(self):
		data=super(report_visitor, self).get_queryset()
		
		data=data.all() #выбираем основной запрос
		
		f=Form_filter_visitor(self.request.GET)
		
		
		req = ''
		paging = 40
		
		if f.is_valid():
			fdata = f.cleaned_data
			#фильтрация
			if fdata['timestart'] and fdata['timeend']:
				req = '%s&timestart=%s' % (req, self.request.GET['timestart'])
				req = '%s&timeend=%s' % (req, self.request.GET['timeend']) 
				#data=data.filter(ctime__range=(fdata['timestart'], fdata['timeend']))
				data=data.filter(counttime__gte=fdata['timestart'], counttime__lte=fdata['timeend'])

			if fdata['shop']:
				req = '%s&shop=%s' % (req, self.request.GET['shop'])
				data=data.filter(shop__in=fdata['shop'])
				
			if fdata['event'] and fdata['event'] != 'all':
				req = '%s&event=%s' % (req, self.request.GET['event'])
				data=data.filter(event=fdata['event'])
		
		self.req = req
		self.data = data
		
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
		context_data = super(report_visitor, self).get_context_data(*args, **kwargs)
		context_data.update({'form': Form_filter_visitor(self.request.GET),})
		context_data.update({'req': self.req,})
		context_data.update({'total': self.p.count,})
		
		return context_data
	
		

		
		
		
		
#отчет счетчик посетителей
class Form_filter_visitor_period(forms.Form):
	#time
	timestart = forms.DateTimeField(label="Время от", help_text='Время от %d-%m-%y %H:%M', input_formats=['%d-%m-%y', '%d-%m-%Y', '%d-%m-%y %H:%M', '%d-%m-%Y %H:%M', '%d/%m/%y', '%d/%m/%Y', '%d/%m/%y %H:%M', '%d/%m/%Y %H:%M'], required=False, widget=forms.TextInput(attrs={'class':'1mydatepicker1'}), initial=datetime.date.today())
	timeend = forms.DateTimeField(label="Время до", help_text='Время до %d-%m-%y %H:%M', input_formats=['%d-%m-%y', '%d-%m-%Y', '%d-%m-%y %H:%M', '%d-%m-%Y %H:%M', '%d/%m/%y', '%d/%m/%Y', '%d/%m/%y %H:%M', '%d/%m/%Y %H:%M'], required=False, widget=forms.TextInput(attrs={'class':'1mydatepicker1'}))
	#

	shop = forms.ModelMultipleChoiceField(label='Магазины', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '5',}), queryset=shop.objects.all(), required=False)
	
	periodchoice=(
		('y', 'Год'),
		('m', 'Месяц'),
		('w', 'Неделя'),
		('d', 'День'),
		)
	
	period = forms.ChoiceField(label='Период', help_text='Период', widget=forms.Select(attrs={'class': 'form-control'}), choices=periodchoice, required=False)


#@method_decorator(permission_required('device.add_countvisitor'), name='dispatch')
class report_visitor_period(ListView):
	template_name = "report_visitor_period.html"
	model = countvisitor
	#paginate_by = 20
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'report', 'R')
		#if "timestart" not in request.GET:
			#startdate = datetime.datetime.now() + datetime.timedelta(days=-60)
			#enddate = datetime.datetime.now() + datetime.timedelta(days=60)
			#return HttpResponseRedirect('/report/visitorperiod/1/?timestart=%s&timeend=%s' % (startdate.strftime('%d-%m-%Y %H:%M'), enddate.strftime('%d-%m-%Y %H:%M')))
		return super(report_visitor_period, self).dispatch(request, *args, **kwargs)
	
	def get_queryset(self):
		data=super(report_visitor_period, self).get_queryset()
		
		data=data.all() #выбираем основной запрос
		
		f=Form_filter_visitor_period(self.request.GET)
		
		
		req = ''
		paging = 40
		
		if f.is_valid():
			fdata = f.cleaned_data
			#фильтрация
			if fdata['timestart'] and fdata['timeend']:
				req = '%s&timestart=%s' % (req, self.request.GET['timestart'])
				req = '%s&timeend=%s' % (req, self.request.GET['timeend']) 
				#data=data.filter(ctime__range=(fdata['timestart'], fdata['timeend']))
				data=data.filter(counttime__gte=fdata['timestart'], counttime__lte=fdata['timeend'])

			if fdata['shop']:
				req = '%s&shop=%s' % (req, self.request.GET['shop'])
				data=data.filter(shop__in=fdata['shop'])
				
			'''	
			countvisitor.objects.filter(Q(shop__id=6), Q(event='entry') | Q(event='exit')).annotate(year=ExtractYear('counttime'), month=ExtractMonth('counttime')).values('year', 'month', 'shop').annotate(entry=Count(Case(When(event='entry', then=F('event')), output_field=IntegerField())), exit=Count(Case(When(event='exit', then=F('event')), output_field=IntegerField()))).order_by('-month').distinct()	
			'''	
			
			period='y'
			if fdata['period']:
				req = '%s&period=%s' % (req, self.request.GET['period'])
				period=fdata['period']

			if period == 'y':
				data=data.filter(Q(shop__id=6), Q(event='entry') | Q(event='exit')).annotate(year=ExtractYear('counttime')).values('year', 'shop').annotate(entry=Count(Case(When(event='entry', then=F('event')), output_field=IntegerField())), exit=Count(Case(When(event='exit', then=F('event')), output_field=IntegerField()))).order_by('-year').distinct()
			if period == 'm':
				data=data.filter(Q(shop__id=6), Q(event='entry') | Q(event='exit')).annotate(year=ExtractYear('counttime'), month=ExtractMonth('counttime')).values('year', 'month', 'shop').annotate(entry=Count(Case(When(event='entry', then=F('event')), output_field=IntegerField())), exit=Count(Case(When(event='exit', then=F('event')), output_field=IntegerField()))).order_by('-month').distinct()
			if period == 'w':
				data=data.filter(Q(shop__id=6), Q(event='entry') | Q(event='exit')).annotate(year=ExtractYear('counttime'), month=ExtractMonth('counttime'), week=ExtractWeek('counttime')).values('year', 'month', 'week', 'shop').annotate(entry=Count(Case(When(event='entry', then=F('event')), output_field=IntegerField())), exit=Count(Case(When(event='exit', then=F('event')), output_field=IntegerField()))).order_by('-week').distinct()
			if period == 'd':
				data=data.filter(Q(shop__id=6), Q(event='entry') | Q(event='exit')).annotate(year=ExtractYear('counttime'), month=ExtractMonth('counttime'), week=ExtractWeek('counttime'), day=ExtractDay('counttime')).values('year', 'month', 'week', 'day', 'shop').annotate(entry=Count(Case(When(event='entry', then=F('event')), output_field=IntegerField())), exit=Count(Case(When(event='exit', then=F('event')), output_field=IntegerField()))).order_by('-year', '-week', '-month', '-day').distinct()	

		
		self.req = req
		self.data = data
		
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
		context_data = super(report_visitor_period, self).get_context_data(*args, **kwargs)
		context_data.update({'form': Form_filter_visitor_period(self.request.GET),})
		context_data.update({'req': self.req,})
		context_data.update({'total': self.p.count,})
		
		return context_data		
		
		
		
		
		
		

#ОТЧЕТ НЕДЕЛИ МЕСЯЦЫ
class Form_filter_sumperiod(forms.Form):
	#time
	timestart = forms.DateField(label="Время от", help_text='Время чека от', input_formats=['%d-%m-%y', '%d/%m/%y', '%d.%m.%y', '%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y',], required=False, widget=forms.TextInput(attrs={'class':'mydatepicker1'}), initial=datetime.date.today())
	timeend = forms.DateField(label="Время до", help_text='Время чека до', input_formats=['%d-%m-%y', '%d/%m/%y', '%d.%m.%y', '%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y',], required=False, widget=forms.TextInput(attrs={'class':'mydatepicker1'}))
	timedm = forms.BooleanField(label="Игнорировать год", required=False, initial=False,)
	#

	shop = forms.ModelMultipleChoiceField(label='Магазины', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '5',}), queryset=shop.objects.all(), required=False)
	
	cashbox = forms.ModelMultipleChoiceField(label='Касса', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '5',}), queryset=cashbox.objects.all(), required=False)
	
	paging = forms.BooleanField(label='На одной странице', required=False)
	
	sortchoice=(
		('shop', 'Магазин'),
		('-s', 'Сумма (больше)'),
		('s', 'Сумма (меньше)'),
		('-date', 'Дата (больше)'),
		('date', 'Дата (меньше)'),
		)
	
	sort = forms.ChoiceField(label='Сортировка', help_text='Сортировать по полю', widget=forms.Select(attrs={'class': 'form-control'}), choices=sortchoice, required=False)
	
	
	periodchoice=(
		('y', 'Год'),
		('m', 'Месяц'),
		('w', 'Неделя'),
		)
	
	period = forms.ChoiceField(label='Период', help_text='Период', widget=forms.Select(attrs={'class': 'form-control'}), choices=periodchoice, required=False)

#@method_decorator(permission_required('node.add_check'), name='dispatch')		
class report_sumperiod(ListView):
	template_name = "report_sumperiod.html"
	model = check
	#paginate_by = 20
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'report', 'R')
		#if "timestart" not in request.GET:
		#	startdate = datetime.datetime.now() + datetime.timedelta(days=-60)
		#	enddate = datetime.datetime.now() + datetime.timedelta(days=60)
		#	return HttpResponseRedirect('/report/sale/1/?timestart=%s&timeend=%s' % (startdate.strftime('%d-%m-%Y'), enddate.strftime('%d-%m-%Y')))
		return super(report_sumperiod, self).dispatch(request, *args, **kwargs)
	
	def get_queryset(self):
		data=super(report_sumperiod, self).get_queryset()
		
		data=data.all() #выбираем основной запрос
		
		f=Form_filter_sumperiod(self.request.GET)
		
		
		req = ''
		paging = 40
		
		if f.is_valid():
			fdata = f.cleaned_data
			#фильтрация
			if fdata['timestart'] and fdata['timeend']:
				req = '%s&timestart=%s' % (req, self.request.GET['timestart'])
				req = '%s&timeend=%s' % (req, self.request.GET['timeend'])
				if fdata['timedm'] == True: #фильтр только день месяц, игнорировать год
					req = '%s&timedm=%s' % (req, self.request.GET['timedm'])
					s = fdata['timestart']
					e = fdata['timeend']
					count = (e-s).days
					count=count+1
					dlist = []
					for x in range(0, count):
						dlist.append(s + datetime.timedelta(days=x))
					dindex = []
					for date in dlist:
						dindex.append(date.strftime("%d%m")) 
					data=data.filter(timeindex__in=dindex)	 
				else: #полный фильтр день месяц год
					data=data.filter(time__range=(fdata['timestart'], fdata['timeend']))	

			if fdata['shop']:
				req = '%s&shop=%s' % (req, self.request.GET['shop'])
				data=data.filter(shop__in=fdata['shop'])
			
			if fdata['cashbox']:
				req = '%s&cashbox=%s' % (req, self.request.GET['cashbox'])
				data=data.filter(cashbox__in=fdata['cashbox'])

			if fdata['paging']:
				req = '%s&paging=%s' % (req, self.request.GET['paging'])
				paging = 1000
				
			sort='shop'
			if fdata['sort']:
				req = '%s&sort=%s' % (req, self.request.GET['sort'])
				sort=fdata['sort']

			period='y'
			if fdata['period']:
				req = '%s&period=%s' % (req, self.request.GET['period'])
				period=fdata['period']
	
				
		self.req = req
		self.data = data.filter().distinct()
		self.period = period
		
		#data=self.data.annotate(month=TruncMonth('time')).values('month', 'shop').annotate(s=Sum(F('nal')+F('beznal')))

		#фильтр, тип продажа
		
		self.data=self.data.filter(operation='sale')
		
		if period == 'w':
			self.data=self.data.annotate(year=ExtractYear('time'), month=ExtractMonth('time'), week=ExtractWeek('time')).values('year', 'month', 'week', 'shop').annotate(s=Sum('checkitem__sum')).order_by(sort)
			if sort == 'date':
				self.data=self.data.order_by('year', 'month', 'week')
			if sort == '-date':
				self.data=self.data.order_by('-year', '-month', '-week')
		if period == 'm':
			self.data=self.data.annotate(year=ExtractYear('time'), month=ExtractMonth('time')).values('year', 'month', 'shop').annotate(s=Sum('checkitem__sum')).order_by(sort)
			if sort == 'date':
				self.data=self.data.order_by('year', 'month')
			if sort == '-date':
				self.data=self.data.order_by('-year', '-month')
		if period == 'y':
			self.data=self.data.annotate(year=ExtractYear('time'), month=ExtractMonth('time')).values('year', 'shop').annotate(s=Sum('checkitem__sum')).order_by(sort)
			if sort == 'date':
				self.data=self.data.order_by('year')
			if sort == '-date':
				self.data=self.data.order_by('-year')

		#paginator
		self.p = Paginator(self.data, paging)
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
		context_data = super(report_sumperiod, self).get_context_data(*args, **kwargs)
		context_data.update({'form': Form_filter_sumperiod(self.request.GET),})
		context_data.update({'req': self.req,})
		context_data.update({'count': self.data.count(),})
		context_data.update({'period': self.period,})
		return context_data
		
	
	
	
	
	
	
	
#ABC АНАЛИЗ

class Form_filter_abcgoods(forms.Form):
	goods = forms.ModelMultipleChoiceField(label=u'Товар', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), queryset=goods.objects.all(), required=False)
	
	ncheck = forms.CharField(label='Номер чека', help_text='номер чека по 1c например 5046', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'off'}), max_length=100, required=False)
	barcode = forms.CharField(label='Штрих код', help_text='Работа со сканером шрих кода', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'off'}), max_length=100, required=False)
	
	#time
	timestart = forms.DateField(label="Время от", help_text='Время чека от', input_formats=['%d-%m-%y', '%d/%m/%y', '%d.%m.%y', '%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y',], required=False, widget=forms.TextInput(attrs={'class':'mydatepicker1'}), initial=datetime.date.today())
	timeend = forms.DateField(label="Время до", help_text='Время чека до', input_formats=['%d-%m-%y', '%d/%m/%y', '%d.%m.%y', '%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y',], required=False, widget=forms.TextInput(attrs={'class':'mydatepicker1'}))
	timedm = forms.BooleanField(label="Игнорировать год", required=False, initial=False,)
	#

	tax = forms.ModelMultipleChoiceField(label='Категория', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), queryset=tax.objects.all(), required=False)
	
	discount = forms.ModelMultipleChoiceField(label='Скидки', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), queryset=discounts.objects.all(), required=False)
	
	shop = forms.ModelMultipleChoiceField(label='Магазины', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '5',}), queryset=shop.objects.all(), required=False)
	
	cashbox = forms.ModelMultipleChoiceField(label='Касса', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '5',}), queryset=cashbox.objects.all(), required=False)
	
	stock = forms.ModelMultipleChoiceField(label='Склад', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '5',}), queryset=stock.objects.filter(status=True), required=False)
	
	pricefrom = forms.FloatField(label="Цена товара от", required=False,)
	priceto = forms.FloatField(label="Цена товара до", required=False,)
	
	paging = forms.BooleanField(label='На одной странице', required=False)
	instock = forms.BooleanField(label='В наличии', required=False)
	inbuyer = forms.BooleanField(label='Покупатель определен', required=False)

	operation = forms.ChoiceField(label='Вид операции', help_text='Вид операции', widget=forms.Select(attrs={'class': 'form-control'}), choices=operationchoice, required=False)
	
	sortchoice=(
		('-profit', 'Сумма проданных (больше)'),
		('profit', 'Сумма проданных (меньше)'),
		('-col', 'Количество проданных (больше)'),
		('col', 'Количество проданных (меньше)'),
		)
	
	sort = forms.ChoiceField(label='Сортировка', help_text='Сортировать по полю', widget=forms.Select(attrs={'class': 'form-control'}), choices=sortchoice, required=False)
		
	base = forms.ModelMultipleChoiceField(label='База 1с', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '3',}), queryset=base1c.objects.all(), required=False, initial=2)
	
	pdown = forms.IntegerField(label='Процент розничная цена', help_text='Процент закупочной цены от розничной', min_value=1, max_value=99, required=False, initial=0)
	


#@method_decorator(permission_required('node.add_check'), name='dispatch')		
class report_abcgoods(ListView):
	template_name = "report_abcgoods1.html"
	model = check
	#paginate_by = 20
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'report', 'R')
		if "timestart" not in request.GET:
			startdate = datetime.datetime.now() + datetime.timedelta(days=-60)
			enddate = datetime.datetime.now() + datetime.timedelta(days=60)
			return HttpResponseRedirect('/report/abcgoods/1/?timestart=%s&timeend=%s' % (startdate.strftime('%d-%m-%Y'), enddate.strftime('%d-%m-%Y')))
		return super(report_abcgoods, self).dispatch(request, *args, **kwargs)
	
	def get_queryset(self):
		data=super(report_abcgoods, self).get_queryset()
		
		data=data.all() #выбираем основной запрос
		
		f=Form_filter_abcgoods(self.request.GET)
		
		
		req = ''
		paging = 40
		
		if f.is_valid():
			fdata = f.cleaned_data
			#фильтрация
			if fdata['goods']:
				req = '%s&goods=%s' % (req, self.request.GET['goods'])
				data=data.filter(checkitem__goods__in=fdata['goods']).distinct()
				
			if fdata['ncheck']:
				req = '%s&ncheck=%s' % (req, self.request.GET['ncheck'])
				data=data.filter(nckkm=fdata['ncheck'])
	
			if fdata['barcode']:
				req = '%s&barcode=%s' % (req, fdata['barcode'])
				data=data.filter(checkitem__goods__barcode=fdata['barcode'])
	
			if fdata['timestart'] and fdata['timeend']:
				req = '%s&timestart=%s' % (req, self.request.GET['timestart'])
				req = '%s&timeend=%s' % (req, self.request.GET['timeend'])
				if fdata['timedm'] == True: #фильтр только день месяц, игнорировать год
					req = '%s&timedm=%s' % (req, self.request.GET['timedm'])
					s = fdata['timestart']
					e = fdata['timeend']
					count = (e-s).days
					count=count+1
					dlist = []
					for x in range(0, count):
						dlist.append(s + datetime.timedelta(days=x))
					dindex = []
					for date in dlist:
						dindex.append(date.strftime("%d%m")) 
					data=data.filter(timeindex__in=dindex)	 
				else: #полный фильтр день месяц год
					data=data.filter(time__range=(fdata['timestart'], fdata['timeend']))	

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
				data=data.filter(checkitem__goods__tax__in=taxin).distinct()
			
			if fdata['discount']:
				req = '%s&discount=%s' % (req, self.request.GET['discount'])
				data=data.filter(checkitem__checkd__discounts__in=fdata['discount']).distinct()

			if fdata['shop']:
				req = '%s&shop=%s' % (req, self.request.GET['shop'])
				data=data.filter(shop__in=fdata['shop'])
			
			if fdata['cashbox']:
				req = '%s&cashbox=%s' % (req, self.request.GET['cashbox'])
				data=data.filter(cashbox__in=fdata['cashbox'])
			
			if fdata['stock']:
				req = '%s&stock=%s' % (req, self.request.GET['stock'])
				data=data.filter(checkitem__goods__qinstock__value__gte=1, checkitem__goods__qinstock__stock__in=fdata['stock']).distinct()

			if fdata['pricefrom']: #цена gte больше или равно
				req = '%s&pricefrom=%s' % (req, fdata['pricefrom'])
				data=data.filter(checkitem__goods__price__gte=fdata['pricefrom'])
			if fdata['priceto']: #цена lte маньше или равно
				req = '%s&priceto=%s' % (req, fdata['priceto'])
				data=data.filter(checkitem__goods__price__lte=fdata['priceto'])
				

			if fdata['paging']:
				req = '%s&paging=%s' % (req, self.request.GET['paging'])
				paging = 1000
			
			if fdata['instock']: #в наличии, количество больше 1
				req = '%s&instock=%s' % (req, self.request.GET['instock'])
				data=data.filter(checkitem__goods__qinstock__value__gte=1).distinct() #направильное считал, сейчас это лишнее
				
			if fdata['inbuyer']: #покупатель присутствует
				req = '%s&inbuyer=%s' % (req, self.request.GET['inbuyer'])
				data=data.filter(buyer__isnull=False)

			if fdata['operation']:
				req = '%s&operation=%s' % (req, self.request.GET['operation'])
				#self.checkreturn=data.filter(operation='return').count()
				data=data.filter(operation=fdata['operation'])
			else:
				#self.checkreturn=data.filter(operation='return').count()
				data=data.filter(operation='sale')
				
			if fdata['tax']:
				data=data.filter(checkitem__goods__tax__in=taxin)

			if fdata['base']:
				req = '%s&base=%s' % (req, self.request.GET['base'])
				data=data.filter(checkitem__goods__base=fdata['base'])
			
			self.checksum = data.aggregate(s=Sum('checkitem__sum'))['s']
			if self.checksum == None:
				self.checksum = 0
			
			
			data = data.filter().distinct()
				

			#ТОП ПРОДАВАЕМЫХ ТОВАРОВ
			self.topgoods=goods.objects.filter(checkitem__fcheck__in=data)
			if fdata['tax']:
				self.topgoods=self.topgoods.filter(tax__in=taxin)

			if fdata['base']:
				self.topgoods=self.topgoods.filter(base=fdata['base'])
				
			pdown = 0
			if fdata['pdown']:
				req = '%s&pdown=%s' % (req, self.request.GET['pdown'])
				pdown = fdata['pdown']
				
			
			if pdown == 0:
				self.topgoods=self.topgoods.annotate(col=Count('checkitem__col'), sum=Sum('checkitem__sum'), profit=Sum('checkitem__sum')).annotate(p=Cast((F('profit')/float(self.checksum))*Value(100), IntegerField())).order_by('-profit')
			else:
				self.topgoods=self.topgoods.annotate(col=Count('checkitem__col'), sum=Sum('checkitem__sum'), startprice=Cast((F('price')/100)*pdown,FloatField()), ).annotate(profit=Cast(((F('sum')-(F('startprice')*F('col')))), FloatField())).annotate(p=Cast((F('profit')/float(self.checksum))*Value(100.0), FloatField())).order_by('-profit')
			
			
			
			if fdata['sort']:
				req = '%s&sort=%s' % (req, self.request.GET['sort'])
				self.topgoods=self.topgoods.order_by(fdata['sort'])
		
		self.req = req
		
		
		#Годовой объем продаж нарастающим итогом рассчитываем как сумму вычисляемого параметра и всех предыдущих.
		ppvalue=0
		for i in self.topgoods:
			ppvalue=ppvalue + i.p
			i.pp = ppvalue
			if i.pp < 80:
				i.abc = 'A'
			if i.pp >= 80 and i.pp < 95:
				i.abc = 'B'
			if i.pp >= 95 and i.pp < 120:
				i.abc = 'C'
				
			#закупочная цена
			#goods.objects.get(base__id=1, id1c='ЦО000000686').a.all().first().b.price
			#try:
			#	startprice = i.a.all().first().b.price
			#except:
			#	i.startprice = float(0)
			#else:
			#	i.startprice=startprice
		
		################# исключение категории для отладки
		#t = tax.objects.get(id=18)
		#data=data.exclude(tax=t)
		#self.sum=data.exclude(tax=t).aggregate(s=Sum('qinstock__value'))
		#######################

		#paginator
		self.p = Paginator(self.topgoods, paging)
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
		context_data = super(report_abcgoods, self).get_context_data(*args, **kwargs)
		context_data.update({'form': Form_filter_abcgoods(self.request.GET),})
		context_data.update({'req': self.req,})
		context_data.update({'checkcount': self.p.count,})
		context_data.update({'count': self.topgoods.count,})
		
		#ТОП ПРОДАВАЕМЫХ ТОВАРОВ
		#context_data.update({'topgoods': self.topgoods,})
		context_data.update({'checksum': self.checksum,})
		

		return context_data
	








class Form_filter_buyertop(forms.Form):
	q = forms.CharField(label='Поиск', help_text='Введите слово для поиска', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'off'}), max_length=100, required=False)

	
	datestart = forms.DateField(label="Дата от", help_text='Дата от', input_formats=['%d-%m-%y', '%d-%m-%Y',], required=False, widget=forms.TextInput(attrs={'class':'form-control datepicker',  'data-dateformat': "dd-mm-yy"}))
	dateend = forms.DateField(label="Дата до", help_text='Дата до', input_formats=['%d-%m-%y', '%d-%m-%Y',], required=False, widget=forms.TextInput(attrs={'class':'form-control datepicker',  'data-dateformat': "dd-mm-yy"}))
	
	sort = forms.ChoiceField(label='Сортировка', help_text='Сортировать по полю', widget=forms.Select(attrs={'class': 'form-control'}), choices=(('id', 'id'),('bday', 'Д. Рождения'),('f', 'Фамилия'),('i', 'Имя'),('o', 'Отчество')), required=False)
	
	sumfrom = forms.FloatField(label="Сумма чеков от", required=False,)
	sumto = forms.FloatField(label="сумма чеков до", required=False,)
	
	#согласие на рассылку
	adv = forms.ChoiceField(label='Согласие на рассылку', widget=forms.Select(attrs={'class': 'form-control'}), choices=(('all', 'Все'),('true', 'Да'),('false', 'Нет'),), initial='all', required=False)
	
	anketa = forms.ChoiceField(label='Анкета', widget=forms.Select(attrs={'class': 'form-control'}), choices=(('all', 'Все'),('true', 'Да'),('false', 'Нет'),), initial='all', required=False)


	
#@method_decorator(permission_required('node.add_buyer'), name='dispatch')
class report_buyertop(ListView):
	template_name = 'report_buyertop.html'
	model = buyer
	#paginate_by = 10
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'report', 'R')
		return super(report_buyertop, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(report_buyertop, self).get_queryset()
		
		#data=data.all() #выбираем основной запрос

		f=Form_filter_buyertop(self.request.GET)
		
		
		
		req = ''
		
		if f.is_valid():
			fdata = f.cleaned_data
			#фильтрация
			if fdata['q']:
				req = '%s&q=%s' % (req, fdata['q'])
				data=data.filter(Q(id__icontains=fdata['q']) | Q(id1c__icontains=fdata['q']) | Q(phone__icontains=fdata['q']) | Q(f__search=fdata['q']) | Q(i__icontains=fdata['q']) | Q(o__icontains=fdata['q']))
			
			if fdata['datestart'] and fdata['dateend']:
				req = '%s&datestart=%s' % (req, self.request.GET['datestart'])
				req = '%s&dateend=%s' % (req, self.request.GET['dateend']) 
				data=data.filter(check__time__gte=fdata['datestart'], check__time__lte=fdata['dateend'])

				
			#	
			data=data.filter(check__process='valid')
			data=data.filter().annotate(s=Sum(F('check__checkitem__sum')))
			if fdata['sumfrom']: #сумма чека от
				req = '%s&sumfrom=%s' % (req, fdata['sumfrom'])
				data=data.filter(s__gte=fdata['sumfrom'])
			if fdata['sumto']: #сумма чека до
				req = '%s&sumto=%s' % (req, fdata['sumto'])
				data=data.filter(s__lte=fdata['sumto'])

			if fdata['sort']:
				req = '%s&sort=%s' % (req, self.request.GET['sort'])
				data=data.order_by(fdata['sort'])
			#	
			
			if fdata['adv']:
				req = '%s&adv=%s' % (req, self.request.GET['adv'])
				if fdata['adv'] == 'true':
					data=data.filter(adv=True)
				if fdata['adv'] == 'false':
					data=data.filter(adv=False)
					
			if fdata['anketa']:
				req = '%s&anketa=%s' % (req, self.request.GET['anketa'])
				if fdata['anketa'] == 'true':
					data=data.filter(anketa__isnull=False)
					data=data.exclude(anketa='')
					#Q(anketa='') | Q(anketa__exact=None)
				if fdata['anketa'] == 'false':
					data=data.filter(anketa__isnull=True)
					#data=data.exclude(~Q(anketa=''))
			
		self.req = req
			
		#data=data.order_by('-id')

		
		#paginator
		self.p = Paginator(data, 20)
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
		context_data = super(report_buyertop, self).get_context_data(*args, **kwargs)
		
		#self.initial.update({'your_field': self.request.user})
		#if "fio" in self.request.GET:
		#	data=data.filter(i__contains=self.request.GET['fio'])
		context_data.update({'req': self.req,})
		context_data.update({'urlpage': '/report/buyertop',})
		context_data.update({'count': self.p.count,})
		context_data.update({'form': Form_filter_buyertop(self.request.GET),})
		return context_data


# class buyer_list(TemplateView):
	# template_name = 'crm/buyer_list.html'
	
	# def dispatch(self, request, *args, **kwargs):
		# return super(buyer_list, self).dispatch(request, *args, **kwargs)
		
	# def get_context_data(self, *args, **kwargs):
		# context_data = super(buyer_list, self).get_context_data(*args, **kwargs)
		# #context_data.update({'command': True,})
		# return context_data




	
	
	
	
	
#################ОТЧЕТ ПРОДАЖ ПО ПОЗИЦИЯМ ТОВАРОВ
class Form_filter_report_sale_topgoods(forms.Form):
	#time
	datestart = forms.DateField(label="Время от", help_text='Дата от', input_formats=['%d-%m-%y', '%d/%m/%y', '%d.%m.%y', '%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y',], required=False, widget=forms.TextInput(attrs={'class':'datepicker'}), initial=datetime.date.today())
	dateend = forms.DateField(label="Время до", help_text='Дата до', input_formats=['%d-%m-%y', '%d/%m/%y', '%d.%m.%y', '%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y',], required=False, widget=forms.TextInput(attrs={'class':'datepicker'}))
	#

	tax = forms.ModelMultipleChoiceField(label='Категория', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), queryset=tax.objects.all(), required=False)
	
	pricefrom = forms.FloatField(label="Цена товара от", required=False,)
	priceto = forms.FloatField(label="Цена товара до", required=False,)
	
	shop = forms.ModelMultipleChoiceField(label='Магазины', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '5',}), queryset=shop.objects.all(), required=False)
	
	discount = forms.ModelMultipleChoiceField(label='Скидки', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), queryset=discounts.objects.all(), required=False)

	instock = forms.BooleanField(label='В наличии', required=False)
	inbuyer = forms.BooleanField(label='Покупатель определен', required=False)
	
	base = forms.ModelMultipleChoiceField(label='База 1с', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '3',}), queryset=base1c.objects.all(), required=False, initial=2)
	
	sortchoice=(
		('-c', 'Количество (больше)'),
		('c', 'Количество (меньше))'),
		('-s', 'Сумма (больше)'),
		('s', 'Сумма (меньше)'),
		)
	
	sort = forms.ChoiceField(label='Сортировка', help_text='Сортировать по полю', widget=forms.Select(attrs={'class': 'form-control'}), choices=sortchoice, required=False)

	pagingchoice=(
		('40', '40'),
		('80', '80'),
		('120', '120'),
		('160', '160'),
		)
	
	paging = forms.ChoiceField(label='Пагинация', help_text='Сколько на странице', widget=forms.Select(attrs={'class': 'form-control'}), choices=pagingchoice, required=False)
	
	
	limitchoice=(
		('100', '100'),
		('500', '500'),
		('400', '400'),
		('300', '300'),
		('200', '200'),
		('all', 'все'),
		)
	
	limit = forms.ChoiceField(label='Лимит', help_text='Лимит элементов (для производительности)', widget=forms.Select(attrs={'class': 'form-control'}), choices=limitchoice, required=False)

	operation = forms.ChoiceField(label='Вид операции', help_text='Вид операции', widget=forms.Select(attrs={'class': 'form-control'}), choices=operationchoice, required=False)

#@method_decorator(permission_required('node.add_check'), name='dispatch')		
class report_sale_topgoods(ListView):
	template_name = "report_sale_topgoods.html"
	model = check
	#paginate_by = 20
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'report', 'R')
		return super(report_sale_topgoods, self).dispatch(request, *args, **kwargs)
	
	def get_queryset(self):
		data=super(report_sale_topgoods, self).get_queryset()
		
		data=data.all() #выбираем основной запрос
		
		f=Form_filter_report_sale_topgoods(self.request.GET)
		
		
		req = ''
		paging = 40
		limit = 100
		
		if f.is_valid():
			fdata = f.cleaned_data
			#фильтрация
			if fdata['datestart'] and fdata['dateend']:
				req = '%s&datestart=%s' % (req, self.request.GET['datestart'])
				req = '%s&dateend=%s' % (req, self.request.GET['dateend'])
				#полный фильтр день месяц год
				data=data.filter(time__range=(fdata['datestart'], fdata['dateend']))	

			if fdata['shop']:
				req = '%s&shop=%s' % (req, self.request.GET['shop'])
				data=data.filter(shop__in=fdata['shop'])

			if fdata['pricefrom']: #цена gte больше или равно
				req = '%s&pricefrom=%s' % (req, fdata['pricefrom'])
				data=data.filter(checkitem__goods__price__gte=fdata['pricefrom'])
			if fdata['priceto']: #цена lte маньше или равно
				req = '%s&priceto=%s' % (req, fdata['priceto'])
				data=data.filter(checkitem__goods__price__lte=fdata['priceto'])
				
			if fdata['operation']:
				req = '%s&operation=%s' % (req, self.request.GET['operation'])
				self.checkreturn=data.filter(operation='return')
				data=data.filter(operation=fdata['operation'])
			else:
				self.checkreturn=data.filter(operation='return')
				data=data.filter(operation='sale')
				
			if fdata['base']:
				req = '%s&base=%s' % (req, self.request.GET['base'])
				data=data.filter(checkitem__goods__base=fdata['base'])

			datareport = goods.objects.filter(checkitem__fcheck__in=data)
			
			#ТОП ПРОДАВАЕМЫХ ТОВАРОВ
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
				datareport = datareport.filter(tax__in=taxin)
				
			if fdata['base']:
				datareport=datareport.filter(base=fdata['base'])
				
			datareport = datareport.annotate(c=Count('checkitem__col'), s=Sum('checkitem__sum'))
			
			datareport=datareport.order_by('-c')
			

			
			if fdata['paging']:
				req = '%s&paging=%s' % (req, self.request.GET['paging'])
				paging = fdata['paging']

			if fdata['sort']:
				datareport=datareport.order_by(fdata['sort'])

			if fdata['limit']:
				req = '%s&limit=%s' % (req, self.request.GET['limit'])
				limit = fdata['limit']
				if fdata['limit'] == 'all':
					limit = 0
	
			if limit != 0:
				datareport=datareport[:limit]
				

		self.req = req

		#paginator
		self.p = Paginator(datareport, paging)
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
		context_data = super(report_sale_topgoods, self).get_context_data(*args, **kwargs)
		context_data.update({'form': Form_filter_report_sale_topgoods(self.request.GET),})
		context_data.update({'req': self.req,})
		context_data.update({'urlpage': '/report/saletopgoods/',})
		context_data.update({'count': self.p.count,})
		return context_data
		


###################################################
	
	
	



class Form_filter_mot(forms.Form):
	#goods = forms.ModelMultipleChoiceField(label=u'Товар', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), queryset=goods.objects.all(), required=False)

	#time
	timestart = forms.DateField(label="Время от", help_text='Время чека от', input_formats=['%d-%m-%y', '%d/%m/%y', '%d.%m.%y', '%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y',], required=False, widget=forms.TextInput(attrs={'class':'form-control datepicker',  'data-dateformat': "dd-mm-yy"}), initial=datetime.date.today())

	timeend = forms.DateField(label="Время до", help_text='Время чека до', input_formats=['%d-%m-%y', '%d/%m/%y', '%d.%m.%y', '%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y',], required=False, widget=forms.TextInput(attrs={'class':'form-control datepicker',  'data-dateformat': "dd-mm-yy"}))
	timedm = forms.BooleanField(label="Игнорировать год", required=False, initial=False,)
	#

	#tax = forms.ModelMultipleChoiceField(label='Категория', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), queryset=tax.objects.all(), required=False)
	
	#shop = forms.ModelMultipleChoiceField(label='Магазины', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '5',}), queryset=shop.objects.all(), required=False)
	
	#pricefrom = forms.FloatField(label="Цена товара от", required=False,)
	#priceto = forms.FloatField(label="Цена товара до", required=False,)
	
	#sortchoice=(
	#	('time', 'Время (старые)'),
	#	('-time', 'Время (новые)'),
	#	)
	
	#sort = forms.ChoiceField(label='Сортировка', help_text='Сортировать по полю', widget=forms.Select(attrs={'class': 'form-control'}), choices=sortchoice, required=False)
	
#@method_decorator(permission_required('node.add_check'), name='dispatch')		
class report_motivation(ListView):
	template_name = "report_motivation.html"
	model = check
	#paginate_by = 20
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'report', 'R')
		#get_object_or_denied(self.request.user, 'check', 'L') #проверяем права
		if "timestart" not in request.GET:
			startdate = datetime.datetime.now() + datetime.timedelta(days=-60)
			enddate = datetime.datetime.now() + datetime.timedelta(days=60)
			return HttpResponseRedirect('/report/motivation/?timestart=%s&timeend=%s' % (startdate.strftime('%d-%m-%Y'), enddate.strftime('%d-%m-%Y')))
		return super(report_motivation, self).dispatch(request, *args, **kwargs)
	
	def get_queryset(self):
		data=super(report_motivation, self).get_queryset()
		
		data=data.all() #выбираем основной запрос
		
		f=Form_filter_mot(self.request.GET)
		
		
		req = ''
		paging = 40
		
		if f.is_valid():
			fdata = f.cleaned_data
			#фильтрация
			# if fdata['goods']:
				# req = '%s&goods=%s' % (req, self.request.GET['goods'])
				# data=data.filter(checkitem__goods__in=fdata['goods']).distinct()
	
			if fdata['timestart'] and fdata['timeend']:
				req = '%s&timestart=%s' % (req, self.request.GET['timestart'])
				req = '%s&timeend=%s' % (req, self.request.GET['timeend'])
				if fdata['timedm'] == True: #фильтр только день месяц, игнорировать год
					req = '%s&timedm=%s' % (req, self.request.GET['timedm'])
					s = fdata['timestart']
					e = fdata['timeend']
					count = (e-s).days
					count=count+1
					dlist = []
					for x in range(0, count):
						dlist.append(s + datetime.timedelta(days=x))
					dindex = []
					for date in dlist:
						dindex.append(date.strftime("%d%m")) 
					data=data.filter(timeindex__in=dindex)	 
				else: #полный фильтр день месяц год
					data=data.filter(time__range=(fdata['timestart'], fdata['timeend']))	

			# if fdata['tax']:
				# req = '%s&tax=%s' % (req, self.request.GET['tax'])
				# print fdata['tax']
				# #########################################
				# ########обработка дочерних категорий#####
				# #########################################
				# datatax=tax.objects.filter(id__in=fdata['tax']).values('id')
				# taxin=datatax
				# #берем дочернии категории, если есть
				# taxparent = tax.objects.filter(parent__in=datatax).values('id')
				# if taxparent.exists():
					# taxin = taxparent
				# #########################################
				# data=data.filter(checkitem__goods__tax__in=taxin).distinct()

			# if fdata['shop']:
				# req = '%s&shop=%s' % (req, self.request.GET['shop'])
				# data=data.filter(shop__in=fdata['shop'])

			# if fdata['pricefrom']: #цена gte больше или равно
				# req = '%s&pricefrom=%s' % (req, fdata['pricefrom'])
				# data=data.filter(checkitem__goods__price__gte=fdata['pricefrom'])
			# if fdata['priceto']: #цена lte маньше или равно
				# req = '%s&priceto=%s' % (req, fdata['priceto'])
				# data=data.filter(checkitem__goods__price__lte=fdata['priceto'])

			# if fdata['sort']:
				# req = '%s&sort=%s' % (req, self.request.GET['sort'])
				# data=data.order_by(fdata['sort'])

		self.req = req
		self.data = data.filter().distinct()

		################# исключение категории для отладки
		#t = tax.objects.get(id=18)
		#data=data.exclude(tax=t)
		#self.sum=data.exclude(tax=t).aggregate(s=Sum('qinstock__value'))
		#######################
		
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
		context_data = super(report_motivation, self).get_context_data(*args, **kwargs)
		context_data.update({'form': Form_filter_mot(self.request.GET),})
		context_data.update({'req': self.req,})
		#context_data.update({'count': self.p.count,})
		return context_data










	
'''	
@method_decorator(permission_required('node.add_check'), name='dispatch')		
class report_abcgoods(ListView):
	template_name = "report_abcgoods.html"
	model = checkitem
	#paginate_by = 20
	
	def dispatch(self, request, *args, **kwargs):
		if "timestart" not in request.GET:
			startdate = datetime.datetime.now() + datetime.timedelta(days=-60)
			enddate = datetime.datetime.now() + datetime.timedelta(days=60)
			return HttpResponseRedirect('/report/abcgoods/1/?timestart=%s&timeend=%s' % (startdate.strftime('%d-%m-%Y'), enddate.strftime('%d-%m-%Y')))
		return super(report_abcgoods, self).dispatch(request, *args, **kwargs)
	
	def get_queryset(self):
		data=super(report_abcgoods, self).get_queryset()
		
		data=data.all() #выбираем основной запрос
		
		f=Form_filter_abcgoods(self.request.GET)
		print f.errors
		fdata = f.cleaned_data
		
		req = ''
		paging = 80
		
		if f.is_valid():
			#фильтрация
			if fdata['goods']:
				req = '%s&goods=%s' % (req, self.request.GET['goods'])
				data=data.filter(goods__in=fdata['goods']).distinct()
				
			if fdata['ncheck']:
				req = '%s&ncheck=%s' % (req, self.request.GET['ncheck'])
				data=data.filter(fcheck__nckkm=fdata['ncheck'])
	
			if fdata['barcode']:
				req = '%s&barcode=%s' % (req, fdata['barcode'])
				data=data.filter(goods__barcode=fdata['barcode'])
	
			if fdata['timestart'] and fdata['timeend']:
				req = '%s&timestart=%s' % (req, self.request.GET['timestart'])
				req = '%s&timeend=%s' % (req, self.request.GET['timeend'])
				if fdata['timedm'] == True: #фильтр только день месяц, игнорировать год
					req = '%s&timedm=%s' % (req, self.request.GET['timedm'])
					s = fdata['timestart']
					e = fdata['timeend']
					count = (e-s).days
					count=count+1
					dlist = []
					for x in range(0, count):
						dlist.append(s + datetime.timedelta(days=x))
					dindex = []
					for date in dlist:
						dindex.append(date.strftime("%d%m")) 
					data=data.filter(fcheck__timeindex__in=dindex)	 
				else: #полный фильтр день месяц год
					data=data.filter(fcheck__time__range=(fdata['timestart'], fdata['timeend']))	

			if fdata['tax']:
				req = '%s&tax=%s' % (req, self.request.GET['tax'])
				print fdata['tax']
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
				data=data.filter(goods__tax__in=taxin).distinct()
			
			if fdata['discount']:
				req = '%s&discount=%s' % (req, self.request.GET['discount'])
				data=data.filter(checkd__discounts__in=fdata['discount']).distinct()

			if fdata['shop']:
				req = '%s&shop=%s' % (req, self.request.GET['shop'])
				data=data.filter(fcheck__shop__in=fdata['shop'])
			
			if fdata['cashbox']:
				req = '%s&cashbox=%s' % (req, self.request.GET['cashbox'])
				data=data.filter(fcheck__cashbox__in=fdata['cashbox'])
			
			if fdata['stock']:
				req = '%s&stock=%s' % (req, self.request.GET['stock'])
				print fdata['stock']
				data=data.filter(goods__qinstock__value__gte=1, goods__qinstock__stock__in=fdata['stock']).distinct()

			if fdata['pricefrom']: #цена gte больше или равно
				req = '%s&pricefrom=%s' % (req, fdata['pricefrom'])
				data=data.filter(goods__price__gte=fdata['pricefrom'])
			if fdata['priceto']: #цена lte маньше или равно
				req = '%s&priceto=%s' % (req, fdata['priceto'])
				data=data.filter(goods__price__lte=fdata['priceto'])
				


			if fdata['paging']:
				req = '%s&paging=%s' % (req, self.request.GET['paging'])
				paging = 1000
			
			if fdata['instock']: #в наличии, количество больше 1
				req = '%s&instock=%s' % (req, self.request.GET['instock'])
				data=data.filter(goods__qinstock__value__gte=1).distinct() #направильное считал, сейчас это лишнее
				
			if fdata['inbuyer']: #покупатель присутствует
				req = '%s&inbuyer=%s' % (req, self.request.GET['inbuyer'])
				data=data.filter(fcheck__buyer__isnull=False)

			if fdata['operation']:
				req = '%s&operation=%s' % (req, self.request.GET['operation'])
				self.checkreturn=data.filter(fcheck__operation='return').count()
				data=data.filter(fcheck__operation=fdata['operation'])
			else:
				self.checkreturn=data.filter(fcheck__operation='return').count()
				data=data.filter(fcheck__operation='sale')
				
			if fdata['tax']:
				data=data.filter(goods__tax__in=taxin)

			
			data = data.distinct()
				

			#ТОП ПРОДАВАЕМЫХ ТОВАРОВ
			#self.topgoods=goods.objects.filter(checkitem__fcheck__in=data)
			#if fdata['tax']:
			#	self.topgoods=self.topgoods.filter(checkitem__goods__tax__in=taxin)

			#data=data.values('goods__id', 'col', 'sum').annotate(c=Count('col'), s=Sum('sum')).order_by('-s')
			data=data.values('goods__id', 'goods__name', 'goods__price', 'col', 'sum').annotate(c=Count('col'), s=Sum('sum')).order_by('-s')
			
			if fdata['sort']:
				req = '%s&sort=%s' % (req, self.request.GET['sort'])
				data=data.order_by(fdata['sort'])
		
		self.req = req
		

		################# исключение категории для отладки
		#t = tax.objects.get(id=18)
		#data=data.exclude(tax=t)
		#self.sum=data.exclude(tax=t).aggregate(s=Sum('qinstock__value'))
		#######################
		
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
		context_data = super(report_abcgoods, self).get_context_data(*args, **kwargs)
		context_data.update({'form': Form_filter_abcgoods(self.request.GET),})
		context_data.update({'req': self.req,})
		context_data.update({'checkcount': self.p.count,})
		
		#ТОП ПРОДАВАЕМЫХ ТОВАРОВ
		#context_data.update({'topgoods': self.topgoods,})

		return context_data	
'''	
	
