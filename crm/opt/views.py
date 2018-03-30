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
from django.db.models import Q, F, FloatField

from ckeditor.widgets import CKEditorWidget

#
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from io import BytesIO
from django.template.loader import render_to_string
from weasyprint import HTML
from django.template.defaultfilters import date
#

from dj.views import *
from acl.views import *

from django.core.mail import send_mail

from django.conf import settings

from node.templatetags.nodetag import *



from node.models import *
from log.models import *

from .models import *

import logging
log = logging.getLogger(__name__)


#@method_decorator(permission_required('opt.add_optprice'), name='dispatch')
class optbuyer_list(ListView):
	template_name = 'optbuyer_list.html'
	model = optbuyer
	#paginate_by = 20
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'opt', 'R')
		return super(optbuyer_list, self).dispatch(request, *args, **kwargs)
		
	# def get_queryset(self):
		# data=super(optbuyer_list, self).get_queryset()
		# self.data=data.all().order_by('-edate')
		# return self.data
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(optbuyer_list, self).get_context_data(*args, **kwargs)
		#context_data.update({'command': True,})
		return context_data

#@method_decorator(permission_required('opt.add_optprice'), name='dispatch')
class optbuyer_add(CreateView):
	model = optbuyer
	template_name = 'optbuyer_add.html'
	success_url = '/opt/buyer/list'
	fields = ['status', 'name', 'phone', 'email', 'fullname', 'namedir', 'org', 'inn', 'ogrn', 'bik', 'bankname', 'checkaccount', 'coraccount', 'uraddr',]

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'opt', 'R')
		#self.b = get_object_or_404(self.model , id=self.kwargs['pk'])
		return super(optbuyer_add, self).dispatch(request, *args, **kwargs)
	
	#def get_success_url(self):
	#	return '%s/%s' % (self.success_url, self.hashkey)
	
	def form_valid(self, form):
		#instance = form.save(commit=False)
		#instance.url = id_generator()
		#instance.save()
		return super(optbuyer_add, self).form_valid(form)	
	
	def get_context_data(self, **kwargs):
		context = super(optbuyer_add, self).get_context_data(**kwargs)
		#context['object'] = self.b
		return context

#@method_decorator(permission_required('opt.add_optprice'), name='dispatch')
class optbuyer_edit(UpdateView):
	model = optbuyer
	template_name = 'optbuyer_edit.html'
	success_url = '/opt/buyer/list'
	fields = ['status', 'name', 'phone', 'email', 'fullname', 'namedir', 'org', 'inn', 'ogrn', 'bik', 'bankname', 'checkaccount', 'coraccount', 'uraddr',]
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'opt', 'R')
		#self.e = get_object_or_404(self.model, id=self.kwargs['pk'], user=request.user) #ПОТОМ ВКЛЮЧИТЬ
		return super(optbuyer_edit, self).dispatch(request, *args, **kwargs)
	
	def get_success_url(self):
		url = '/opt/buyer/edit/%s' % (self.get_object().id)
		return url
	
	def get_context_data(self, **kwargs):
		context = super(optbuyer_edit, self).get_context_data(**kwargs)
		context['object'] = self.get_object()
		return context		
		
#@method_decorator(permission_required('opt.add_optprice'), name='dispatch')	
class optbuyer_del(DeleteView):
	model = optbuyer
	template_name = '_confirm_delete.html'
	success_url = '/opt/buyer/list/'

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'opt', 'R')
		self.data = get_object_or_404(self.model, id=self.kwargs['pk'])
		return super(optbuyer_del, self).dispatch(request, *args, **kwargs)
	
	#def get_object(self, queryset=None):
	#	return get_object_or_404(self.model, id=self.kwargs['pk'])
		
	def get_context_data(self, **kwargs):
		context = super(optbuyer_del, self).get_context_data(**kwargs)
		context['object'] = self.data.id
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = '/opt/buyer/list/'
		return context		
		
		

#@method_decorator(permission_required('opt.add_optprice'), name='dispatch')
class optprice_list(ListView):
	template_name = 'optprice_list.html'
	model = optprice
	#paginate_by = 20
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'opt', 'R')
		return super(optprice_list, self).dispatch(request, *args, **kwargs)
		
	# def get_queryset(self):
		# data=super(optprice_list, self).get_queryset()
		# self.data=data.all().order_by('-edate')
		# return self.data
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(optprice_list, self).get_context_data(*args, **kwargs)
		#context_data.update({'command': True,})
		return context_data


class optprice_detail(DetailView):
	model = optprice
	template_name = 'optprice_detail.html'
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'opt', 'R')
		return super(optprice_detail, self).dispatch(request, *args, **kwargs)
		
	def get_object(self, queryset=None):
		data = super(optprice_detail, self).get_object()
		#self.data = self.get_object()
		#self.data = get_object_or_404(optprice, status='accept', url=self.kwargs['url'])
		self.data = data
		return self.data
	
	def get_context_data(self, *args, **kwargs):
		context_data = super(optprice_detail, self).get_context_data(*args, **kwargs)
		#context_data.update({'params': params})
		return context_data		
		
		
		

#@method_decorator(permission_required('opt.add_optprice'), name='dispatch')
class optprice_add(CreateView):
	model = optprice
	template_name = 'optprice_add.html'
	success_url = '/opt/price/list'
	fields = ['optbuyer', 'status', 'name', 'comment', ]

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'opt', 'R')
		#self.b = get_object_or_404(self.model , id=self.kwargs['pk'])
		return super(optprice_add, self).dispatch(request, *args, **kwargs)
	
	#def get_success_url(self):
	#	return '%s/%s' % (self.success_url, self.hashkey)
	
	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.url = id_generator()
		instance.save()
		return super(optprice_add, self).form_valid(form)	
	
	
	def get_context_data(self, **kwargs):
		context = super(optprice_add, self).get_context_data(**kwargs)
		#context['object'] = self.b
		return context


#@method_decorator(permission_required('opt.add_optprice'), name='dispatch')
class optprice_edit(UpdateView):
	model = optprice
	template_name = 'optprice_edit.html'
	success_url = '/opt/price/list'
	fields = ['optbuyer', 'status', 'name', 'comment', ]
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'opt', 'R')
		#self.e = get_object_or_404(self.model, id=self.kwargs['pk'], user=request.user) #ПОТОМ ВКЛЮЧИТЬ
		return super(optprice_edit, self).dispatch(request, *args, **kwargs)
	
	def get_success_url(self):
		url = '/opt/price/detail/%s' % (self.get_object().id)
		return url
	
	def get_context_data(self, **kwargs):
		context = super(optprice_edit, self).get_context_data(**kwargs)
		context['object'] = self.get_object()
		return context

#@method_decorator(permission_required('opt.add_optprice'), name='dispatch')	
class optprice_del(DeleteView):
	model = optprice
	template_name = '_confirm_delete.html'
	success_url = '/opt/price/list/'

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'opt', 'R')
		self.data = get_object_or_404(self.model, id=self.kwargs['pk'])
		return super(optprice_del, self).dispatch(request, *args, **kwargs)
	
	#def get_object(self, queryset=None):
	#	return get_object_or_404(self.model, id=self.kwargs['pk'])
		
	def get_context_data(self, **kwargs):
		context = super(optprice_del, self).get_context_data(**kwargs)
		context['object'] = self.data.id
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = '/opt/price/list/'
		return context

class optprice_contract(DetailView):
	model = optprice
	template_name = 'optprice_contract.html'
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'opt', 'R')
		return super(optprice_contract, self).dispatch(request, *args, **kwargs)
		
	def get_object(self, queryset=None):
		data = super(optprice_contract, self).get_object()
		#self.data = self.get_object()
		#self.data = get_object_or_404(optprice, status='accept', url=self.kwargs['url'])
		self.data = data
		return self.data
	
	def render_to_response(self, context, **response_kwargs):
		if 'type' in self.request.GET:
			html_string = render_to_string('optprice_contract.html', {'params': context['params']})
			html = HTML(string=html_string)
			if self.request.GET['type'] == 'viewpdf':
				buffer = BytesIO() #make empty buffer in memory
				html.write_pdf(target=buffer) #send render pdf to buffer
				output = buffer.getvalue() #get data from buffer to output
				buffer.close() #close buffer
				
				response = HttpResponse(output, content_type='application/pdf')
				response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % (self.data.url)
				return response
			if self.request.GET['type'] == 'exportpdf':
				buffer = BytesIO() #make empty buffer in memory
				html.write_pdf(target=buffer) #send render pdf to buffer
				output = buffer.getvalue() #get data from buffer to output
				self.data.contract.save('pricecontractpdf.pdf', File(buffer))
				buffer.close() #close buffer
				
				response = HttpResponse(output, content_type='application/pdf')
				response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % (self.data.url)
				return response
		
		response_kwargs.setdefault('content_type', self.content_type)
		return self.response_class(
			request = self.request,
			template = self.get_template_names(),
			context = context,
			**response_kwargs
		)

	def get_context_data(self, *args, **kwargs):
		context_data = super(optprice_contract, self).get_context_data(*args, **kwargs)
		params = {
			'number': self.data.id,
			'date': "«%s» %s %s г." % (self.data.utime.day, date(self.data.utime, 'M'), self.data.utime.year),
			'req1': "Индивидуальный предприниматель",
			'base': "ОГРН %s" % (self.data.optbuyer.ogrn),
			'fio': self.data.optbuyer.namedir,
			'req2': self.data.optbuyer.name,
			'legaddress': self.data.optbuyer.uraddr,
			'inn': self.data.optbuyer.inn,
			'bik': self.data.optbuyer.bik,
			'checkaccount': self.data.optbuyer.checkaccount,
			'bank': self.data.optbuyer.bankname,
			'coraccount': self.data.optbuyer.coraccount,
		}
		context_data.update({'params': params})
		return context_data


##########################################################################################################	
	
class Form_filter_majorprice(forms.Form):
	q = forms.CharField(label='Поиск', help_text='Введите слово для поиска', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'off'}), max_length=100, required=False)
	tax = forms.ModelMultipleChoiceField(label='Категория', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), queryset=tax.objects.all(), required=False)
	pricefrom = forms.FloatField(label="Цена от", required=False,)
	priceto = forms.FloatField(label="Цена до", required=False,)
	paging = forms.BooleanField(label='На одной странице', initial=True, required=False)
	sort = forms.ChoiceField(label='Сортировка', help_text='Сортировать по полю', widget=forms.Select(attrs={'class': 'form-control'}), choices=(('name', 'Название'),('-price', 'Дороже'),('price', 'Дешевле'),), required=False)
	
#@method_decorator(permission_required('node.add_goods'), name='dispatch')
class majorprice(ListView):
	template_name = 'majorprice.html'
	model = goods
	#paginate_by = 10
	
	def dispatch(self, request, *args, **kwargs):
		try:
			self.optprice = optprice.objects.get(status='create', url=self.kwargs['url'])
		except:
			return HttpResponseRedirect('http://babah24.ru/opt/noprice/')
		else:
			self.urlpage = '/major/price/%s' % (self.optprice.url)
			self.priceid = self.optprice.url
		return super(majorprice, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(majorprice, self).get_queryset()
		
		data=data.all().order_by('name') #выбираем основной запрос
		#в наличии
		data=data.filter(goodsinstock__value__gte=1, manualstartprice__gte=0.01).distinct()
		#по основной базе
		base = base1c.objects.get(id=1)
		data=data.filter(base=base)
		
		
		f=Form_filter_majorprice(self.request.GET)
		
		req = ''
		paging = 60
		
		if f.is_valid():
			fdata = f.cleaned_data
			#фильтрация
			if fdata['q']:
				req = '%s&q=%s' % (req, fdata['q'])
				data=data.filter(Q(id__icontains=fdata['q']) | Q(id1c__icontains=fdata['q']) | Q(idbitrix__icontains=fdata['q']) | Q(name__search=fdata['q']) | Q(namefull__search=fdata['q']) | Q(art__icontains=fdata['q']) | Q(bname__search=fdata['q']))
				
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
				
			if fdata['sort']:
				req = '%s&sort=%s' % (req, self.request.GET['sort'])
				data=data.order_by(fdata['sort'])
				
		#подсчет количества по остаткам на складах
		self.sum=data.aggregate(s=Sum('goodsinstock__value'))

		self.req = req

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
		context_data = super(majorprice, self).get_context_data(*args, **kwargs)
		context_data.update({'req': self.req,})
		context_data.update({'urlpage': self.urlpage,})
		context_data.update({'priceid': self.priceid,})
		context_data.update({'count': self.p.count,})
		context_data.update({'form': Form_filter_majorprice(self.request.GET, initial={'q': '123',})})
		context_data.update({'sum': self.sum})
		
		return context_data

		
		
		
		
@csrf_exempt
def majorcartadd(request):
	tmp={'res': 0, 'data': u'bad',}
	if request.method == 'GET':
		try:
			data=optprice.objects.get(status='create', url=request.GET['priceid'])
			p=goods.objects.get(id=request.GET['id'], manualstartprice__gte=0.01)
			quant = request.GET['quant']
		except:
			tmp={'res': 0, 'data': u'bad',}
		else:
			q = goodsinstock.objects.filter(goods=p).aggregate(count=Sum('value'))
			try:
				cartitem=optpricecart.objects.get(optprice=data, goods=p)
			except:
				cartitem=optpricecart.objects.create(optprice=data, goods=p, price=p.manualstartprice)
				cartitem.save()

			if int(quant)+cartitem.quant <= int(q['count']):
				cartitem.quant=int(quant)+cartitem.quant
			else:
				cartitem.quant=q['count']
			cartitem.save()
					
			tmp={'res': 1, 'data': u'add to store good',}

	return HttpResponse(json.dumps(tmp), content_type='application/json')


@csrf_exempt
def majorcartdel(request, url, pk):
	tmp={'res': 0, 'data': u'bad',}
	if request.method == 'GET':
		try:
			price=optprice.objects.get(status='create', url=url)
			p=goods.objects.get(id=pk)
		except:
			return HttpResponseRedirect('http://babah24.ru/')
		else:
			q = optpricecart.objects.filter(optprice=price, goods=p).delete()
			return HttpResponseRedirect('/major/cart/%s' % (price.url))

	return HttpResponseRedirect('http://babah24.ru/')	
		
		
@csrf_exempt
def majorcartclear(request, url):
	tmp={'res': 0, 'data': u'bad',}
	if request.method == 'GET':
		try:
			price=optprice.objects.get(status='create', url=url)
		except:
			return HttpResponseRedirect('http://babah24.ru/')
		else:
			q = optpricecart.objects.filter(optprice=price).delete()
			return HttpResponseRedirect('/major/cart/%s' % (price.url))

	return HttpResponseRedirect('http://babah24.ru/')	
		
#корзина
class majorcart(ListView):
	template_name = 'majorcart.html'
	model = optpricecart
	#paginate_by = 20
	
	def dispatch(self, request, *args, **kwargs):
		if self.request.user.is_authenticated:
			self.optprice = get_object_or_404(optprice, url=self.kwargs['url'])
		else:
			try:
				self.optprice = optprice.objects.get(Q(status='create') | Q(status='accept'), url=self.kwargs['url'])
			except:
				return HttpResponseRedirect('http://babah24.ru/opt/noprice/')			
		return super(majorcart, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(majorcart, self).get_queryset()
		self.data=data.filter(optprice=self.optprice)
		return self.data
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(majorcart, self).get_context_data(*args, **kwargs)
		context_data.update({'object': self.optprice})
		context_data.update({'sum': self.data.aggregate(s=Sum(F('goods__manualstartprice')*F('quant')))['s'],})
		context_data.update({'count': self.data.aggregate(c=Count('goods__id'))['c'],})
		context_data.update({'quant': self.data.aggregate(s=Sum('quant'))['s'],})
		return context_data



#корзина версия для печати
class majorcartprint(ListView):
	template_name = 'majorcartprint.html'
	model = optpricecart
	#paginate_by = 20
	
	def dispatch(self, request, *args, **kwargs):
		if self.request.user.is_authenticated:
			self.optprice = get_object_or_404(optprice, url=self.kwargs['url'])
		else:
			try:
				self.optprice = optprice.objects.get(Q(status='create') | Q(status='accept'), url=self.kwargs['url'])
			except:
				return HttpResponseRedirect('http://babah24.ru/opt/noprice/')	
		return super(majorcartprint, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(majorcartprint, self).get_queryset()
		self.data=data.filter(optprice=self.optprice)
		return self.data
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(majorcartprint, self).get_context_data(*args, **kwargs)
		context_data.update({'object': self.optprice})
		context_data.update({'sum': self.data.aggregate(s=Sum(F('goods__manualstartprice')*F('quant')))['s'],})
		context_data.update({'count': self.data.aggregate(c=Count('goods__id'))['c'],})
		context_data.update({'quant': self.data.aggregate(s=Sum('quant'))['s'],})
		return context_data



		
class majororder(UpdateView):
	model = optbuyer
	template_name = 'majororder.html'
	success_url = '/major/success/'
	fields = ['fullname', 'namedir', 'org', 'inn', 'ogrn', 'bik', 'bankname', 'checkaccount', 'coraccount', 'uraddr',]

	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(optprice, status='create', url=self.kwargs['url'])
		return super(majororder, self).dispatch(request, *args, **kwargs)
	
	def get_success_url(self):
		return '/major/success/%s' % (self.data.url)
	
	def get_object(self, queryset=None):
		#data = super(majororder, self).get_object()
		#data = self.get_object()
		return self.data.optbuyer
	
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
			form = super(majororder, self).get_form(form_class)

			if 'pay' in self.request.GET and self.request.GET['pay'] == 'false':
				form.fields['fullname'].widget=forms.HiddenInput()
				#form.fields['namedir'].widget=forms.HiddenInput()
				form.fields['org'].widget=forms.HiddenInput()
				form.fields['inn'].widget=forms.HiddenInput()
				form.fields['ogrn'].widget=forms.HiddenInput()
				form.fields['bik'].widget=forms.HiddenInput()
				form.fields['bankname'].widget=forms.HiddenInput()
				form.fields['checkaccount'].widget=forms.HiddenInput()
				form.fields['coraccount'].widget=forms.HiddenInput()
				form.fields['uraddr'].widget=forms.HiddenInput()
				#form.fields['phone'].required=True
				#form.fields['email2'].required=True
			else:
				form.fields['fullname'].required=True
				form.fields['namedir'].required=True
				form.fields['org'].required=True
				form.fields['inn'].required=True
				form.fields['ogrn'].required=True
				form.fields['bik'].required=True
				form.fields['bankname'].required=True
				form.fields['checkaccount'].required=True
				form.fields['coraccount'].required=True
				form.fields['uraddr'].required=True
				#form.fields['phone'].required=True
				#form.fields['email2'].required=True
			return form
		return form_class(**self.get_form_kwargs())
	
	def form_valid(self, form):
		#instance = form.save(commit=False)
		#instance.status = 'accept'
		#instance.save()
		self.data.status = 'accept' #меняем статус прайса
		self.data.save()
		#отправляем письмо на почту администраторам
		mres=mailres.objects.create(email='admins', action='MAJOR PRICE SUCCESS')
		try:
			a=send_mail(u'Опт. Заказ', u'Опт. Заказ #%s' % (self.data.id), settings.EMAIL_HOST_USER, ['office@babah24.ru', 'it@babah24.ru',], fail_silently=True)
			#a=mail_admins(u'create order okimarket.ru', u'Создан заказ на сайте okimarket.ru', fail_silently=False)
		except Exception as e:
			mres.result = e
		else:
			pass
			mres.result = '1'
		mres.save()
		return super(majororder, self).form_valid(form)	
	
	
	def get_context_data(self, *args, **kwargs):
		context_data = super(majororder, self).get_context_data(*args, **kwargs)
		context_data.update({'object': self.data})
		context_data.update({'sum': optpricecart.objects.filter(optprice=self.data).aggregate(s=Sum(F('goods__manualstartprice')*F('quant')))['s'],})
		context_data.update({'count': optpricecart.objects.filter(optprice=self.data).aggregate(c=Count('goods__id'))['c'],})
		context_data.update({'quant': optpricecart.objects.filter(optprice=self.data).aggregate(s=Sum('quant'))['s'],})
		return context_data
		
class majorsuccess(DetailView):
	model = optprice
	template_name = 'majorsuccess.html'
	
	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(optprice, status='accept', url=self.kwargs['url'])
		return super(majorsuccess, self).dispatch(request, *args, **kwargs)
	
	def get_object(self, queryset=None):
		#data = super(majorsuccess, self).get_object()
		#data = self.get_object()
		return optprice.objects.get(status='accept', url=self.kwargs['url'])
	

class majorcontract(DetailView):
	model = optprice
	template_name = 'majorcontract.html'
	
	def dispatch(self, request, *args, **kwargs):
		return super(majorcontract, self).dispatch(request, *args, **kwargs)
		
	def get_object(self, queryset=None):
		#data = super(majorcontract, self).get_object()
		#data = self.get_object()
		self.data = get_object_or_404(optprice, status='contract', url=self.kwargs['url'])
		return self.data
	
	def get_context_data(self, *args, **kwargs):
		context_data = super(majorcontract, self).get_context_data(*args, **kwargs)
		#context_data.update({'params': params})
		return context_data

	
# def majorcontract(request, url):
	# params = {
		# 'number': 59,
		# 'date': "«19» января 2018 г.",
		# 'req1': "Индивидуальный предприниматель",
		# 'base': "ОГРН313246805300077",
		# 'fio': "Беляев Алексей Анатольевич",
		# 'req2': "ИП Беляев А.А.",
		# 'legaddress': "660010, г.Красноярск, пр.им.Газеты Красноярский рабочий, д.127, кв.40",
		# 'inn': 246400016053,
		# 'bik': "040407702",
		# 'checkaccount': 40802810500030001391,
		# 'bank': "Красноярский филиал АКБ «Ланта-Банк» (ЗАО)",
		# 'coraccount': 30101810000000000702
	# }

	# html_string = render_to_string('majorcontract.html',{'params': params})

	# html = HTML(string=html_string)
	# html.write_pdf(target='/tmp/mypdf.pdf');

	# fs = FileSystemStorage('/tmp')
	# with fs.open('mypdf.pdf') as pdf:
			# response = HttpResponse(pdf, content_type='application/pdf')
			# response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
			# return response

	# return response
