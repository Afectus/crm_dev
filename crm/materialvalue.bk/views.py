# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse
from django.http import Http404
from django.contrib.auth.models import User

import time
import requests
import datetime
from django.utils import timezone
from django.contrib import messages
# Create your views here.
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView

from django.views.generic import DetailView, DeleteView
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView

from django.contrib.admin.widgets import AdminDateWidget 

from dj.views import *
from acl.views import *
from node.models import *
from .models import *
from django.urls import reverse



import logging
log = logging.getLogger(__name__)

# grantchoice=(('L', 'Список'), ('R', 'Чтение'), ('С', 'Создание'), ('U', 'Редактирование'),)

class materialvalue_add(CreateView):
	model = materialvalue
	template_name = '_edit2.html'
	fields = ['category', 'name', 'model', 'serial', 'pictdesc', 'photo', 'amount']

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'materialvalue', 'C')
		return super(materialvalue_add, self).dispatch(request, *args, **kwargs)

	# def form_valid(self, form):
	#	  instance = form.save(commit=False)
	#	  # instance.user = self.request.user
	#	  instance.save()
	#	  return super(materialvalue_add, self).form_valid(form)

	def get_success_url(self):
		return reverse('materialvalue:materialvalue_list')

class Form_filter_materialvalue(forms.Form):
	q = forms.CharField(label='Поиск по названию', help_text='Введите слово для поиска', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'off'}), max_length=100, required=False)
	category = forms.MultipleChoiceField(label='Категория', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), choices=CATEGORY, required=False)
	stock = forms.ModelMultipleChoiceField(label='Склад', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), queryset=stock.objects.filter(status=True), required=False)
	shop = forms.ModelMultipleChoiceField(label='Магазин', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), queryset=shop.objects.filter(status=True), required=False)	
	paging = forms.BooleanField(label='На одной странице', initial=True, required=False)
	# printing = forms.BooleanField(label='Вывод на печать', initial=True, required=False)

class materialvalue_list(ListView): 
	template_name = 'materialvalue_list.html' 
	model = materialvalue
	# paginate_by = 40

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'materialvalue', 'L')
		return super(materialvalue_list, self).dispatch(request, *args, **kwargs) 

	def get_queryset(self):
		data=super(materialvalue_list, self).get_queryset()
		
		data=data.all() #выбираем основной запрос
		f=Form_filter_materialvalue(self.request.GET)
		
		
		req = ''
		paging = 40
		
		if f.is_valid():
			fdata = f.cleaned_data
			#фильтрация
			if fdata['q']:
				req = '%s&q=%s' % (req, fdata['q'])
				data=data.filter(name=fdata['q'])
				
			if fdata['category']:
				req = '%s&category=%s' % (req, self.request.GET['category'])
				data=data.filter(category__in=fdata['category']).distinct() #distinct() если выбирается из нескольких категорий

			if fdata['stock']:
				req = '%s&stock=%s' % (req, self.request.GET['stock'])
				movein=[]
				for i in data:
					a = i.materialvaluemove_set.all()
					# print a
					if a.exists() and a.last().stock in fdata['stock']:
						# print a.last().materialvalue.id
						movein.append(a.last().materialvalue.id)

				data = data.filter(id__in=movein)
				
				# data=data.filter(materialvaluemove__stock__gte=1, materialvaluemove__stock__in=fdata['stock']).distinct()
				
			
			if fdata['shop']:
				req = '%s&shop=%s' % (req, self.request.GET['shop'])
				movein=[]
				for i in data:
					a = i.materialvaluemove_set.all()
					# print a
					if a.exists() and a.last().shop in fdata['shop']:
						# print a.last().materialvalue.id
						movein.append(a.last().materialvalue.id)
				
				data = data.filter(id__in=movein)

			if fdata['paging']:
				req = '%s&paging=%s' % (req, self.request.GET['paging'])
				paging = 1000
				
		#подсчет количества по остаткам на складах
		# self.sum=data.aggregate(s=Sum('qinstock__value'))

		self.req = req

		# ################# исключение категории для отладки
		#t = tax.objects.get(id=18)
		#data=data.exclude(tax=t)
		#self.sum=data.exclude(tax=t).aggregate(s=Sum('qinstock__value'))
		#######################
		
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
		context_data = super(materialvalue_list, self).get_context_data(*args, **kwargs)
		context_data.update({'req': self.req,})
		context_data.update({'count': self.p.count,})
		context_data.update({'form': Form_filter_materialvalue(self.request.GET, initial={'q': '123',})})
		context_data.update({'urlpage': reverse('materialvalue:materialvalue_list'),})
		# context_data.update({'sum': self.sum})
		
		return context_data

class materialvalue_list_print(materialvalue_list):
	template_name = 'materialvalue_list_print.html'
	paginate_by = 10000
	
	
######################################################################
#######################перемещение ценнстей###########################	
######################################################################
class Form_filter_materialvalue_gmove_filter(forms.Form):
	ids = forms.ModelMultipleChoiceField(label='Ценности', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), queryset=materialvalue.objects.all(), required=True)

class Form_filter_materialvalue_gmove_shop(forms.ModelForm):
	ids = forms.ModelMultipleChoiceField(label='Ценности', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), queryset=materialvalue.objects.all(), required=True)
	shop = forms.ModelChoiceField(label='Магазин', widget=forms.Select(attrs={'class': 'form-control',}), queryset=shop.objects.all(), required=True)
	class Meta:
		model = materialvaluegmove
		fields = ['name',]
	
class materialvalue_gmove_shop(CreateView):
	template_name = 'materialvalue_gmove.html'
	form_class = Form_filter_materialvalue_gmove_shop
	model = materialvaluegmove
	#fields = ['name',]

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'materialvalue', 'L')
		return super(materialvalue_gmove_shop, self).dispatch(request, *args, **kwargs) 

	def get_initial(self):
		initial = super(materialvalue_gmove_shop, self).get_initial()
		initial = self.request.GET
		return initial
		
	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.save()
		gmove = instance

		fdata = form.cleaned_data

		for i in fdata['ids']:
			move = materialvaluemove.objects.create(shop=fdata['shop'], materialvalue=i)
			move.materialvaluegmove = gmove
			move.save()
		return super(materialvalue_gmove_shop, self).form_valid(form)
				
	def form_invalid(self, form):
		log.info(form.errors)
		return super(materialvalue_gmove_shop, self).form_invalid(form)

	def get_success_url(self):
		return reverse('materialvalue:materialvalue_list')
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(materialvalue_gmove_shop, self).get_context_data(*args, **kwargs)
		#список ценностей
		data=materialvalue.objects.none()
		f=Form_filter_materialvalue_gmove_filter(self.request.GET)
		
		if f.is_valid():
			fdata = f.cleaned_data
			if fdata['ids']:
				data=materialvalue.objects.filter(id__in=fdata['ids'])
		context_data.update({'object_list': data})
		#
		return context_data
		
class Form_filter_materialvalue_gmove_stock(forms.ModelForm):
	ids = forms.ModelMultipleChoiceField(label='Ценности', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), queryset=materialvalue.objects.all(), required=True)
	stock = forms.ModelChoiceField(label='Склад', widget=forms.Select(attrs={'class': 'form-control',}), queryset=stock.objects.all(), required=True)
	class Meta:
		model = materialvaluegmove
		fields = ['name',]		

class materialvalue_gmove_stock(materialvalue_gmove_shop): 
	form_class = Form_filter_materialvalue_gmove_stock
		
	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.save()
		gmove = instance

		fdata = form.cleaned_data

		for i in fdata['ids']:
			move = materialvaluemove.objects.create(stock=fdata['stock'], materialvalue=i)
			move.materialvaluegmove = gmove
			move.save()
		return super(materialvalue_gmove_shop, self).form_valid(form)
				

		
######################################################################
#######################конец перемещение ценнстей#####################	
######################################################################


class materialvalue_edit(UpdateView):
	model = materialvalue
	template_name = '_edit2.html'
	fields = ['category', 'name', 'model', 'serial', 'pictdesc', 'photo', 'amount', 'status']

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'materialvalue', 'U')
		return super(materialvalue_edit, self).dispatch(request, *args, **kwargs)

	# def get_object(self, queryset=None):
	#	  return get_object_or_denied(self.request.user, 'materialvalue', 'U')

	def get_success_url(self):
		return reverse('materialvalue:materialvalue_list')

#для кассиров
# старое редактирование фотографий ценности, 
# на случай если понадобиться редактировать старые фото
#		
class materialvalue_addphoto(UpdateView):
	model = materialvalue
	template_name = '_edit2.html'
	fields = ['pictdesc', 'photo']

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'materialvalue_addphoto', 'U')
		self.data = get_object_or_404(materialvalue, id=self.kwargs['pk'])
		# print self.data.materialvaluemove_set.last().shop.profileuser_set
		if not self.data.materialvaluemove_set.last().shop.profileuser_set.filter(user=self.request.user):
			raise PermissionDenied
		return super(materialvalue_addphoto, self).dispatch(request, *args, **kwargs)

	def get_success_url(self):
		return reverse('materialvalue:materialvalue_detail', args=[self.data.id])

class addphotoForm(forms.Form):
	photo_field = forms.FileField(label='Дополнительные фото объекта',widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

class materialvalue_addmorephoto(FormView):
	form_class = addphotoForm
	template_name = '_edit2.html'

	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(materialvalue, id=self.kwargs['pk'])
		location = self.data.materialvaluemove_set.last()
		if location:
			if location.shop:
				if location.shop.profileuser_set.filter(user=self.request.user):
					return super(materialvalue_addmorephoto, self).dispatch(request, *args, **kwargs)
				else:
					get_object_or_denied(self.request.user, 'materialvalue_addphoto', 'U')
					return super(materialvalue_addmorephoto, self).dispatch(request, *args, **kwargs)
			else:
				get_object_or_denied(self.request.user, 'materialvalue_addphoto', 'U')
				return super(materialvalue_addmorephoto, self).dispatch(request, *args, **kwargs)
		else:
			get_object_or_denied(self.request.user, 'materialvalue_addphoto', 'U')
			return super(materialvalue_addmorephoto, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		photos = self.request.FILES.getlist('photo_field')
	
		for ph in photos:
			cfile = additionalphoto.objects.create(materialvalue=self.data, photo=ph)
			cfile.save()

		return super(materialvalue_addmorephoto, self).form_valid(form)

	def get_success_url(self):
		return reverse('materialvalue:materialvalue_detail', args=[self.data.id])	

class materialvalue_del(DeleteView): 
	template_name = '_confirm_delete.html' 
	model = materialvalue

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'materialvalue', 'U')
		return super(materialvalue_del, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(materialvalue_del, self).get_context_data(**kwargs)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = reverse('materialvalue:materialvalue_list')
		return context

	def get_success_url(self):
		return reverse('materialvalue:materialvalue_list')

class materialvalue_detail(ListView): 
	template_name = 'materialvalue_detail.html' 
	model = materialvaluemove

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'materialvalue', 'R')
		self.data = get_object_or_404(materialvalue, id=self.kwargs['pk'])
		return super(materialvalue_detail, self).dispatch(request, *args, **kwargs)
	
	# def get_queryset(self):
		
	#	  data=super(materialvalue_detail, self).get_queryset()
	#	  return data

	def get_context_data(self, *args, **kwargs):
		context_data = super(materialvalue_detail, self).get_context_data(*args, **kwargs)
		context_data.update({'object': self.data,})
		return context_data
		
		
class materialvalue_detail_print(materialvalue_detail): 
	template_name = 'materialvalue_detail_print.html' 	
		

#######################################

class materialvaluetoshopForm(forms.ModelForm):
	# shop = forms.ModelChoiceField(label='Магазин',queryset=shop.objects.all(), required=True)
	class Meta:
		model = materialvaluemove
		fields = ['mdate','shop','note']

class materialvaluemove_toshop(FormView):
	form_class = materialvaluetoshopForm
	template_name = '_edit2.html'
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'materialvalue', 'C')
		self.data = get_object_or_404(materialvalue, id=self.kwargs['pk'])
		return super(materialvaluemove_toshop, self).dispatch(request, *args, **kwargs)
	
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
			form = super(materialvaluemove_toshop, self).get_form(form_class)
			# form.fields['sdate'].widget.attrs['class'] = 'form-control datepicker'
			form.fields['mdate'].widget.attrs['class'] = 'form-control datepicker'
			#form.fields['sdate'].input_formats=['%d-%m-%y', '%d-%m-%Y',]
			form.fields['shop'].required = True
			if self.data.materialvaluemove_set.all().exists():
				if self.data.materialvaluemove_set.last().shop is not None:
					form.fields['shop'].queryset=shop.objects.exclude(name=self.data.materialvaluemove_set.last().shop.name)
			return form
		return form_class(**self.get_form_kwargs())

	def form_valid(self, form):
		data = materialvaluemove.objects.create(
			materialvalue=self.data,
			mdate = form.cleaned_data['mdate'],
			shop = form.cleaned_data['shop'],
			note = form.cleaned_data['note']
			)  
		return super(materialvaluemove_toshop, self).form_valid(form)
	
	def get_success_url(self):
		return reverse('materialvalue:materialvalue_detail', args=[self.data.id])

class materialvaluetostockForm(forms.ModelForm):
	# shop = forms.ModelChoiceField(label='Магазин',queryset=shop.objects.all(), required=True)
	class Meta:
		model = materialvaluemove
		fields = ['mdate','stock','note']

class materialvaluemove_tostock(FormView):
	form_class = materialvaluetostockForm
	template_name = '_edit2.html'
	# fields = ['mdate', 'stock', 'note']

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'materialvalue', 'C')
		self.data = get_object_or_404(materialvalue, id=self.kwargs['pk'])
		return super(materialvaluemove_tostock, self).dispatch(request, *args, **kwargs)
	
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
			form = super(materialvaluemove_tostock, self).get_form(form_class)
			# form.fields['sdate'].widget.attrs['class'] = 'form-control datepicker'
			form.fields['mdate'].widget.attrs['class'] = 'form-control datepicker'
			#form.fields['sdate'].input_formats=['%d-%m-%y', '%d-%m-%Y',]
			#form.fields['edate'].input_formats=['%d-%m-%y', '%d-%m-%Y',]
			form.fields['stock'].required = True
			if self.data.materialvaluemove_set.all().exists():
				if self.data.materialvaluemove_set.last().stock is not None:
					form.fields['stock'].queryset=stock.objects.exclude(name=self.data.materialvaluemove_set.last().stock.name)
			return form
		return form_class(**self.get_form_kwargs())

	def form_valid(self, form):
		data = materialvaluemove.objects.create(
			materialvalue=self.data,
			mdate = form.cleaned_data['mdate'],
			stock = form.cleaned_data['stock'],
			note = form.cleaned_data['note']
			)	 
		return super(materialvaluemove_tostock, self).form_valid(form)
	
	def get_success_url(self):
		return reverse('materialvalue:materialvalue_detail', args=[self.data.id])

		
		
		
######## Список групповых перемещений ценностей

class materialvalue_gmove_list(ListView): 
	template_name = 'materialvalue_gmove_list.html' 
	model = materialvaluegmove

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'materialvalue', 'R')
		return super(materialvalue_gmove_list, self).dispatch(request, *args, **kwargs)

class materialvalue_gmove_detail(DetailView): 
	template_name = 'materialvalue_gmove_detail.html' 
	model = materialvaluegmove

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'materialvalue', 'R')
		# self.data = get_object_or_404(materialvaluegmove, id=self.kwargs['pk'])
		return super(materialvalue_gmove_detail, self).dispatch(request, *args, **kwargs)

	# def get_context_data(self, *args, **kwargs):
	#	context_data = super(materialvalue_gmove_detail, self).get_context_data(*args, **kwargs)
	#	context_data.update({'': self.data,})
	#	return context_data
	
	
class materialvalue_gmove_detail_print(DetailView):
	template_name = 'materialvalue_gmove_detail_print.html'
	model = materialvaluegmove

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'materialvalue', 'R')
		# self.data = get_object_or_404(materialvaluegmove, id=self.kwargs['pk'])
		return super(materialvalue_gmove_detail_print, self).dispatch(request, *args, **kwargs)


		