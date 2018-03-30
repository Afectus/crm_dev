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


from django.core.mail import send_mail


from node.templatetags.nodetag import *

from node.models import *
from panel.form import *
from panel.models import *
from panel.form import *
from workflow.models import *


import logging
log = logging.getLogger(__name__)




@method_decorator(permission_required('workflow.add_printtask'), name='dispatch')
class printtask_list(ListView):
	template_name = 'printtask_list.html'
	model = printtask
	#paginate_by = 40
	
	def dispatch(self, request, *args, **kwargs):
		return super(printtask_list, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		self.data=super(printtask_list, self).get_queryset()
		self.data=self.data.filter(user=self.request.user) #выбираем основной запрос
		return self.data
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(printtask_list, self).get_context_data(*args, **kwargs)
		context_data.update({'itembarcode': printtask.objects.filter(user=self.request.user, barcode__isnull=False).exclude(barcode__exact=''),})
		context_data.update({'itemprice': printtask.objects.filter(user=self.request.user, imageprice__isnull=False).exclude(imageprice__exact=''),})
		context_data.update({'stock': stock.objects.filter(status=True),})
		#sum
		sum=self.data.aggregate(s=Sum('copies'))
		context_data.update({'sum': sum['s'],})
		return context_data
		
		
@method_decorator(permission_required('workflow.add_printtask'), name='dispatch')	
class printtask_edit(UpdateView):
	model = printtask
	template_name = 'printtask_edit.html'
	success_url = '/printtask/list/'
	fields = ['status', 'copies', 'barcode', ]
	
	def dispatch(self, request, *args, **kwargs):
		data = get_object_or_404(self.model, user=self.request.user, status=True, id=self.kwargs['pk'])
		return super(printtask_edit, self).dispatch(request, *args, **kwargs)	

		
@method_decorator(permission_required('workflow.add_(printtask'), name='dispatch')	
class printtask_detail(DetailView):
	model = printtask
	template_name = '(printtask_detail.html'
	
	def dispatch(self, request, *args, **kwargs):
		data = get_object_or_404(self.model, user=self.request.user, id=self.kwargs['pk'])
		return super(printtask_detail, self).dispatch(request, *args, **kwargs)	


		
@method_decorator(permission_required('workflow.add_printtask'), name='dispatch')
class printtask_del(DeleteView):
	model = printtask
	template_name = '_confirm_delete.html'
	success_url = '/printtask/list/'

	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(self.model, user=self.request.user, status=True, id=self.kwargs['pk'])
		return super(printtask_del, self).dispatch(request, *args, **kwargs)
	
	#def get_object(self, queryset=None):
	#	return get_object_or_404(self.model, id=self.kwargs['pk'])
		
	#Django DeleteView without confirmation template
	def get(self, request, *args, **kwargs):
		return self.post(request, *args, **kwargs)
		
	def get_context_data(self, **kwargs):
		context = super(printtask_del, self).get_context_data(**kwargs)
		context['object'] = self.data.id
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = '/printtask/list/'
		return context
		

#@csrf_exempt
@permission_required('workflow.add_printtask')
def printtask_add(request, pk, copies, barcode):
	if request.method == 'GET':
		try:
			data = goods.objects.get(id=pk)
		except:
			pass
		else:
			if printtask.objects.filter(goods=data, barcode=barcode).exists():
				tmp={'res': 2, 'data': 'exist',}
				return HttpResponse(json.dumps(tmp), content_type='application/json')
			else:
				p=printtask(user=request.user, goods=data, copies=copies, barcode=barcode)
				p.save()
				tmp={'res': 1, 'data': p.id,}
				return HttpResponse(json.dumps(tmp), content_type='application/json')
	tmp={'res': 0, 'data': u'bad',}
	return HttpResponse(json.dumps(tmp), content_type='application/json')
	
# #@csrf_exempt
# @permission_required('workflow.add_printtask')
# def printtask_add_nobarcode(request, pk, copies):
	# if request.method == 'GET':
		# try:
			# data = goods.objects.get(id=pk)
		# except:
			# pass
		# else:
			# if printtask.objects.filter(goods=data).exists():
				# tmp={'res': 2, 'data': 'exist',}
				# return HttpResponse(json.dumps(tmp), content_type='application/json')
			# else:
				# p=printtask(goods=data, copies=copies)
				# p.save()
				# tmp={'res': 1, 'data': p.id,}
				# return HttpResponse(json.dumps(tmp), content_type='application/json')
	# tmp={'res': 0, 'data': u'bad',}
	# return HttpResponse(json.dumps(tmp), content_type='application/json')

@permission_required('workflow.add_printtask')
def printtask_clear(request):
	if request.method == 'GET':
		printtask.objects.filter(user=request.user).delete()
	return HttpResponseRedirect('/printtask/list')
	
	
	

class Form_imageprice(forms.ModelForm):
	class Meta:
		model = printtask
		fields = ['imageprice',]

#@permission_required('workflow.add_printtask')
@csrf_exempt
def price2image_add(request, pk):
	#вызывается битриксом
	if request.method == 'POST':
		try:
			instance = printtask.objects.get(goods__idbitrix=pk)
		except:
			pass
		else:
			f=Form_imageprice(request.POST, request.FILES, instance=instance)
			if f.is_valid():
				cd = f.cleaned_data
				f.save()
				tmp={'res': 1, 'data': u'good',}
				return HttpResponse(json.dumps(tmp), content_type='application/json')
	tmp={'res': 0, 'data': u'bad',}
	return HttpResponse(json.dumps(tmp), content_type='application/json')
	
	
#@csrf_exempt
@permission_required('workflow.add_printtask')
def printtask_copies(request, copies):
	if request.method == 'GET':
		if int(copies) >= 1:
			printtask.objects.filter(user=request.user).update(copies=copies)
		if int(copies) == 0:
			for i in printtask.objects.filter(user=self.request.user):
				#q=qinstock.objects.filter(goods=i.goods)
				q=qinstock.objects.filter(goods=i.goods).aggregate(s=Sum('value'))
				i.copies=q['s']
				i.save()
	return HttpResponseRedirect('/printtask/list')
	
	
#@csrf_exempt
@permission_required('workflow.add_printtask')
def printtask_stock(request, id):
	if request.method == 'GET':
		s=stock.objects.get(id=id)
		for i in printtask.objects.filter(user=self.request.user):
			q=qinstock.objects.filter(stock=s, goods=i.goods).aggregate(s=Sum('value'))
			if q['s']:
				i.copies=q['s']
			else:
				i.copies=0
			i.save()
	return HttpResponseRedirect('/printtask/list')
	
	
	
	
#ПОСТАВЩИКИ	
#@method_decorator(permission_required('workflow.add_distributor'), name='dispatch')
class distributor_list(ListView):
	template_name = 'distributor_list.html'
	model = distributor
	paginate_by = 20
	
	def get_queryset(self):
		data=super(distributor_list, self).get_queryset()
		data=data.filter(distributormenu__aclu__user=self.request.user, distributormenu__aclu__type='R')
		self.dm=None
		if 'pk' in self.kwargs:
			self.dm=get_object_or_404(distributormenu, id=self.kwargs['pk'], aclu__user=self.request.user, aclu__type='R')
			data=data.filter(distributormenu=self.dm)
		return data
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(distributor_list, self).get_context_data(*args, **kwargs)
		context_data.update({'distributormenu': distributormenu.objects.filter(aclu__user=self.request.user, aclu__type='R'),})
		context_data.update({'dm': self.dm})
		return context_data
	
#@method_decorator(permission_required('workflow.add_distributor'), name='dispatch')
class distributor_add(CreateView):
	model = distributor
	template_name = 'distributor_add.html'
	success_url = '/distributor/list'
	fields = ['name', 'distributormenu', 'c', 'tax2', 'a', 'b', 'desc', 'pricefile', 'pricefile2', 'pricefile3',]
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'distributor', 'R')
		return super(distributor_add, self).dispatch(request, *args, **kwargs)
	
	

#@method_decorator(permission_required('workflow.add_distributor'), name='dispatch')
class distributor_edit(UpdateView):
	model = distributor
	template_name = 'distributor_edit.html'
	success_url = '/distributor/list'
	fields = ['name', 'distributormenu', 'c', 'tax2', 'a', 'b', 'desc', 'pricefile', 'pricefile2', 'pricefile3',]
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'distributor', 'R')
		get_object_or_404(self.model, id=self.kwargs['pk'])
		return super(distributor_edit, self).dispatch(request, *args, **kwargs)
		
#@method_decorator(permission_required('workflow.add_distributor'), name='dispatch')
class distributormenu_edit(UpdateView):
	model = distributormenu
	template_name = 'distributormenu_edit.html'
	success_url = '/distributor/list'
	fields = ['aclu',]
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'distributor', 'R')
		get_object_or_404(self.model, id=self.kwargs['pk'])
		return super(distributormenu_edit, self).dispatch(request, *args, **kwargs)
##############################
	
	
	
class Form_printbarcodetext(forms.Form):
	name = forms.CharField(label='Название', help_text='Название', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'off'}), max_length=100, required=True)
	barcode = forms.CharField(label='Штрихкод', help_text='Штрихкод', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'off'}), max_length=100, required=True)
	col = forms.IntegerField(label='Количество', help_text='Количество', min_value=1, max_value=1000, required=True, initial=1)
	

	
@method_decorator(permission_required('workflow.add_printtask'), name='dispatch')
class printbarcodetext(FormView):
	template_name = 'printbarcodetext.html'
	success_url = '/printtask/printbarcodetext'
	form_class = Form_printbarcodetext
	
	# def dispatch(self, request, *args, **kwargs):
		# #self.e = get_object_or_404(self.model, id=self.kwargs['pk'], user=request.user) #ПОТОМ ВКЛЮЧИТЬ
		# return super(printbarcodetext, self).dispatch(request, *args, **kwargs)
	
	# def get_success_url(self):
		# url = '/goods/edit/%s' % (self.get_object().id)
		# if self.saveonclose:
			# url = reverse('panel:saveonclose')
		# return url
	
	# def get_context_data(self, **kwargs):
		# context = super(printbarcodetext, self).get_context_data(**kwargs)
		# context['object'] = self.get_object()
		# return context
	
	# def get_initial(self):
		# return {'buyer':self.b, 'user': self.request.user}
	
	# def get_form(self, form_class=None):
		# if form_class is None:
			# form_class = self.get_form_class()
			# form = super(printbarcodetext, self).get_form(form_class)
			# form.fields['saveonclose'].widget=forms.HiddenInput()
			# return form
		# return form_class(**self.get_form_kwargs())
	
	# def form_valid(self, form):
		# self.object = form.save(commit=False)
		# # self.object.user = self.request.user
		# # self.object.save()
		# if form.cleaned_data['saveonclose'] == 'true':
			# self.saveonclose = True
		# return super(printbarcodetext, self).form_valid(form)
		
	#def form_invalid(self, form):
		#print form.errors
	#	return super(printbarcodetext, self).form_invalid(form)
			

	
	
	
class Form_printtext(forms.Form):
	value = forms.CharField(label='Текст', help_text='Текст', widget=forms.TextInput(attrs={'class': 'form-control',}), max_length=500, required=True)
	col = forms.IntegerField(label='Количество', help_text='Количество', min_value=1, max_value=1000, required=True, initial=1)
	

	
@method_decorator(permission_required('workflow.add_printtask'), name='dispatch')
class printtext(FormView):
	template_name = 'printtext.html'
	success_url = '/printtask/printtext'
	form_class = Form_printtext
	
	# def dispatch(self, request, *args, **kwargs):
		# #self.e = get_object_or_404(self.model, id=self.kwargs['pk'], user=request.user) #ПОТОМ ВКЛЮЧИТЬ
		# return super(printbarcodetext, self).dispatch(request, *args, **kwargs)
	
	# def get_success_url(self):
		# url = '/goods/edit/%s' % (self.get_object().id)
		# if self.saveonclose:
			# url = reverse('panel:saveonclose')
		# return url
	
	# def get_context_data(self, **kwargs):
		# context = super(printbarcodetext, self).get_context_data(**kwargs)
		# context['object'] = self.get_object()
		# return context
	
	# def get_initial(self):
		# return {'buyer':self.b, 'user': self.request.user}
	
	# def get_form(self, form_class=None):
		# if form_class is None:
			# form_class = self.get_form_class()
			# form = super(printbarcodetext, self).get_form(form_class)
			# form.fields['saveonclose'].widget=forms.HiddenInput()
			# return form
		# return form_class(**self.get_form_kwargs())
	
	# def form_valid(self, form):
		# self.object = form.save(commit=False)
		# # self.object.user = self.request.user
		# # self.object.save()
		# if form.cleaned_data['saveonclose'] == 'true':
			# self.saveonclose = True
		# return super(printbarcodetext, self).form_valid(form)
		
	#def form_invalid(self, form):
		#print form.errors
	#	return super(printbarcodetext, self).form_invalid(form)
