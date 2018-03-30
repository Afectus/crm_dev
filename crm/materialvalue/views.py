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
	fields = ['category', 'name', 'model', 'serial', 'pictdesc', 'photo', 'amount', 'assessed_value', 'parent']

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'materialvalue', 'C')
		return super(materialvalue_add, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.save()
		instance.barcode = genbarcode(3, instance.id)
		self.data = instance
		return super(materialvalue_add, self).form_valid(form)

	def get_success_url(self):
		#return reverse('materialvalue:materialvalue_list')
		return reverse('materialvalue:materialvalue_detail', args=[self.data.id])

	def get_success_url(self):
		#return reverse('materialvalue:materialvalue_list')
		return reverse('materialvalue:materialvalue_detail', args=[self.data.id])

class Form_filter_materialvalue(forms.Form):
	q = forms.CharField(label='Поиск по названию', help_text='Введите слово для поиска', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'off'}), max_length=100, required=False)
	category = forms.MultipleChoiceField(label='Категория', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), choices=CATEGORY, required=False)
	shopstock = forms.ModelMultipleChoiceField(label='Магазин/склад', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), queryset=shopstock.objects.filter(), required=False)	
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
				data=data.filter(Q(name__icontains=fdata['q']) | Q(barcode__icontains=fdata['q']))
				
			if fdata['category']:
				req = '%s&category=%s' % (req, self.request.GET['category'])
				data=data.filter(category__in=fdata['category']).distinct() #distinct() если выбирается из нескольких категорий		
			
			if fdata['shopstock']:
				req = '%s&shopstock=%s' % (req, self.request.GET['shopstock'])
				movein=[]
				for i in data:
					a = i.mvmove_set.all()
					# print a
					if a.exists() and a.last().shopstock in fdata['shopstock']:
						# print a.last().materialvalue.id
						movein.append(a.last().materialvalue.id)
				
				data = data.filter(id__in=movein)

			if fdata['paging']:
				req = '%s&paging=%s' % (req, self.request.GET['paging'])
				paging = 1000
				
			#if f.is_valid():
			self.request.session['req'] = req
				
				
		#подсчет количества по остаткам на складах
		# self.sum=data.aggregate(s=Sum('qinstock__value'))

		self.req = req
		

		# ################# исключение категории для отладки
		#t = tax.objects.get(id=18)
		#data=data.exclude(tax=t)
		#self.sum=data.exclude(tax=t).aggregate(s=Sum('qinstock__value'))
		#######################
		data=data.distinct()
		data = data.filter(status='inuse')
		
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
#######################перемещение ценностей###########################	
######################################################################
class Form_filter_materialvalue_gmove_filter(forms.Form):
	ids = forms.ModelMultipleChoiceField(label='Ценности', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), queryset=materialvalue.objects.all(), required=True)
	
class Form_filter_materialvalue_gmove_shopstock(forms.ModelForm):
	ids = forms.ModelMultipleChoiceField(label='Ценности', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), queryset=materialvalue.objects.all(), required=True)
	shopstock = forms.ModelChoiceField(label='Магазин/склад', widget=forms.Select(attrs={'class': 'form-control',}), queryset=shopstock.objects.all(), required=True)
	gmtype = forms.ChoiceField(label='Тип перемещения', widget=forms.Select(attrs={'class': 'form-control',}), choices=MOVETYPES, required=True)
	
	class Meta:
		model = materialvaluegmove
		fields = ['name', 'gmtype']
	
class materialvalue_gmove_shopstock(CreateView):
	template_name = 'materialvalue_gmove.html'
	form_class = Form_filter_materialvalue_gmove_shopstock
	model = materialvaluegmove
	#fields = ['name',]

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'materialvalue', 'L')
		return super(materialvalue_gmove_shopstock, self).dispatch(request, *args, **kwargs) 

	def get_initial(self):
		initial = super(materialvalue_gmove_shopstock, self).get_initial()
		initial = self.request.GET
		return initial
		
	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.save()
		gmove = instance

		fdata = form.cleaned_data

		for i in fdata['ids']:
			move = mvmove.objects.create(shopstock=fdata['shopstock'], materialvalue=i)
			move.materialvaluegmove = gmove
			if gmove.gmtype == 'writeoff':
				# print("Write-off")
				mv = materialvalue.objects.filter(id=i.id).first()
				mv.status = 'decommissioned'
				mv.save()
			move.save()
		return super(materialvalue_gmove_shopstock, self).form_valid(form)
				
	def form_invalid(self, form):
		log.info(form.errors)
		return super(materialvalue_gmove_shopstock, self).form_invalid(form)

	
	def get_context_data(self, *args, **kwargs):
		context_data = super(materialvalue_gmove_shopstock, self).get_context_data(*args, **kwargs)
		#список ценностей
		data=materialvalue.objects.none()
		f=Form_filter_materialvalue_gmove_filter(self.request.GET)
		
		if f.is_valid():
			fdata = f.cleaned_data
			print(fdata)
			if fdata['ids']:
				data=materialvalue.objects.filter(id__in=fdata['ids'])
		
		context_data.update({'object_list': data})
		#
		return context_data

	def get_success_url(self):
		print("All is ok")
		return reverse('materialvalue:materialvalue_list')
		

######################################################################
#######################конец перемещение ценнстей#####################	
######################################################################

class materialvalue_edit(UpdateView):
	model = materialvalue
	template_name = '_edit2.html'
	fields = ['category', 'name', 'model', 'serial', 'pictdesc', 'photo', 'amount', 'status', 'assessed_value', 'parent', 'desc',]

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'materialvalue', 'U')
		return super(materialvalue_edit, self).dispatch(request, *args, **kwargs)

	def get_object(self, queryset=None):
		self.data=super(materialvalue_edit, self).get_object()
		return self.data

	def get_success_url(self):
		#return reverse('materialvalue:materialvalue_list')
		return reverse('materialvalue:materialvalue_detail', args=[self.data.id])

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
		if not self.data.mvmove_set.last().shopstock.profileuser_set.filter(user=self.request.user):
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
		get_object_or_denied(self.request.user, 'materialvalue_addphoto', 'U')
		# location = self.data.mvmove_set.last()
		# if location:
			# if location.shop:
				# if location.shop.profileuser_set.filter(user=self.request.user):
					# return super(materialvalue_addmorephoto, self).dispatch(request, *args, **kwargs)
				# else:
					# get_object_or_denied(self.request.user, 'materialvalue_addphoto', 'U')
					# return super(materialvalue_addmorephoto, self).dispatch(request, *args, **kwargs)
			# else:
				# get_object_or_denied(self.request.user, 'materialvalue_addphoto', 'U')
				# return super(materialvalue_addmorephoto, self).dispatch(request, *args, **kwargs)
		# else:
			# get_object_or_denied(self.request.user, 'materialvalue_addphoto', 'U')
			# return super(materialvalue_addmorephoto, self).dispatch(request, *args, **kwargs)
		return super(materialvalue_addmorephoto, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		photos = self.request.FILES.getlist('photo_field')
	
		for ph in photos:
			cfile = additionalphoto.objects.create(materialvalue=self.data, photo=ph)
			cfile.save()

		return super(materialvalue_addmorephoto, self).form_valid(form)

	def get_success_url(self):
		return reverse('materialvalue:materialvalue_detail', args=[self.data.id])	

		
class materialvalue_delmorephoto(DeleteView): 
	template_name = '_confirm_delete.html'
	model = additionalphoto

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'materialvalue', 'R')
		return super(materialvalue_delmorephoto, self).dispatch(request, *args, **kwargs)
	
	def get_object(self, queryset=None):
		self.data=super(materialvalue_delmorephoto, self).get_object()
		return self.data

	def get_context_data(self, **kwargs):
		context = super(materialvalue_delmorephoto, self).get_context_data(**kwargs)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = reverse('materialvalue:materialvalue_detail', args=[self.data.materialvalue.id])
		return context

	def get_success_url(self):
		return reverse('materialvalue:materialvalue_detail', args=[self.data.materialvalue.id])
		
		
		
		
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
	model = mvmove

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

class FileFieldForm(forms.Form):
	file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
		
class mvfile_add(FormView): 
	form_class = FileFieldForm
	template_name = 'materialvalue_file_add.html'	 # Replace with your template.

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'materialvalue', 'U')
		self.data = get_object_or_404(materialvalue, id=self.kwargs['pk'])
		return super(mvfile_add, self).dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		files = request.FILES.getlist('file_field')

		if form.is_valid():
			for f in files:
				instance = mvfile.objects.create(sourcefile=f, desc=f.name, materialvalue=self.data)
				instance.save()
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def get_success_url(self):
		return reverse('materialvalue:materialvalue_detail', args=[self.data.id])
	
class mvfile_del(DeleteView): 
	template_name = '_confirm_delete.html'
	model = mvfile

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'materialvalue', 'U')
		return super(mvfile_del, self).dispatch(request, *args, **kwargs)
	
	def get_object(self, queryset=None):
		self.data=super(mvfile_del, self).get_object()
		return self.data

	def get_context_data(self, **kwargs):
		context = super(mvfile_del, self).get_context_data(**kwargs)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = reverse('materialvalue:materialvalue_detail', args=[self.data.materialvalue.id])
		return context

	def get_success_url(self):
		return reverse('materialvalue:materialvalue_detail', args=[self.data.materialvalue.id])


#######################################

class materialvaluetoshopstockForm(forms.ModelForm):
	# shop = forms.ModelChoiceField(label='Магазин',queryset=shop.objects.all(), required=True)
	class Meta:
		model = mvmove
		fields = ['mdate', 'shopstock', 'note']

class materialvaluemove_toshopstock(FormView):
	form_class = materialvaluetoshopstockForm
	template_name = '_edit2.html'
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'materialvalue', 'C')
		self.data = get_object_or_404(materialvalue, id=self.kwargs['pk'])
		return super(materialvaluemove_toshopstock, self).dispatch(request, *args, **kwargs)
	
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
			form = super(materialvaluemove_toshopstock, self).get_form(form_class)
			# form.fields['sdate'].widget.attrs['class'] = 'form-control datepicker'
			form.fields['mdate'].widget.attrs['class'] = 'form-control datepicker'
			#form.fields['sdate'].input_formats=['%d-%m-%y', '%d-%m-%Y',]
			form.fields['shopstock'].required = True
			if self.data.mvmove_set.all().exists():
				if self.data.mvmove_set.last().shopstock is not None:
					form.fields['shopstock'].queryset=shopstock.objects.exclude(name=self.data.mvmove_set.last().shopstock.name)
			return form
		return form_class(**self.get_form_kwargs())

	def form_valid(self, form):
		data = mvmove.objects.create(
			materialvalue=self.data,
			mdate = form.cleaned_data['mdate'],
			shopstock = form.cleaned_data['shopstock'],
			note = form.cleaned_data['note']
			)  
		return super(materialvaluemove_toshopstock, self).form_valid(form)
	
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

########### операции с контейнерами и ячейками

class materialvalue_container_add(CreateView):
	model = mvcontainer
	template_name = '_edit2.html'
	fields = ['name', 'shopstock']

	def dispatch(self, request, *args, **kwargs):
		
		# get_object_or_denied(self.request.user, 'materialvalue', 'C')
		return super(materialvalue_container_add, self).dispatch(request, *args, **kwargs)
	
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
			form = super(materialvalue_container_add, self).get_form(form_class)
			form.fields['shopstock'].required = True
			form.fields['shopstock'].queryset=shopstock.objects.filter(profileuser__user=self.request.user)
			return form
		return form_class(**self.get_form_kwargs())

	def get_success_url(self):
		return reverse('materialvalue:materialvalue_container_list')

class materialvalue_container_edit(UpdateView):
	model = mvcontainer
	template_name = '_edit2.html'
	fields = ['name', 'shopstock']

	def dispatch(self, request, *args, **kwargs):
		# get_object_or_denied(self.request.user, 'materialvalue', 'C')

		return super(materialvalue_container_edit, self).dispatch(request, *args, **kwargs)
	
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
			form = super(materialvalue_container_edit, self).get_form(form_class)
			form.fields['shopstock'].required = True
			form.fields['shopstock'].queryset=shopstock.objects.filter(profileuser__user=self.request.user)
			return form
		return form_class(**self.get_form_kwargs())
	# def form_valid(self, form):
	# 	instance = form.save(commit=False)
	# 	instance.shop = self.request.user
	# 	instance.save()
	# 	return super(materialvalue_container_edit, self).form_valid(form)

	def get_success_url(self):
		return reverse('materialvalue:materialvalue_container_list')

class materialvalue_container_list(ListView): 
	template_name = 'materialvalue_container_list.html' 
	model = mvcontainer
	# paginate_by = 40

	def dispatch(self, request, *args, **kwargs):
		# get_object_or_denied(self.request.user, 'materialvalue', 'L')
		return super(materialvalue_container_list, self).dispatch(request, *args, **kwargs) 

	def get_queryset(self):
		data=super(materialvalue_container_list, self).get_queryset()
		data = data.filter(shopstock__profileuser__user=self.request.user)
		return data

class materialvalue_container_del(DeleteView): 
	template_name = '_confirm_delete.html' 
	model = mvcontainer

	def dispatch(self, request, *args, **kwargs):
		# get_object_or_denied(self.request.user, 'materialvalue', 'U')
		self.data = get_object_or_404(mvcontainer, id=self.kwargs['pk'])
		if not self.data.shopstock.profileuser_set.filter(user=self.request.user):
			raise PermissionDenied
		return super(materialvalue_container_del, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(materialvalue_container_del, self).get_context_data(**kwargs)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = reverse('materialvalue:materialvalue_container_list')
		return context

	def get_success_url(self):
		return reverse('materialvalue:materialvalue_container_list')

class materialvalue_container_detail(ListView): 
	template_name = 'materialvalue_container_detail.html' 
	model = mvcell
	# paginate_by = 40

	def dispatch(self, request, *args, **kwargs):
		# get_object_or_denied(self.request.user, 'materialvalue', 'R')
		self.data = get_object_or_404(mvcontainer, id=self.kwargs['pk'])
		if not self.data.shopstock.profileuser_set.filter(user=self.request.user):
			raise PermissionDenied
		return super(materialvalue_container_detail, self).dispatch(request, *args, **kwargs)
	
	def get_queryset(self):
		data=super(materialvalue_container_detail, self).get_queryset()
		data = data.filter(container=self.data)
		return data

	def get_context_data(self, *args, **kwargs):
		context_data = super(materialvalue_container_detail, self).get_context_data(*args, **kwargs)
		context_data.update({'object': self.data,})
		return context_data

class materialvalue_cell_add(CreateView):
	model = mvcell
	template_name = '_edit2.html' 
	fields = ['name']
	# paginate_by = 40

	def dispatch(self, request, *args, **kwargs):
		# get_object_or_denied(self.request.user, 'materialvalue', 'R')
		self.data = get_object_or_404(mvcontainer, id=self.kwargs['pk'])
		if not self.data.shopstock.profileuser_set.filter(user=self.request.user):
			raise PermissionDenied
		return super(materialvalue_cell_add, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.container = self.data
		instance.save()
		return super(materialvalue_cell_add, self).form_valid(form)

	def get_success_url(self):
		return reverse('materialvalue:materialvalue_container_detail', args=[self.data.id])

class materialvalue_cell_edit(UpdateView):
	model = mvcell
	template_name = '_edit2.html' 
	fields = ['name']
	# paginate_by = 40

	def dispatch(self, request, *args, **kwargs):
		# get_object_or_denied(self.request.user, 'materialvalue', 'R')
		self.data = get_object_or_404(mvcell, id=self.kwargs['pk'])
		if not self.data.container.shopstock.profileuser_set.filter(user=self.request.user):
			raise PermissionDenied
		return super(materialvalue_cell_edit, self).dispatch(request, *args, **kwargs)

	def get_success_url(self):
		return reverse('materialvalue:materialvalue_container_detail', args=[self.data.container.id])

class materialvalue_cell_del(DeleteView): 
	template_name = '_confirm_delete.html' 
	model = mvcell

	def dispatch(self, request, *args, **kwargs):
		# get_object_or_denied(self.request.user, 'materialvalue', 'U')
		self.data = get_object_or_404(mvcell, id=self.kwargs['pk'])
		if not self.data.container.shopstock.profileuser_set.filter(user=self.request.user):
			raise PermissionDenied
		return super(materialvalue_cell_del, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(materialvalue_cell_del, self).get_context_data(**kwargs)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = reverse('materialvalue:materialvalue_container_detail', args=[self.data.container.id])
		return context

	def get_success_url(self):
		return reverse('materialvalue:materialvalue_container_detail', args=[self.data.container.id])


class materialvalue_movetocell(UpdateView):
	model = mvmove
	template_name = '_edit2.html'
	fields = ['mvcell']

	def dispatch(self, request, *args, **kwargs):
		# get_object_or_denied(self.request.user, 'materialvalue', 'U')
		self.data = get_object_or_404(mvmove,id=self.kwargs['pk'])
		if not self.data.shopstock.profileuser_set.filter(user=self.request.user):
			raise PermissionDenied
		return super(materialvalue_movetocell, self).dispatch(request, *args, **kwargs)
	
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
			form = super(materialvalue_movetocell, self).get_form(form_class)
			form.fields['mvcell'].required = True
			if self.data.shopstock:
				if self.data.shopstock is not None:
					form.fields['mvcell'].queryset=mvcell.objects.filter(container__shopstock=self.data.shopstock)
			return form
		return form_class(**self.get_form_kwargs())

	def get_success_url(self):
		return reverse('materialvalue:materialvalue_detail',args=[self.data.materialvalue.id])

