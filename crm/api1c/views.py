# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.http import HttpResponsePermanentRedirect

from django.core.exceptions import PermissionDenied


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
from django.utils import timezone

from django.db.models import Sum, Count
from django.db.models import Q

from django.urls import reverse
from urllib.parse import urljoin

from django import forms

from django.views.decorators.csrf import csrf_exempt

#from node.templatetags.nodetags import node_count

from node.models import *
from dj.views import *

from .func import *

import logging
log = logging.getLogger(__name__)


def validate_phone_9(value):
	p = re.compile('^9[0-9]{9}$')
	if not p.match(value):
		raise ValidationError(u'формат телефона 9XXXXXXXXX. ')
	#try:
	#	data=buyer.objects.get(phone=value)
	#except:
	#	raise ValidationError(u'Номер %s не зарегистрирован. ' % value)
	

class Form_1c_getcard(forms.Form):
	phone = forms.CharField(label='Номер телефона', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'on'}), min_length=10, max_length=10, required=False, validators=[validate_phone_9])
	
	card = forms.CharField(label='Номер карты', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'on'}), min_length=1, max_length=300, required=False)
	
	fio = forms.CharField(label='Фио', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'on'}), min_length=1, max_length=300, required=False)
	
class form_1c_getcard(ListView):
	model = buyer
	#form_class = Form_1c_getcard
	template_name = 'form_1c_getcard.html'
	#form_class = Form_create_nickname
	success_url = '/form/1c/getcard/?success=true'
	#fields = ['name', 'message', ]
	#data=None
	crc=None
	salt=None
	
	def dispatch(self, request, *args, **kwargs):
		#http://crm.babah24.ru/form/1c/getcard/?salt=123456&crc=EFA645BF3AC5297469EB61B4E0369B89&phone=9021618482&card=&fio=
		if 'salt' in request.GET:
			crc = makeapitoken_1c(request.GET['salt'])
			if crc.lower() == request.GET['crc'].lower():
				self.salt = id_generator()
				self.crc = crc = makeapitoken_1c(self.salt)
				return super(form_1c_getcard, self).dispatch(request, *args, **kwargs)
		return HttpResponseNotFound('<h1>Access denied</h1>')
		
	#def get_success_url(self):
	#	return '/worktask/detail/%s' % (self.data.id)
	
	def get_queryset(self):
		data=super(form_1c_getcard, self).get_queryset()
		data=data.none()
		f=Form_1c_getcard(self.request.GET)
		#print f
		#print dir(f)
		if f.is_valid():
			fdata = f.cleaned_data
			if fdata['phone']:
				data=super(form_1c_getcard, self).get_queryset()
				data=data.filter(phone=fdata['phone'])
			elif fdata['card']:
				data=super(form_1c_getcard, self).get_queryset()
				data=data.filter(Q(discountcard__name=fdata['card']) | Q(discountcard__id1c=fdata['card']))
			elif fdata['fio']:
				data=super(form_1c_getcard, self).get_queryset()
				data=data.filter(Q(f__icontains=fdata['fio']) | Q(f__search=fdata['fio']) | Q(i__icontains=fdata['fio']) | Q(i__search=fdata['fio']) | Q(o__icontains=fdata['fio']) | Q(o__search=fdata['fio']))
		return data	
		
	
	# def form_valid(self, form):
		# #instance = form.save(commit=False)
		# #instance.user = self.request.user
		# #instance.save()
		# #self.data = instance
		# fdata = form.cleaned_data
		# print fdata['phone'], fdata['card']
		# if form.is_valid():
			# self.data=buyer.objects.filter(phone=fdata['phone'])
			# print self.data
		
		
		#return super(form_1c_getcard, self).form_valid(form)
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(form_1c_getcard, self).get_context_data(*args, **kwargs)
		context_data.update({'form': Form_1c_getcard(self.request.GET)})
		#context_data.update({'data': self.data,})
		#
		context_data.update({'salt': self.salt,})
		context_data.update({'crc': self.crc,})
		return context_data		
		
		
	
		
class Form_1c_makecard(forms.Form):
	seller = forms.CharField(label='Кассир', widget=forms.TextInput(attrs={'class': 'form-control'}), min_length=1, max_length=300, required=True, initial='0')
	
	#shop = forms.CharField(label='Магазин', widget=forms.TextInput(attrs={'class': 'form-control'}), min_length=1, max_length=300, required=True)
	#cashbox = forms.CharField(label='Касса', widget=forms.TextInput(attrs={'class': 'form-control'}), min_length=1, max_length=300, required=True)

	phone = forms.CharField(label='Номер телефона', help_text='9XXXXXXXXX', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'on'}), min_length=10, max_length=10, required=True, validators=[validate_phone_9])
	
	f = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'on'}), min_length=1, max_length=300, required=True)
	
	i = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'on'}), min_length=1, max_length=300, required=True)
	
	o = forms.CharField(label='Отчество', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'on'}), min_length=1, max_length=300, required=True)
	
	bday = forms.DateField(label="Дата рождения", help_text='дд-мм-гггг, дд/мм/гггг, дд.мм.гггг', input_formats=['%d-%m-%y', '%d/%m/%y', '%d.%m.%y', '%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y',], required=True, widget=forms.TextInput(attrs={'class':'form-control'}),)
	
	sex = forms.ChoiceField(label='Пол', widget=forms.Select(attrs={'class': 'form-control'}), choices=(('male', 'Мужской'), ('female', 'Женский')))

	#согласие на рассылку
	adv = forms.BooleanField(label='Согласие на рассылку', widget=forms.CheckboxInput(attrs={'class': 'form-control_DISABLE'}), required=False, initial=False)
	
	card = forms.CharField(label='Номер карты', widget=forms.TextInput(attrs={'class': 'form-control',}), min_length=1, max_length=50, required=True)

	
class form_1c_makecard(FormView):
	#model = buyer
	form_class = Form_1c_makecard
	template_name = 'form_1c_makecard.html'
	success_url = '/form/1c/makecard/?salt=123456&crc=EFA645BF3AC5297469EB61B4E0369B89&success=true'
	#fields = ['name', 'message', ]
	bdata=False
	crc=None
	salt=None
	
	def dispatch(self, request, *args, **kwargs):
		log.info('start=form_1c_makecard')
		log.info('bdata=%s' % self.bdata)
		#
		#http://crm.babah24.ru/form/1c/makecard/?salt=123456&crc=EFA645BF3AC5297469EB61B4E0369B89
		if 'salt' in request.GET:
			crc = makeapitoken_1c(request.GET['salt'])
			if crc.lower() == request.GET['crc'].lower():
				self.salt = id_generator()
				self.crc = crc = makeapitoken_1c(self.salt)
				return super(form_1c_makecard, self).dispatch(request, *args, **kwargs)
		return HttpResponseNotFound('<h1>Access denied</h1>')
		#return super(form_1c_makecard, self).dispatch(request, *args, **kwargs)
		
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
			form = super(form_1c_makecard, self).get_form(form_class)
			#form.fields['phone'].initial='9021618481'
			#form.fields['bday'].initial='20.10.17'
			#form.fields['f'].initial='delete'
			#form.fields['i'].initial='удалить'
			#form.fields['o'].initial='delete'
			#form.fields['card'].initial='111111'
			#form.fields['seller'].widget=forms.HiddenInput()
			form.fields['seller'].widget.attrs['readonly'] = True
			
			return form
		return form_class(**self.get_form_kwargs())
	
	# def get(self, request, *args, **kwargs):
			# if form.is_valid():
		# return self.render_to_response(self.get_context_data(form=form))
	
	def form_valid(self, form):
		log.info('form_valid=%s' % True)
		fdata = form.cleaned_data
		#check buyer by phone
		b=buyer.objects.filter(phone=form.cleaned_data['phone'])
		if b.exists():
			log.info('buyer=%s' % b)
			self.bdata=b
			return HttpResponseRedirect('http://crm.babah24.ru/form/1c/getcard/?salt=%s&crc=%s&phone=%s&message=exist' % (self.salt, self.crc, b.first().phone))
		
		id1c_tmp=id1c_generator()

		b=buyer.objects.create(id1c='BU%s' % (id1c_tmp), phone=fdata['phone'], bday=fdata['bday'], sex=fdata['sex'], adv=fdata['adv'], f=fdata['f'], i=fdata['i'], o=fdata['o'], creator=fdata['seller'], lastmod=fdata['seller'], lastmodtime=timezone.now)
		
		d=discountcard.objects.create(id1c='DC%s' % (id1c_tmp), name=fdata['card'], buyer=b)
		
		self.bdata=b
		
		#instance = form.save(commit=False)
		#instance.user = self.request.user
		#instance.save()
		#self.data = instance
		#fdata = form.cleaned_data
		

		log.info('bdata=%s' % self.bdata)
		
		return super(form_1c_makecard, self).form_valid(form)
		
	def get_success_url(self):
		return 'http://crm.babah24.ru/form/1c/detailcard/%s/?salt=%s&crc=%s&message=make' % (self.bdata.id, self.salt, self.crc)
		#return 'http://crm.babah24.ru/form/1c/relcard/%s/?salt=%s&crc=%s' % (self.bdata.id, self.salt, self.crc)
		
	def get_context_data(self, *args, **kwargs):
		log.info('get_context_data=%s' % 'start')
		context_data = super(form_1c_makecard, self).get_context_data(*args, **kwargs)
		#context_data.update({'form': Form_1c_makecard()})
		context_data.update({'bdata': self.bdata,})
		#
		context_data.update({'salt': self.salt,})
		context_data.update({'crc': self.crc,})
		return context_data
		
		
		
class form_1c_detailcard(DetailView):
	model = buyer
	template_name = 'form_1c_detailcard.html'
	crc=None
	salt=None
	
	def dispatch(self, request, *args, **kwargs):
		log.info('start=form_1c_detailcard')
		#http://crm.babah24.ru/form/1c/makecard/?salt=123456&crc=EFA645BF3AC5297469EB61B4E0369B89
		if 'salt' in request.GET:
			crc = makeapitoken_1c(request.GET['salt'])
			if crc.lower() == request.GET['crc'].lower():
				self.salt = id_generator()
				self.crc = crc = makeapitoken_1c(self.salt)
				return super(form_1c_detailcard, self).dispatch(request, *args, **kwargs)
		return HttpResponseNotFound('<h1>Access denied</h1>')
		#return super(form_1c_detailcard, self).dispatch(request, *args, **kwargs)
		
	def get_object(self, queryset=None):
		self.data=super(form_1c_detailcard, self).get_object()
		return self.data
		
	def get_context_data(self, *args, **kwargs):
		log.info('get_context_data=%s' % 'start')
		context_data = super(form_1c_detailcard, self).get_context_data(*args, **kwargs)
		#
		context_data.update({'salt': self.salt,})
		context_data.update({'crc': self.crc,})
		context_data.update({'next': 'http://crm.babah24.ru/form/1c/relcard/%s/?salt=%s&crc=%s' % (self.data.id, self.salt, self.crc),})
		
		return context_data		

		
		
class Form_1c_editcard(forms.ModelForm):
	seller = forms.CharField(label='Кассир', widget=forms.TextInput(attrs={'class': 'form-control'}), min_length=1, max_length=300, required=True, initial='0')
	#shop = forms.CharField(label='Магазин', widget=forms.TextInput(attrs={'class': 'form-control'}), min_length=1, max_length=300, required=True)
	#cashbox = forms.CharField(label='Касса', widget=forms.TextInput(attrs={'class': 'form-control'}), min_length=1, max_length=300, required=True)

	class Meta:
		model = buyer
		fields = ['phone', 'f', 'i', 'o', 'bday', 'sex', 'adv']

class form_1c_editcard(UpdateView):
	model = buyer
	form_class = Form_1c_editcard
	template_name = 'form_1c_editcard.html'
	success_url = '/form/1c/getcard/?salt=123456&crc=EFA645BF3AC5297469EB61B4E0369B89&success=true'
	#fields = ['phone', 'f', 'i', 'o', 'bday', 'sex', 'adv']
	crc=None
	salt=None
	
	def dispatch(self, request, *args, **kwargs):
		log.info('start=form_1c_editcard')
		#http://crm.babah24.ru/form/1c/makecard/?salt=123456&crc=EFA645BF3AC5297469EB61B4E0369B89
		if 'salt' in request.GET:
			crc = makeapitoken_1c(request.GET['salt'])
			if crc.lower() == request.GET['crc'].lower():
				self.salt = id_generator()
				self.crc = crc = makeapitoken_1c(self.salt)
				return super(form_1c_editcard, self).dispatch(request, *args, **kwargs)
		return HttpResponseNotFound('<h1>Access denied</h1>')
		#return super(form_1c_editcard, self).dispatch(request, *args, **kwargs)
		
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
			form = super(form_1c_editcard, self).get_form(form_class)
			#phone
			form.fields['phone'].widget=forms.TextInput(attrs={'class': 'form-control'}) 
			form.fields['phone'].required=True
			form.fields['phone'].validators=[validate_phone_9]
			#
			form.fields['f'].widget=forms.TextInput(attrs={'class': 'form-control'})
			form.fields['f'].required=True
			form.fields['i'].widget=forms.TextInput(attrs={'class': 'form-control'})
			form.fields['i'].required=True
			form.fields['o'].widget=forms.TextInput(attrs={'class': 'form-control'})
			form.fields['o'].required=True
			#
			form.fields['bday'].widget=forms.TextInput(attrs={'class':'form-control'})
			form.fields['bday'].help_text='дд-мм-гггг, дд/мм/гггг, дд.мм.гггг'
			form.fields['bday'].input_formats=['%d-%m-%y', '%d/%m/%y', '%d.%m.%y', '%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y', '%Y-%m-%d']
			form.fields['bday'].required=True,
			#
			form.fields['sex'].widget=forms.Select(attrs={'class':'form-control'})
			form.fields['sex'].choices=(('male', 'Мужской'), ('female', 'Женский'))
			#
			#form.fields['seller'].widget=forms.HiddenInput()
			form.fields['seller'].widget.attrs['readonly'] = True
			return form
		return form_class(**self.get_form_kwargs())
		
	def get_object(self, queryset=None):
		self.data=super(form_1c_editcard, self).get_object()
		return self.data
		
	def get_success_url(self):
		#return 'http://crm.babah24.ru/form/1c/getcard/?salt=%s&crc=%s&phone=%s&message=update' % (self.salt, self.crc, self.data.phone)def get_success_url(self):
		return 'http://crm.babah24.ru/form/1c/detailcard/%s/?salt=%s&crc=%s&message=make' % (self.data.id, self.salt, self.crc)
		
		

	def form_valid(self, form):
		instance = form.save(commit=False)
		fdata = form.cleaned_data
		instance.lastmod=fdata['seller']
		instance.save()
		return super(form_1c_editcard, self).form_valid(form)

	def get_context_data(self, *args, **kwargs):
		log.info('get_context_data=%s' % 'start')
		context_data = super(form_1c_editcard, self).get_context_data(*args, **kwargs)
		#
		context_data.update({'salt': self.salt,})
		context_data.update({'crc': self.crc,})
		context_data.update({'object': self.data,})
		return context_data
		
	
	
		
class Form_1c_relcard(forms.ModelForm):
	#psave = forms.BooleanField(label='Все равно записать?', help_text='asd', widget=forms.CheckboxInput(attrs={'class': 'form-control1'}), initial=False, required=False)
	seller = forms.CharField(label='Кассир', widget=forms.TextInput(attrs={'class': 'form-control'}), min_length=1, max_length=300, required=True, initial='0')
	#shop = forms.CharField(label='Магазин', widget=forms.TextInput(attrs={'class': 'form-control'}), min_length=1, max_length=300, required=True)
	#cashbox = forms.CharField(label='Касса', widget=forms.TextInput(attrs={'class': 'form-control'}), min_length=1, max_length=300, required=True)

	class Meta:
		model = buyerrel
		#fields = ['psave', 'type', 'i', 'o', 'bday', ]
		fields = ['type', 'i', 'o', 'bday', ]	
	

#добавление родственников
class form_1c_relcard(CreateView):
	model = buyerrel
	form_class = Form_1c_relcard
	template_name = 'form_1c_relcard.html'
	success_url = '/form/1c/getcard/?salt=123456&crc=EFA645BF3AC5297469EB61B4E0369B89&success=true'
	#fields = ['type', 'i', 'o', 'bday', ]
	crc=None
	salt=None
	
	def dispatch(self, request, *args, **kwargs):
		log.info('start=form_1c_relcard')
		self.data = get_object_or_404(buyer, id=self.kwargs['pk'])
		#http://crm.babah24.ru/form/1c/makecard/?salt=123456&crc=EFA645BF3AC5297469EB61B4E0369B89
		if 'salt' in request.GET:
			crc = makeapitoken_1c(request.GET['salt'])
			if crc.lower() == request.GET['crc'].lower():
				self.salt = id_generator()
				self.crc = crc = makeapitoken_1c(self.salt)
				return super(form_1c_relcard, self).dispatch(request, *args, **kwargs)
		return HttpResponseNotFound('<h1>Access denied</h1>')
		#return super(form_1c_relcard, self).dispatch(request, *args, **kwargs)
		
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
			form = super(form_1c_relcard, self).get_form(form_class)
			#
			#form.fields['f'].widget=forms.TextInput(attrs={'class': 'form-control'})
			#form.fields['f'].required=True
			form.fields['i'].widget=forms.TextInput(attrs={'class': 'form-control'})
			form.fields['i'].required=True
			form.fields['o'].widget=forms.TextInput(attrs={'class': 'form-control'})
			form.fields['o'].required=True
			#
			form.fields['bday'].widget=forms.TextInput(attrs={'class':'form-control'})
			form.fields['bday'].help_text='дд-мм-гггг, дд/мм/гггг, дд.мм.гггг'
			form.fields['bday'].input_formats=['%d-%m-%y', '%d/%m/%y', '%d.%m.%y', '%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y', '%Y-%m-%d']
			form.fields['bday'].required=True,
			#
			#form.fields['type'].widget=forms.Select(attrs={'class':'form-control'})
			#form.fields['type'].choices=(('male', 'Мужской'), ('female', 'Женский'))
			#
			#form.fields['seller'].widget=forms.HiddenInput()
			form.fields['seller'].widget.attrs['readonly'] = True
			return form
		return form_class(**self.get_form_kwargs())
		
	def get_initial(self, **kwargs):
		if self.request.GET:
			initial = {
				'type': self.request.GET.get('type', None),
				'i': self.request.GET.get('i', None),
				'o': self.request.GET.get('o', None),
				'bday': self.request.GET.get('bday', None),
				}
			return initial
		else:
			return super(form_1c_relcard, self).get_initial()
		return initial
		
		
	def form_valid(self, form):
		instance = form.save(commit=False)
		fdata = form.cleaned_data
		#прочеряем дубли родственником, при условии, что это уже не подтверждение записи
		if 'confirmsave' not in self.request.GET:
			#проверяем, существует ли уже родственник по входным данным из формы
			brexist=buyerrel.objects.filter(buyer=self.data, type=fdata['type'], bday=fdata['bday'])
			if brexist.exists():
				log.info('brexist.exists()=%s' % 'true')
				#если найден родственник, то редиректим на редактирование
				url=reverse('api1c:form_1c_relcard', args=[self.data.id])
				url=urljoin(url, '?salt=%s&crc=%s&type=%s&i=%s&o=%s&bday=%s&confirmsave=true' % (self.salt, self.crc, fdata['type'], fdata['i'], fdata['o'], fdata['bday']))
				return HttpResponseRedirect(url)
		#
		id1c_tmp=id1c_generator()
		instance.id1c=id1c='BR%s' % (id1c_tmp)
		instance.buyer=self.data
		instance.creator=fdata['seller']
		instance.lastmod=fdata['seller']
		instance.save()
		self.br=instance
		return super(form_1c_relcard, self).form_valid(form)
		
	def get_success_url(self):
		#return 'http://crm.babah24.ru/form/1c/getcard/?salt=%s&crc=%s&phone=%s&message=buyerrel' % (self.salt, self.crc, self.data.phone)
		return 'http://crm.babah24.ru/form/1c/export/%s/?salt=%s&crc=%s' % (self.br.id, self.salt, self.crc)
		
	def get_context_data(self, *args, **kwargs):
		log.info('get_context_data=%s' % 'start')
		context_data = super(form_1c_relcard, self).get_context_data(*args, **kwargs)
		#
		context_data.update({'salt': self.salt,})
		context_data.update({'crc': self.crc,})
		context_data.update({'buyer': self.data,})
		
		return context_data
		
		
class form_1c_export(DetailView):
	model = buyerrel
	template_name = 'form_1c_export.html'
	crc=None
	salt=None
	
	def dispatch(self, request, *args, **kwargs):
		log.info('start=form_1c_export')
		#http://crm.babah24.ru/form/1c/makecard/?salt=123456&crc=EFA645BF3AC5297469EB61B4E0369B89
		if 'salt' in request.GET:
			crc = makeapitoken_1c(request.GET['salt'])
			if crc.lower() == request.GET['crc'].lower():
				self.salt = id_generator()
				self.crc = crc = makeapitoken_1c(self.salt)
				return super(form_1c_export, self).dispatch(request, *args, **kwargs)
		return HttpResponseNotFound('<h1>Access denied</h1>')
		#return super(form_1c_export, self).dispatch(request, *args, **kwargs)
		
	def get_object(self, queryset=None):
		self.data=super(form_1c_export, self).get_object()
		return self.data
		
	def get_context_data(self, *args, **kwargs):
		log.info('get_context_data=%s' % 'start')
		context_data = super(form_1c_export, self).get_context_data(*args, **kwargs)
		#
		context_data.update({'salt': self.salt,})
		context_data.update({'crc': self.crc,})
		context_data.update({'next': 'http://crm.babah24.ru/form/1c/relcard/%s/?salt=%s&crc=%s' % (self.data.buyer.id, self.salt, self.crc),})
		return context_data
		
class form_1c_relcard_edit(forms.ModelForm):
	seller = forms.CharField(label='Кассир', widget=forms.TextInput(attrs={'class': 'form-control'}), min_length=1, max_length=300, required=True, initial='0')
	#shop = forms.CharField(label='Магазин', widget=forms.TextInput(attrs={'class': 'form-control'}), min_length=1, max_length=300, required=True)
	#cashbox = forms.CharField(label='Касса', widget=forms.TextInput(attrs={'class': 'form-control'}), min_length=1, max_length=300, required=True)

	class Meta:
		model = buyerrel
		fields = ['type', 'i', 'o', 'bday', ]	
		
class form_1c_relcard_edit(UpdateView):
	model = buyerrel
	form_class = form_1c_relcard_edit
	template_name = 'form_1c_relcard_edit.html'
	success_url = '/form/1c/getcard/?salt=123456&crc=EFA645BF3AC5297469EB61B4E0369B89&success=true'
	#fields = ['type', 'i', 'o', 'bday', ]	
	crc=None
	salt=None
	
	def dispatch(self, request, *args, **kwargs):
		log.info('start=form_1c_relcard_edit')
		#http://crm.babah24.ru/form/1c/makecard/?salt=123456&crc=EFA645BF3AC5297469EB61B4E0369B89
		if 'salt' in request.GET:
			crc = makeapitoken_1c(request.GET['salt'])
			if crc.lower() == request.GET['crc'].lower():
				self.salt = id_generator()
				self.crc = crc = makeapitoken_1c(self.salt)
				self.data = get_object_or_404(buyerrel, id=self.kwargs['pk'])
				return super(form_1c_relcard_edit, self).dispatch(request, *args, **kwargs)
		return HttpResponseNotFound('<h1>Access denied</h1>')
		#return super(form_1c_relcard_edit, self).dispatch(request, *args, **kwargs)
		
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
			form = super(form_1c_relcard_edit, self).get_form(form_class)
			#
			form.fields['i'].widget=forms.TextInput(attrs={'class': 'form-control'})
			form.fields['i'].required=True
			form.fields['o'].widget=forms.TextInput(attrs={'class': 'form-control'})
			form.fields['o'].required=True
			#
			form.fields['bday'].widget=forms.TextInput(attrs={'class':'form-control'})
			form.fields['bday'].help_text='дд-мм-гггг, дд/мм/гггг, дд.мм.гггг'
			form.fields['bday'].input_formats=['%d-%m-%y', '%d/%m/%y', '%d.%m.%y', '%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y', '%Y-%m-%d']
			form.fields['bday'].required=True,
			#form.fields['seller'].widget=forms.HiddenInput()
			form.fields['seller'].widget.attrs['readonly'] = True
			return form
		return form_class(**self.get_form_kwargs())
		
	#def get_object(self, queryset=None):
		#self.data=super(form_1c_relcard_edit, self).get_object()
		#return self.data
		
	def get_success_url(self):
		#return 'http://crm.babah24.ru/form/1c/getcard/?salt=%s&crc=%s&phone=%s&message=update' % (self.salt, self.crc, self.data.phone)def get_success_url(self):
		#return 'http://crm.babah24.ru/form/1c/getcard/?salt=%s&crc=%s&phone=%s&message=make' % (self.salt, self.crc, self.data.buyer.phone)
		return 'http://crm.babah24.ru/form/1c/export/%s/?salt=%s&crc=%s' % (self.data.id, self.salt, self.crc)

	def form_valid(self, form):
		instance = form.save(commit=False)
		fdata = form.cleaned_data
		instance.lastmod=fdata['seller']
		instance.save()
		return super(form_1c_relcard_edit, self).form_valid(form)

	def get_context_data(self, *args, **kwargs):
		log.info('get_context_data=%s' % 'start')
		context_data = super(form_1c_relcard_edit, self).get_context_data(*args, **kwargs)
		#
		context_data.update({'salt': self.salt,})
		context_data.update({'crc': self.crc,})
		context_data.update({'object': self.data,})
		return context_data