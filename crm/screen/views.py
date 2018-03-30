# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponsePermanentRedirect

from django.core.exceptions import PermissionDenied

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django import forms
from django.contrib.auth.models import User, Group

import json
from django.core import serializers

from django.http import QueryDict

from django.views.generic import DetailView, ListView, DeleteView
from django.views.generic.edit import FormView, UpdateView
from django.views.generic.base import TemplateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator

import datetime, time

from django.db.models import Sum, Count, Q, IntegerField
from django.db.models.functions import Cast

from django.views.decorators.csrf import csrf_exempt

#from node.templatetags.nodetags import node_count

from node.models import *
from .models import *

from dj.views import *



class screenhome(ListView):
	template_name = 'screenhome.html'
	model = tax
	#paginate_by = 4
	
	def dispatch(self, request, *args, **kwargs):
		return super(screenhome, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(screenhome, self).get_queryset()
		self.data=data.filter(status=True).order_by('id')
		return self.data
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(screenhome, self).get_context_data(*args, **kwargs)
		#context_data.update({'leftmenu': tax.objects.all(),})
		return context_data
		
class screenlist(ListView):
	template_name = 'screenlist.html'
	model = goods
	paginate_by = 6
	
	def dispatch(self, request, *args, **kwargs):
		self.tax = get_object_or_404(tax, id=self.kwargs['pk'])
		return super(screenlist, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		self.data=super(screenlist, self).get_queryset()
		
		#########################################
		########обработка дочерних категорий#####
		#########################################
		datatax=tax.objects.filter(id=self.tax.id).values('id')
		taxin=datatax
		#берем дочернии категории, если есть
		taxparent = tax.objects.filter(parent__in=datatax).values('id')
		if taxparent:
			taxin = taxparent
		#########################################
		
		self.data=self.data.filter(Q(catalogshow=True), Q(status=True), Q(touchscreen=True), Q(tax__in=taxin) | Q(tax__in=datatax)).distinct()
		
		#сортировка
		#sqlalchemy
		#res=goods.sa.query().join(goods.sa.tax).join(propertiesvalue.sa).join(properties.sa).filter(goods.sa.status==True, goods.sa.touchscreen==True, tax.sa.id==12, properties.sa.code=='KOL_RAZ').order_by(cast(propertiesvalue.sa.value, Numeric).desc())
		
		self.data=self.data.order_by('bname')
		
		try:
			self.kwargs['sort']
		except:
			self.data=self.data.order_by('bname')
		else:
			if self.kwargs['sort'] == 'bname':
				self.data=self.data.order_by('bname')
			if self.kwargs['sort'] == 'price':
				self.data=self.data.order_by('price')
			if self.kwargs['sort'] == 'a': #количество зарядов
				self.data=self.data.order_by('propa')
				#self.data=self.data.filter(propertiesvalue__properties__code='KOL_RAZ').annotate(c=Cast('propertiesvalue__value', IntegerField())).order_by('c')
			if self.kwargs['sort'] == 'b': #продолжительность
				self.data=self.data.order_by('propb')
				#self.data=self.data.filter(propertiesvalue__properties__code='TIME').annotate(c=Cast('propertiesvalue__value', IntegerField())).order_by('c')
			
		return self.data
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(screenlist, self).get_context_data(*args, **kwargs)
		context_data.update({'leftmenu': tax.objects.filter(status=True).order_by('id'),})
		context_data.update({'tax': self.tax,})
		return context_data
		
class Form_filter_screenlistsearch(forms.Form):
	q = forms.CharField(label='Поиск', help_text='Введите слово для поиска', widget=forms.TextInput(attrs={'class': 'form-control inputkeyboard','autocomplete': 'off'}), max_length=100, required=False)

class screenlistsearch(ListView):
	template_name = 'screenlistsearch.html'
	model = goods
	#paginate_by = 6
	
	def dispatch(self, request, *args, **kwargs):
		#self.tax = get_object_or_404(tax, id=self.kwargs['pk'])
		return super(screenlistsearch, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
	
		f=Form_filter_screenlistsearch(self.request.GET)
		fdata = f.cleaned_data
	
		req = ''
	
		self.data=super(screenlistsearch, self).get_queryset()
		
		#########################################
		########обработка дочерних категорий#####
		#########################################
		#datatax=tax.objects.filter(id=self.tax.id).values('id')
		#taxin=datatax
		#берем дочернии категории, если есть
		#taxparent = tax.objects.filter(parent__in=datatax).values('id')
		#if taxparent:
		#	taxin = taxparent
		#########################################
		
		self.data=self.data.filter(Q(catalogshow=True), Q(status=True), Q(touchscreen=True)).distinct()
		
		if f.is_valid():
			#фильтрация
			if fdata['q']:
				req = '%s&q=%s' % (req, fdata['q'])
				self.data=self.data.filter(Q(name__icontains=fdata['q']) | Q(name__search=fdata['q']) | Q(bname__icontains=fdata['q']) | Q(bname__search=fdata['q']))
		
		
		
		self.data=self.data.order_by('bname')
		
		self.req = req
			
		#data=data.order_by('-id')

		#paginator
		self.p = Paginator(self.data, 6)
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
		context_data = super(screenlistsearch, self).get_context_data(*args, **kwargs)
		context_data.update({'form': Form_filter_screenlistsearch(self.request.GET),})
		context_data.update({'req': self.req,})
		context_data.update({'urlpage': '/screen/listsearch',})
		context_data.update({'leftmenu': tax.objects.filter(status=True).order_by('id'),})
		#context_data.update({'tax': self.tax,})
		return context_data
		
		
@csrf_exempt
def screenshowvideocount(request, pk):
	if request.method == 'GET':
		data = get_object_or_404(goods, id=pk)
		data.showvideocount = data.showvideocount+1
		data.save()
		tmp={'res': 1, 'data': u'count',}
		return HttpResponse(json.dumps(tmp), content_type='application/json')
		
	tmp={'res': 0, 'data': u'bad',}
	return HttpResponse(json.dumps(tmp), content_type='application/json')
		
