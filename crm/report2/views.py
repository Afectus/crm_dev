# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from .models import *
from sms.models import *
from node.models import *

from django.db.models import Min, Max, Sum, Count, Avg
from django.db.models import Q, F, Func, Value, IntegerField, FloatField, CharField, Case, When
from django.db.models.functions import Cast, Trunc, TruncMonth, ExtractYear, ExtractMonth, ExtractWeek, ExtractWeekDay, ExtractDay
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DetailView, ListView, DeleteView

import logging
log = logging.getLogger(__name__)



class Form_filter_smssale(forms.Form):
	datestart = forms.DateField(label="Дата от", help_text='Дата от', input_formats=['%d-%m-%y', '%d-%m-%Y',], required=False, widget=forms.TextInput(attrs={'class':'form-control datepicker',  'data-dateformat': "dd-mm-yy"}))
	dateend = forms.DateField(label="Дата до", help_text='Дата до', input_formats=['%d-%m-%y', '%d-%m-%Y',], required=False, widget=forms.TextInput(attrs={'class':'form-control datepicker',  'data-dateformat': "dd-mm-yy"}))
	idays = forms.IntegerField(label="Интервал дней", required=True, initial=10)
	showbuys = forms.BooleanField(label='Показать только с учетом покупок', initial=True, required=False)
	showallbuys = forms.BooleanField(label='Показать все покупки покупателя', initial=True, required=False)

class report2_smssale(ListView):
	template_name = 'report_smssale.html'
	model = smsqsend
	# paginate_by = 22
	
	def dispatch(self, request, *args, **kwargs):
		return super(report2_smssale, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(report2_smssale, self).get_queryset()
		
		#data=data.all() #выбираем основной запрос
		# data=data.filter().annotate(s=Sum(F('check__checkitem__price')*F('check__checkitem__col'))-Sum('check__checkitem__checkd__discount'))
		
		f=Form_filter_smssale(self.request.GET)
		log.info(f.errors)
		
		
		self.idays = 0
		
		req = ''
		
		# if f.is_valid():
			# fdata = f.cleaned_data
			# #фильтрация
			# if fdata['datestart'] and fdata['dateend']:
				# req = '%s&datestart=%s' % (req, self.request.GET['datestart'])
				# #req = '%s&dateend=%s' % (req, self.request.GET['dateend']) 
				# #data=data.filter(cdate__gte=fdata['datestart'], cdate__lte=fdata['dateend'])
			
			# if fdata['idays']:
				# req = '%s&idays=%s' % (req, self.request.GET['idays'])
				# self.idays = fdata['idays']
				# log.info(fdata['idays'])
				# # data = data.annotate(num_checks=Sum('check__buyer'))

			# # if fdata['sort']:
			# # 	req = '%s&sort=%s' % (req, self.request.GET['sort'])
			# # 	data=data.order_by(fdata['sort'])
				
				
		self.checkcount = 0
				
		if f.is_valid():
			fdata = f.cleaned_data
			#фильтрация
			if fdata['datestart'] and fdata['idays']:
				req = '%s&datestart=%s' % (req, self.request.GET['datestart'])
				#log.info(fdata['datestart'])
				#data=data.filter(cdate__gte=fdata['datestart'], cdate__lte=fdata['dateend'])
				
				req = '%s&idays=%s' % (req, self.request.GET['idays'])
				self.idays = fdata['idays']
				log.info(fdata['idays'])
				
				# data = data.annotate(num_checks=Sum('check__buyer'))
				
				datestart = fdata['datestart']
				dateend = datestart + datetime.timedelta(days=fdata['idays'])
				
				log.info(datestart)
				log.info(dateend)
				
				
				data=data.filter(cdate__gte=datestart, cdate__lte=dateend)
				
				data=data.filter(buyer__check__time__gte=datestart, buyer__check__time__lte=dateend)
				
				# #
				data = data.annotate(c=Count('buyer__check', filter=Q(buyer__check__time__gte=datestart, buyer__check__time__lte=dateend)))
				self.checkcount = data.aggregate(cc=Sum('c'))['cc']			
				
				
				
		self.req = req
			

			
			
		data=data.order_by('cdate')

		
		
		
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
		context_data = super(report2_smssale, self).get_context_data(*args, **kwargs)
		
		#self.initial.update({'your_field': self.request.user})
		#if "fio" in self.request.GET:
		#	data=data.filter(i__contains=self.request.GET['fio'])
		context_data.update({'req': self.req,})
		context_data.update({'urlpage': '/report/smssale',})
		context_data.update({'idays': self.idays,})
		context_data.update({'count': self.p.count})
		context_data.update({'checkcount': self.checkcount})
		context_data.update({'form': Form_filter_smssale(self.request.GET, initial={"idays": 10}),})
		return context_data

class report2_smssale_after(ListView):
	template_name = 'report_smssale_after.html'
	model = smsqsend
	# paginate_by = 22
	
	def dispatch(self, request, *args, **kwargs):
		return super(report2_smssale_after, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(report2_smssale_after, self).get_queryset()
		
		#data=data.all() #выбираем основной запрос
		# data=data.filter().annotate(s=Sum(F('check__checkitem__price')*F('check__checkitem__col'))-Sum('check__checkitem__checkd__discount'))
		
		f=Form_filter_smssale(self.request.GET)
		log.info(f.errors)
		
		
		self.idays = 0
		
		# self.date1=[data.values('cdate').first(), data.values('cdate').last(), 10]
		
		self.checkcount = 0
		self.totalsum = 0
		buyers = []
		req = ''
		
		if f.is_valid():
			fdata = f.cleaned_data
			#фильтрация
			if fdata['datestart'] and fdata['dateend']:
				req = '%s&datestart=%s' % (req, self.request.GET['datestart'])
				req = '%s&dateend=%s' % (req, self.request.GET['dateend']) 
				data=data.filter(cdate__gte=fdata['datestart'], cdate__lte=fdata['dateend'])
			
			if fdata['idays']:
				req = '%s&idays=%s' % (req, self.request.GET['idays'])
				self.idays = fdata['idays']
				log.info(fdata['idays'])
			
			for d in data:
				check = d.buyer.check_set.filter(time__gte=d.cdate, time__lte=(d.cdate+datetime.timedelta(self.idays))).distinct()
				if check:
					self.checkcount = self.checkcount + check.count()
					buyers.append(d.buyer)
					# print(buyers)
				ci = checkitem.objects.filter(fcheck__in=check).aggregate(ts=Sum('sum'))
				if ci['ts']:
					self.totalsum = self.totalsum + ci['ts']
			
			if fdata['showbuys']:
				req = '%s&showbuys=%s' % (req, self.request.GET['showbuys'])
				data = data.filter(buyer__in=buyers)
				

		self.req = req
		
		data=data.order_by('cdate')

		
		
		
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
		context_data = super(report2_smssale_after, self).get_context_data(*args, **kwargs)
		
		#self.initial.update({'your_field': self.request.user})
		#if "fio" in self.request.GET:
		#	data=data.filter(i__contains=self.request.GET['fio'])
		context_data.update({'req': self.req,})
		context_data.update({'urlpage': '/report/smssaleafter',})
		context_data.update({'idays': self.idays,})
		context_data.update({'count': self.p.count})
		context_data.update({'checkcount': self.checkcount})
		context_data.update({'totalsum': self.totalsum})
		# context_data.update({'date1': self.date1})
		context_data.update({'form': Form_filter_smssale(self.request.GET, initial={"idays": 10}),})
		return context_data

###### Report points starts###########
		
class Form_filter_goods(forms.Form):
	q = forms.CharField(label='Поиск', help_text='Введите слово для поиска', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'off'}), max_length=100, required=False)
	barcode = forms.CharField(label='Штрих код', help_text='Работа со сканером шрих кода', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'off'}), max_length=100, required=False)
	tax = forms.ModelMultipleChoiceField(label='Категория', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), queryset=tax.objects.all(), required=False)
	#sort = forms.ChoiceField(label='Сортировка', help_text='Сортировать по полю', widget=forms.Select(attrs={'class': 'form-control'}), choices=(('id', 'id'),('bday', 'Д. Рождения'),('f', 'Фамилия'),('i', 'Имя'),('o', 'Отчество')), required=False)
	#shop = forms.ChoiceField(label='Магазин', widget=forms.Select(attrs={'class': 'form-control', 'size': '3',}))
	#shop = forms.ChoiceField(label='Магазин', widget=forms.Select(attrs={'class': 'form-control', 'size': '3',}), choices=((i.id, i) for i in shop.objects.filter(status=True)), required=True)
	shop = forms.ModelChoiceField(label='Магазин', widget=forms.Select(attrs={'class': 'form-control', 'size': '3',}), queryset=shop.objects.filter(status=True), required=True)
	
	base = forms.ModelMultipleChoiceField(label='База 1с', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '3',}), queryset=base1c.objects.all(), required=False, initial=2)
	
	pricefrom = forms.FloatField(label="Цена от", required=False,)
	priceto = forms.FloatField(label="Цена до", required=False,)
	
	# paging = forms.BooleanField(label='На одной странице', initial=True, required=False)
	# instock = forms.BooleanField(label='В наличии', initial=True, required=False)
	
	# #
	# showondemo = forms.BooleanField(label='Показывать в демо', initial=False, required=False)
	# touchscreen = forms.BooleanField(label='Отображать на тачскринах', initial=False, required=False)
	
# @method_decorator(permission_required('node.add_goods'), name='dispatch')
class report_points(ListView):
	template_name = 'report_points.html'
	model = goods
	#paginate_by = 10
	
	def dispatch(self, request, *args, **kwargs):
		return super(report_points, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(report_points, self).get_queryset()
		
		data=data.all() #выбираем основной запрос
		
		f=Form_filter_goods(self.request.GET)
		
		
		req = ''
		paging = 20
		
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
				data=data.filter(tax__in=taxin)

			if fdata['shop']:
				req = '%s&shop=%s' % (req, self.request.GET['shop'])
				# datacheckitem=checkitem.objects.filter(fcheck__shop__in=fdata['shop'])
				data=data.filter(checkitem__fcheck__shop__in=fdata['shop'])
				
			if fdata['base']:
				req = '%s&base=%s' % (req, self.request.GET['base'])
				data=data.filter(base=fdata['base'])
				
			if fdata['pricefrom']: #цена gte больше или равно
				req = '%s&pricefrom=%s' % (req, fdata['pricefrom'])
				data=data.filter(price__gte=fdata['pricefrom'])
			if fdata['priceto']: #цена lte маньше или равно
				req = '%s&priceto=%s' % (req, fdata['priceto'])
				data=data.filter(price__lte=fdata['priceto'])
		else:
			data = data.none()
		
		# считаем количество проданных товаров, баллы за шт, количество баллов, коэффициент #
		data = data.annotate(cs=Sum('checkitem__col')).annotate(cp=Cast(F('cs')*F('motivationinpoints'),FloatField())).annotate(tc=Cast(F('cp')*F('checkitem__fcheck__shop__ratio'),FloatField()))
		# self.count_sold = data
		# for item in self.count_sold:
		# 	print u"{0} {1} {2} {3} {4}".format(item.id, item.name, item.cs, item.cp, item.tc)
		# print u"Итого: {0}".format(self.count_sold.count())
		# ##################
		#paginator
		
		self.count_sold = data.aggregate(cs = Sum('tc'))

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
		
		self.req = req
		return pdata
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(report_points, self).get_context_data(*args, **kwargs)
		context_data.update({'req': self.req,})
		context_data.update({'urlpage': '/report_points',})
		context_data.update({'count': self.p.count,})
		context_data.update({'form': Form_filter_goods(self.request.GET, initial={'q': '123',})})
		# context_data.update({'sum': self.sum})
		context_data.update({'count_sold': self.count_sold})
		return context_data

###### Report points ends###########
