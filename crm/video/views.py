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
from django.utils import timezone


from django.db.models import Max, Sum, Count
from django.db.models import Q, F

from ckeditor.widgets import CKEditorWidget

from dj.views import *

from django.core.mail import send_mail

import csv

from node.templatetags.nodetag import *

from node.models import *
from .models import *

from device.models import *

import logging
log = logging.getLogger(__name__)

#показ товара по штрихкоду
class video_select(ListView):
	template_name = 'video_select.html'
	model = shopset
	#paginate_by = 10
	
	def dispatch(self, request, *args, **kwargs):
		return super(video_select, self).dispatch(request, *args, **kwargs)

	def get_queryset(self):
		data=super(video_select, self).get_queryset()
		data=data.all()
		if 'id' in self.request.GET:
			data=data.filter(id=self.request.GET['id'])
		return data
	
	def get_context_data(self, *args, **kwargs):
		context_data = super(video_select, self).get_context_data(*args, **kwargs)
		return context_data


class Form_video_show_barcode(forms.Form):
	barcode = forms.CharField(label='Штрих код', help_text='Работа со сканером шрих кода', widget=forms.NumberInput(attrs={'class': 'form-control','autocomplete': 'off',}), max_length=100, required=True)
	
	id = forms.CharField(label='id', widget=forms.HiddenInput(), max_length=100, required=False)


#@method_decorator(permission_required('video.video_show'), name='dispatch')
class video_show(ListView):
	template_name = 'video_show.html'
	model = goods
	#success_url = '/inv/list/'
	#form_class = Form_video_show_barcode
	#paginate_by = 10
	
	def dispatch(self, request, *args, **kwargs):
		self.screen=get_object_or_404(device, id=self.kwargs['pk'])
		return super(video_show, self).dispatch(request, *args, **kwargs)

		
	def get_queryset(self):
		data=super(video_show, self).get_queryset()
		
		data=data.all() #выбираем основной запрос
		
		f=Form_video_show_barcode(self.request.GET)
		
		
		req = ''
		
		self.barcode = None
		
		if f.is_valid():
			fdata = f.cleaned_data
			#фильтрация	
			if fdata['barcode']:
				self.barcode = fdata['barcode'].strip()
				req = '%s&barcode=%s' % (req, self.barcode)
				data=data.filter(Q(barcodelist__barcode__search=self.barcode) | Q(barcodelist__barcode__icontains=self.barcode))
		else:
			data=None
		
		self.req = req
		pdata = data
		self.data = pdata
		return pdata	
		
		
	# def get_success_url(self):
		# url = '/inv/list/%s/#1' % (self.data.id)
		# #url = reverse('panel:saveonclose')
		# return url
		
	# def form_valid(self, form):
		# data = invitem()
		# data.barcode = form.cleaned_data['barcode']
		# invlist
		# #self.object = form.save(commit=False)
		# #form.cleaned_data['saveonclose']
		# # self.object.user = self.request.user
		# # self.object.save()
		
		# print form
		# return super(video_show, self).form_valid(form)
		
	# def form_invalid(self, form):
		# print form.errors
		# return super(video_show, self).form_invalid(form)
			
	def get_context_data(self, *args, **kwargs):
		context_data = super(video_show, self).get_context_data(*args, **kwargs)
		#context_data.update({'next': '/inv/list/%s' % self.data.id})
		context_data.update({'barcode': self.barcode})
		context_data.update({'data': self.data})
		

		context_data.update({'req': self.req,})
		context_data.update({'form': Form_video_show_barcode(self.request.GET)})
		
		context_data.update({'screen': self.screen})
		
		return context_data


#показ видео через планшет или PC
class video_select_pc(ListView):
	template_name = 'video_select_pc.html'
	model = shopset
	#paginate_by = 10
	
	def dispatch(self, request, *args, **kwargs):
		return super(video_select_pc, self).dispatch(request, *args, **kwargs)

	def get_queryset(self):
		data=super(video_select_pc, self).get_queryset()
		data=data.all()
		if 'id' in self.request.GET:
			data=data.filter(id=self.request.GET['id'])
		return data
	
	def get_context_data(self, *args, **kwargs):
		context_data = super(video_select_pc, self).get_context_data(*args, **kwargs)
		return context_data


class Form_video_show_pc(forms.Form):
	q = forms.CharField(label='Поиск', help_text='Введите слово для поиска', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'off'}), max_length=100, required=False)


#@method_decorator(permission_required('video.video_show_pc'), name='dispatch')
class video_show_pc(ListView):
	template_name = 'video_show_pc.html'
	model = goods
	#success_url = '/inv/list/'
	#form_class = Form_video_show_pc
	#paginate_by = 10
	
	def dispatch(self, request, *args, **kwargs):
		self.screen=get_object_or_404(device, id=self.kwargs['pk'])
		return super(video_show_pc, self).dispatch(request, *args, **kwargs)

	def get_queryset(self):
		data=super(video_show_pc, self).get_queryset()
		
		data=data.all() #выбираем основной запрос
		data=data.filter(base__id=1, status=True, showondemo=True).order_by('bname')
		
		f=Form_video_show_pc(self.request.GET)
		
		
		req = ''
		
		self.barcode = None
		
		if f.is_valid():
			fdata = f.cleaned_data
			#фильтрация	
			if fdata['q']:
				req = '%s&q=%s' % (req, fdata['q'])
				data=data.filter(Q(id__icontains=fdata['q']) | Q(id1c__icontains=fdata['q']) | Q(idbitrix__icontains=fdata['q']) | Q(name__icontains=fdata['q']) | Q(name__search=fdata['q']) | Q(namefull__search=fdata['q']) | Q(namefull__icontains=fdata['q']) | Q(art__icontains=fdata['q']) | Q(bname__search=fdata['q']) | Q(bname__icontains=fdata['q']))

		#сортировка
		try:
			self.request.GET['sort']
		except:
			pass
		else:
			if self.request.GET['sort'] == 'bname':
				data=data.order_by('bname')
			if self.request.GET['sort'] == 'price':
				data=data.order_by('price')

		self.req = req
		pdata = data
		self.data = pdata
		return pdata
		
	# def get_success_url(self):
		# url = '/inv/list/%s/#1' % (self.data.id)
		# #url = reverse('panel:saveonclose')
		# return url
		
	# def form_valid(self, form):
		# data = invitem()
		# data.barcode = form.cleaned_data['barcode']
		# invlist
		# #self.object = form.save(commit=False)
		# #form.cleaned_data['saveonclose']
		# # self.object.user = self.request.user
		# # self.object.save()
		
		# print form
		# return super(video_show_pc, self).form_valid(form)
		
	# def form_invalid(self, form):
		# print form.errors
		# return super(video_show_pc, self).form_invalid(form)
			
	def get_context_data(self, *args, **kwargs):
		context_data = super(video_show_pc, self).get_context_data(*args, **kwargs)
		#context_data.update({'next': '/inv/list/%s' % self.data.id})
		context_data.update({'req': self.req,})
		context_data.update({'form': Form_video_show_pc(self.request.GET)})
		context_data.update({'screen': self.screen})
		return context_data




		
		
# #@csrf_exempt
# @permission_required('inventory.add_invitem')
# def invitem_add(request, pk, barcode, col):
	# if request.method == 'GET':
		# next = request.GET.get('next', '/inv/list/')
		# try:
			# invl = invlist.objects.get(id=pk)
		# except:
			# return HttpResponseRedirect(next)
	
		# try:
			# data = goods.objects.get(barcodelist__barcode=barcode)
		# except:
			# return HttpResponseRedirect(next)
		# else:
			# try:
				# i=invitem.objects.get(invlist=invl, goods=data, barcode=barcode)
			# except:
				# i = invitem()
				# i.invlist = invl
				# i.goods = data
				# i.barcode = barcode
				# i.col = int(col)
				# #i.lifedate = datetime.datetime.now() #timezone.now
				# i.save()
			# else:
				# i.col = i.col+int(col)
				# i.save()

			# return HttpResponseRedirect('%s#item%s' % (next, i.id))
	# return HttpResponseRedirect('/')
		

# @method_decorator(permission_required('inventory.add_invitem'), name='dispatch')
# class invitem_del(DeleteView):
	# model = invitem
	# template_name = 'inv_confirm_delete.html'
	# success_url = '/inv/list/'

	# def dispatch(self, request, *args, **kwargs):
		# self.data = get_object_or_404(self.model,id=self.kwargs['pk'])
		# self.next = request.GET.get('next', '/inv/list/')
		# return super(invitem_del, self).dispatch(request, *args, **kwargs)
	
	# #def get_object(self, queryset=None):
	# #	return get_object_or_404(self.model, id=self.kwargs['pk'])
		
	# def get_success_url(self):
		# return self.next
	
	# def get_context_data(self, **kwargs):
		# context = super(invitem_del, self).get_context_data(**kwargs)
		# context['object'] = self.data
		# context['msg'] = u'Вы уверены что хотите удалить '
		# context['back_url'] = self.next
		# return context	
		
		
		
# @method_decorator(permission_required('inventory.add_invitem'), name='dispatch')
# class invitem_edit(UpdateView):
	# model = invitem
	# template_name = 'invitem_edit.html'
	# success_url = '/goods/list'
	# #form_class = Form_goods_edit
	# fields = ['barcode', 'col', 'lifedate',]
	
	# def dispatch(self, request, *args, **kwargs):
		# self.data = get_object_or_404(self.model, id=self.kwargs['pk'])
		# self.next = request.GET.get('next', '/inv/list/')
		# return super(invitem_edit, self).dispatch(request, *args, **kwargs)
	
	# def get_success_url(self):
		# return self.next
	
	# def get_context_data(self, **kwargs):
		# context = super(invitem_edit, self).get_context_data(**kwargs)
		# context['object'] = self.get_object()
		# context['next'] = self.next
		# return context
	
	# # def get_initial(self):
		# # return {'buyer':self.b, 'user': self.request.user}
	
	# def get_form(self, form_class=None):
		# if form_class is None:
			# form_class = self.get_form_class()
			# form = super(invitem_edit, self).get_form(form_class)
			# form.fields['lifedate'].widget=forms.TextInput(attrs={'onKeyDown':'imputmoddate(event, this);'})
			# return form
		# return form_class(**self.get_form_kwargs())
	
	# # def form_valid(self, form):
		# # self.object = form.save(commit=False)
		# # # self.object.user = self.request.user
		# # # self.object.save()
		# # if form.cleaned_data['saveonclose'] == 'true':
			# # self.saveonclose = True
		# # return super(invitem_edit, self).form_valid(form)
		
	# #def form_invalid(self, form):
		# #print form.errors
	# #	return super(invitem_edit, self).form_invalid(form)
		
			
		
# @permission_required('inventory.add_invitem')
# def invitem_csv(request, pk):
	# response = HttpResponse(content_type='text/csv')
	# response['Content-Disposition'] = 'attachment; filename="%s.csv"' % id_generator()

	# data = get_object_or_404(invlist, id=pk)
	
	# dataitem = invitem.objects.filter(invlist=data)
	
	# writer = csv.writer(response, delimiter=str(';'), quotechar=str('"'), quoting=csv.QUOTE_MINIMAL)
	# writer.writerow(['name', 'id', 'barcode', 'lifedate', 'col'])
	# for i in dataitem:
		# lifedate = 'none'
		# if i.lifedate:
			# lifedate=i.lifedate.strftime("%d.%m.%Y")
		# writer.writerow([i.goods.name.encode('cp1251'), i.goods.id1c.encode('cp1251'), i.barcode, lifedate, i.col])

	# return response

	
	
