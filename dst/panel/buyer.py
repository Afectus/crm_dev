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


from django.db.models import Min, Max, Sum, Count, Avg, Q, F, Func, Value, IntegerField, FloatField, CharField, Case, When, ExpressionWrapper

from django.db.models.functions import Cast, Coalesce, Trunc, TruncMonth, ExtractYear, ExtractMonth, ExtractWeek, ExtractWeekDay, ExtractDay

from pg_utils import DistinctSum

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


class Form_filter_buyer(forms.Form):
	q = forms.CharField(label='Поиск', help_text='Введите слово для поиска', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'off'}), max_length=100, required=False)
	
	dm = forms.BooleanField(label="Фильтр только день и месяц (игнорировать год)", required=False, initial=True,)
	
	bdstart = forms.DateField(label="Д.Р. Старт", help_text='День рождения от', input_formats=['%d-%m-%y', '%d-%m-%Y',], required=False, widget=forms.TextInput(attrs={'class':'form-control datepicker',  'data-dateformat': "dd-mm-yy"}))
	bdend = forms.DateField(label="Д.Р. Конец", help_text='День рождения до', input_formats=['%d-%m-%y', '%d-%m-%Y',], required=False, widget=forms.TextInput(attrs={'class':'form-control datepicker',	 'data-dateformat': "dd-mm-yy"}))
	
	
	#checkdatedm = forms.BooleanField(label="Фильтр только день и месяц (игнорировать год)", required=False, initial=True,)
	checkdatestart = forms.DateField(label="Чек Старт", help_text='Чек дата от', input_formats=['%d-%m-%y', '%d-%m-%Y',], required=False, widget=forms.TextInput(attrs={'class':'form-control datepicker', 'data-dateformat': "dd-mm-yy"}))
	checkdateend = forms.DateField(label="Чек Конец", help_text='Чек дата до', input_formats=['%d-%m-%y', '%d-%m-%Y',], required=False, widget=forms.TextInput(attrs={'class':'form-control datepicker', 'data-dateformat': "dd-mm-yy"}))
	
	
	#отсутствие покупок за период
	#nocheckdatestart = forms.DateField(label="Отсутствие покупок от", help_text='Отсутствие покупок от', input_formats=['%d-%m-%y', '%d-%m-%Y',], required=False, widget=forms.TextInput(attrs={'class':'form-control datepicker', 'data-dateformat': "dd-mm-yy"}))
	#nocheckdateend = forms.DateField(label="Отсутствие покупок до", help_text='Отсутствие покупок до', input_formats=['%d-%m-%y', '%d-%m-%Y',], required=False, widget=forms.TextInput(attrs={'class':'form-control datepicker', 'data-dateformat': "dd-mm-yy"}))
	#
	
	sumfrom = forms.FloatField(label="Сумма чеков от", required=False,)
	sumto = forms.FloatField(label="сумма чеков до", required=False,)
	
	sort = forms.ChoiceField(label='Сортировка', help_text='Сортировать по полю', widget=forms.Select(attrs={'class': 'form-control'}), choices=(('id', 'id'),('bday', 'Д. Рождения'),('f', 'Фамилия'),('i', 'Имя'),('o', 'Отчество')), required=False)
	
	bonusfrom = forms.FloatField(label="Количество бонусов от", required=False,)
	bonusto = forms.FloatField(label="Количество бонусов до", required=False,)
	
	#согласие на рассылку
	adv = forms.ChoiceField(label='Согласие на рассылку', widget=forms.Select(attrs={'class': 'form-control'}), choices=(('all', 'Все'),('true', 'Да'),('false', 'Нет'),), initial='all', required=False)
	
	anketa = forms.ChoiceField(label='Анкета', widget=forms.Select(attrs={'class': 'form-control'}), choices=(('all', 'Все'),('true', 'Да'),('false', 'Нет'),), initial='all', required=False)
	
	dcard = forms.CharField(label='Дисконтная карта', help_text='Дисконтная карта', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'off'}), max_length=100, required=False)
	
	withphone = forms.BooleanField(label="Покупатели с телефонами", required=False, initial=False,)
	
	exportjson = forms.BooleanField(label="Экспорт в json", required=False, initial=False,)

	
@method_decorator(permission_required('node.add_buyer'), name='dispatch')
class buyer_list(ListView):
	template_name = 'buyer_list.html'
	model = buyer
	#paginate_by = 10
	
	def dispatch(self, request, *args, **kwargs):
		return super(buyer_list, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(buyer_list, self).get_queryset()
		
		data=data.all() #выбираем основной запрос

		f=Form_filter_buyer(self.request.GET)
		
		
		req = ''
		
		if f.is_valid():
			fdata = f.cleaned_data
			####################################
			#по отсутствии покупок чеков
			if fdata['checkdatestart'] and fdata['checkdateend']:
				req = '%s&checkdatestart=%s' % (req, self.request.GET['checkdatestart'])
				req = '%s&checkdateend=%s' % (req, self.request.GET['checkdateend'])

				data = data.filter(check__time__range=(fdata['checkdatestart'], fdata['checkdateend']))

				# data=data.values('id')
				# data = buyer.objects.exclude(id__in=data)
				data = data.annotate(bonussum=DistinctSum('discountcard__bonus'))
			else:
				data = data.annotate(bonussum=DistinctSum('discountcard__bonus'))
			########################
			
			
			#фильтрация
			if fdata['q']:
				req = '%s&q=%s' % (req, fdata['q'])
				data=data.filter(Q(id__icontains=fdata['q']) | Q(id1c__icontains=fdata['q']) | Q(phone__icontains=fdata['q']) | Q(f__search=fdata['q']) | Q(i__icontains=fdata['q']) | Q(o__icontains=fdata['q']))
			
			if fdata['bdstart'] and fdata['bdend']:
				req = '%s&bdstart=%s' % (req, self.request.GET['bdstart'])
				req = '%s&bdend=%s' % (req, self.request.GET['bdend'])
				if fdata['dm'] == True: #фильтр только день месяц, игнорировать год
					req = '%s&dm=%s' % (req, self.request.GET['dm'])
					s = fdata['bdstart']
					e = fdata['bdend']
					count = (e-s).days
					count=count+1
					dlist = []
					for x in range(0, count):
						dlist.append(s + datetime.timedelta(days=x))
					dindex = []
					for date in dlist:
						dindex.append(date.strftime("%d%m")) 
					data=data.filter(bdayindex__in=dindex)	 
				else: #полный фильтр день месяц год
					data=data.filter(bday__range=(fdata['bdstart'], fdata['bdend']))

			if fdata['sort']:
				req = '%s&sort=%s' % (req, self.request.GET['sort'])
				data=data.order_by(fdata['sort'])
	
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
					
			if fdata['dcard']:
				req = '%s&dcard=%s' % (req, fdata['dcard'])
				data=data.filter(discountcard__name__icontains=fdata['dcard'])
				
			if fdata['withphone'] == True:
				req = '%s&withphone=%s' % (req, self.request.GET['withphone'])
				data=data.exclude(phone='')
			
			#
			
			if fdata['bonusfrom'] or fdata['bonusto']:
				req = '%s&bonusfrom=%s' % (req, fdata['bonusfrom'])
				req = '%s&bonusto=%s' % (req, fdata['bonusto'])
			if fdata['bonusfrom']: #бонусы gte больше или равно
				data=data.filter(bonussum__gte=fdata['bonusfrom'])
			if fdata['bonusto']: #бонусы lte маньше или равно
				data=data.filter(bonussum__lte=fdata['bonusto'])

			data=data.values('id', 'id1c', 'phone', 'adv', 'f', 'i', 'o', 'bday', 'anketa', 'sex','bonussum', )
		else:
			data=data.values('id', 'id1c', 'phone', 'adv', 'f', 'i', 'o', 'bday', 'anketa', 'sex',)
		
		self.totalsum = data.aggregate(s=Sum('check__checkitem__sum'))['s']
		
		
		self.req = req
		
		#paginator
		self.p = Paginator(data, 40)
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
			
		#экспорт #НЕТ ПАГИНАЦИИ
		self.exportjson=False
		if f.is_valid():
			if fdata['exportjson'] == True:
				self.exportjson=fdata['exportjson']
				return data
		#
		return pdata

		
	def render_to_response(self, context, **response_kwargs):
		if self.exportjson == True:
			data=self.get_queryset()
			jdata=serializers.serialize('json', data, indent=2, fields=('1682','id1c', 'f', 'i', 'o', 'bday', 'sex', 'phone', 'adv', 'anketa',))
			return HttpResponse(jdata, content_type="application/json")
	
		response_kwargs.setdefault('content_type', self.content_type)
		return self.response_class(
			request = self.request,
			template = self.get_template_names(),
			context = context,
			**response_kwargs
		)
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(buyer_list, self).get_context_data(*args, **kwargs)
		
		#self.initial.update({'your_field': self.request.user})
		#if "fio" in self.request.GET:
		#	data=data.filter(i__contains=self.request.GET['fio'])
		context_data.update({'req': self.req,})
		context_data.update({'count': self.p.count,})
		context_data.update({'urlpage': reverse('panel:buyer_list')})
		context_data.update({'form': Form_filter_buyer(self.request.GET),})
		#
		context_data.update({'totalsum': self.totalsum,})
		
		return context_data


# class buyer_list(TemplateView):
	# template_name = 'crm/buyer_list.html'
	
	# def dispatch(self, request, *args, **kwargs):
		# return super(buyer_list, self).dispatch(request, *args, **kwargs)
		
	# def get_context_data(self, *args, **kwargs):
		# context_data = super(buyer_list, self).get_context_data(*args, **kwargs)
		# #context_data.update({'command': True,})
		# return context_data

#использовалось для плагина datatables пока не используется 
class buyer_list_json(ListView):
	template_name = 'buyer_list.html'
	model = buyer
	paginate_by = 2

	#def dispatch(self, request, *args, **kwargs):
	#	if not request.is_ajax():
	#		raise http.Http404("This is an ajax view, friend.")
	#	return super(buyer_list_json, self).dispatch(request, *args, **kwargs)
	
	def get_queryset(self):
		data = super(buyer_list_json, self).get_queryset().all().order_by('-id')
		for i in data:
			i.phone = hidephone(i.phone)
			#print type(i.bday)
			#print dir(i.bday)
			#try:
			#	i.bday = '%s' % i.bday.strftime("%d.%m.%Y")
			#except:
			#	pass
		return data[:1]
	
	def get_context_data(self, *args, **kwargs):
		context_data = super(buyer_list_json, self).get_context_data(*args, **kwargs)
		#context_data.update({'command': True,})
		return context_data

	def get(self, request, *args, **kwargs):
	
		#return HttpResponse(serializers.serialize('json', self.get_queryset(), fields=('id','gethidephone')))
		return HttpResponse(serializers.serialize('json', self.get_queryset()))
		

@method_decorator(permission_required('node.add_buyer'), name='dispatch')
class buyer_detail(DetailView):
	model = buyer
	template_name = 'buyer_detail.html'
	
	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(self.model, id=self.kwargs['pk'])
		return super(buyer_detail, self).dispatch(request, *args, **kwargs)
	
	def get_object(self, queryset=None):
		#self.data = super(buyer_detail, self).get_object(queryset=queryset)
		return self.data

	def get_context_data(self, **kwargs):
		context = super(buyer_detail, self).get_context_data(**kwargs)
		#context['servername'] = self.data.name
		return context
		
		
		
@method_decorator(permission_required('node.add_buyer'), name='dispatch')
class buyer_edit(UpdateView):
	model = buyer
	template_name = 'buyer_edit.html'
	success_url = '/buyer/list'
	fields = ['f', 'i', 'o', 'sex', 'bday', 'bonus', 'anketa', ]
	
	def dispatch(self, request, *args, **kwargs):
		#self.e = get_object_or_404(self.model, id=self.kwargs['pk'], user=request.user) #ПОТОМ ВКЛЮЧИТЬ
		return super(buyer_edit, self).dispatch(request, *args, **kwargs)
	
	def get_success_url(self):
		return '/buyer/edit/%s' % (self.get_object().id)
	
	def get_context_data(self, **kwargs):
		context = super(buyer_edit, self).get_context_data(**kwargs)
		context['object'] = self.get_object()
		return context
	
	# def get_initial(self):
		# return {'buyer':self.b, 'user': self.request.user}
	
	# def get_form(self, form_class):
		# form = super(buyer_edit, self).get_form(form_class)
		# form.fields['buyer'].widget.attrs['readonly'] = True
		# return form
		
		
	# def get_form(self, form_class=None):
		# if form_class is None:
			# form_class = self.get_form_class()
			# form = super(buyer_edit, self).get_form(form_class)
			# form.fields['buyer'].widget=forms.HiddenInput()
			# return form
		# return form_class(**self.get_form_kwargs())
	
	def form_valid(self, form):
		# self.object = form.save(commit=False)
		# self.object.user = self.request.user
		# self.object.save()
		return super(buyer_edit, self).form_valid(form)
		
	#def form_invalid(self, form):
		#print form.errors
	#	return super(buyer_edit, self).form_invalid(form)
		
		
		
		
		

		

#@method_decorator(permission_required('node.add_eventcall'), name='dispatch')
class event_call_list(ListView):
	template_name = 'event_call_list.html'
	model = eventcall
	paginate_by = 20
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'eventcall', 'L')
		return super(event_call_list, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(event_call_list, self).get_queryset()
		#self.data=data.filter(user=self.request.user).order_by('-id')
		self.data=data.all().order_by('-id')
		return self.data
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(event_call_list, self).get_context_data(*args, **kwargs)
		#context_data.update({'command': True,})
		return context_data



#@method_decorator(permission_required('node.add_eventcall'), name='dispatch')
class event_call_add(CreateView):
	model = eventcall
	template_name = 'event_call_add.html'
	success_url = '/event/call/list'
	fields = ['ctime', 'buyer', 'comment',]

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'eventcall', 'L')
		self.b = get_object_or_404(buyer, id=self.kwargs['pk'])
		return super(event_call_add, self).dispatch(request, *args, **kwargs)
	
	#def get_success_url(self):
	#	return '%s/%s' % (self.success_url, self.hashkey)
	
	def get_context_data(self, **kwargs):
		context = super(event_call_add, self).get_context_data(**kwargs)
		context['object'] = self.b
		return context
	
	def get_initial(self):
		return {'buyer':self.b, 'user': self.request.user}
		
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
			form = super(event_call_add, self).get_form(form_class)
			form.fields['buyer'].widget=forms.HiddenInput()
			#form.fields['buyer'].widget.attrs['readonly'] = True
			#form.fields['user'].widget=forms.HiddenInput()
			return form
		return form_class(**self.get_form_kwargs())
	
	def form_valid(self, form):
		#self.object = form.save(commit=False)
		#self.object.user = self.request.user
		#self.object.save()
		return super(event_call_add, self).form_valid(form)
		
	#def form_invalid(self, form):
		#print form.errors
	#	return super(event_call_add, self).form_invalid(form)



#@method_decorator(permission_required('node.add_eventcall'), name='dispatch')
class event_call_edit(UpdateView):
	model = eventcall
	template_name = 'event_call_edit.html'
	success_url = '/event/call/list'
	fields = ['ctime', 'buyer', 'comment',]
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'eventcall', 'L')
		#self.e = get_object_or_404(self.model, id=self.kwargs['pk'], user=request.user) #ПОТОМ ВКЛЮЧИТЬ
		return super(event_call_edit, self).dispatch(request, *args, **kwargs)
	
	#def get_success_url(self):
	#	return '%s/%s' % (self.success_url, self.hashkey)
	
	def get_context_data(self, **kwargs):
		context = super(event_call_edit, self).get_context_data(**kwargs)
		context['object'] = self.get_object()
		return context
	
	# def get_initial(self):
		# return {'buyer':self.b, 'user': self.request.user}
	
	# def get_form(self, form_class):
		# form = super(event_call_edit, self).get_form(form_class)
		# form.fields['buyer'].widget.attrs['readonly'] = True
		# return form
		
		
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
			form = super(event_call_edit, self).get_form(form_class)
			form.fields['buyer'].widget=forms.HiddenInput()
			return form
		return form_class(**self.get_form_kwargs())
	
	def form_valid(self, form):
		# self.object = form.save(commit=False)
		# self.object.user = self.request.user
		# self.object.save()
		return super(event_call_edit, self).form_valid(form)
		
	#def form_invalid(self, form):
		#print form.errors
	#	return super(event_call_edit, self).form_invalid(form)

	

		

		
		
#from node.models import beventtypechoice	
beventtypechoice.append(('all', 'Все'))
class Form_filter_buyerevent(forms.Form):
	q = forms.CharField(label='Поиск', help_text='Введите слово для поиска', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'off'}), max_length=100, required=False)
	
	dm = forms.BooleanField(label="Фильтр только день и месяц (игнорировать год)", required=False, initial=True,)
	
	datestart = forms.DateField(label="Дата старт", input_formats=['%d-%m-%y', '%d-%m-%Y',], required=False, widget=forms.TextInput(attrs={'class':'mydatepicker1'}))
	dateend = forms.DateField(label="Дата конец", input_formats=['%d-%m-%y', '%d-%m-%Y',], required=False, widget=forms.TextInput(attrs={'class':'mydatepicker1'}))
	
	type = forms.ChoiceField(label='Тип события', help_text='Тип события', widget=forms.Select(attrs={'class': 'form-control'}), choices=beventtypechoice, required=False, initial='all')


@method_decorator(permission_required('node.add_buyerevent'), name='dispatch')
class buyerevent_list(ListView):
	template_name = 'buyerevent_list.html'
	model = buyerevent
	#paginate_by = 20
	
	def dispatch(self, request, *args, **kwargs):
		if "datestart" not in request.GET:
			startdate = datetime.datetime.now() + datetime.timedelta(days=-30)
			enddate = datetime.datetime.now() + datetime.timedelta(days=30)
			return HttpResponseRedirect('/buyerevent/list/1/?datestart=%s&dateend=%s' % (startdate.strftime('%d-%m-%Y'), enddate.strftime('%d-%m-%Y')))
		return super(buyerevent_list, self).dispatch(request, *args, **kwargs)
	
	def get_queryset(self):
		data=super(buyerevent_list, self).get_queryset()
		
		#data=data.all() #выбираем основной запрос
		
		f=Form_filter_buyerevent(self.request.GET, initial={'type': 'all'})
		
		
		req = ''
		
		if f.is_valid():
			fdata = f.cleaned_data
			#фильтрация
			if fdata['q']:
				req = '%s&q=%s' % (req, fdata['q'])
				data=data.filter(Q(name__search=fdata['q']) | Q(comment__search=fdata['q']))
			
			if fdata['datestart'] and fdata['dateend']:
				req = '%s&datestart=%s' % (req, self.request.GET['datestart'])
				req = '%s&dateend=%s' % (req, self.request.GET['dateend'])
				if fdata['dm'] == True: #фильтр только день месяц, игнорировать год
					req = '%s&dm=%s' % (req, self.request.GET['dm'])
					s = fdata['datestart']
					e = fdata['dateend']
					count = (e-s).days
					count=count+1
					dlist = []
					for x in range(0, count):
						dlist.append(s + datetime.timedelta(days=x))
					dindex = []
					for date in dlist:
						dindex.append(date.strftime("%d%m")) 
					data=data.filter(stimeindex__in=dindex)	 
				else: #полный фильтр день месяц год
					data=data.filter(stime__range=(fdata['datestart'], fdata['dateend']))
					
			if fdata['type']:
				req = '%s&type=%s' % (req, fdata['type'])
				if fdata['type'] != 'all':
					data=data.filter(type=fdata['type'])
			
		self.req = req
			
		#data=data.order_by('-id')

		
		#paginator
		self.p = Paginator(data, 20)
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
		context_data = super(buyerevent_list, self).get_context_data(*args, **kwargs)
		context_data.update({'req': self.req,})
		context_data.update({'count': self.p.count,})
		context_data.update({'form': Form_filter_buyerevent(self.request.GET, initial={'type': 'all'}),})
		return context_data



@method_decorator(permission_required('node.add_buyerevent'), name='dispatch')
class buyerevent_add(CreateView):
	model = buyerevent
	template_name = 'buyerevent_add.html'
	success_url = '/buyerevent/list'
	fields = ['buyer', 'stime', 'type', 'name', 'comment',]

	def dispatch(self, request, *args, **kwargs):
		self.b = get_object_or_404(buyer, id=self.kwargs['pk'])
		return super(buyerevent_add, self).dispatch(request, *args, **kwargs)
	
	def get_success_url(self):
		return '/buyer/detail/%s' % (self.b.id)
	
	def get_context_data(self, **kwargs):
		context = super(buyerevent_add, self).get_context_data(**kwargs)
		context['object'] = self.b
		return context
	
	def get_initial(self):
		return {'buyer':self.b,}
		
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
			form = super(buyerevent_add, self).get_form(form_class)
			form.fields['buyer'].widget=forms.HiddenInput()
			#form.fields['buyer'].widget.attrs['readonly'] = True
			#form.fields['user'].widget=forms.HiddenInput()
			return form
		return form_class(**self.get_form_kwargs())
	
	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.save()
		return super(buyerevent_add, self).form_valid(form)


@method_decorator(permission_required('node.add_buyerevent'), name='dispatch')
class buyerevent_edit(UpdateView):
	model = buyerevent
	template_name = 'buyerevent_edit.html'
	success_url = '/panel/buyerevent/list'
	fields = ['stime', 'type', 'name', 'comment',]
	
	def dispatch(self, request, *args, **kwargs):
		#self.b = get_object_or_404(self.model, id=self.kwargs['pk'], user=request.user)
		return super(buyerevent_edit, self).dispatch(request, *args, **kwargs)
	
	def get_success_url(self):
		return '/buyerevent/edit/%s' % (self.get_object().id)
	
	def get_context_data(self, **kwargs):
		context = super(buyerevent_edit, self).get_context_data(**kwargs)
		context['object'] = self.get_object()
		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.save()
		return super(buyerevent_edit, self).form_valid(form)


