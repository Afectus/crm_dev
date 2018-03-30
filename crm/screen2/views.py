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


urlroot = 'screen2'



class screenhome2(ListView):
	template_name = 'screenhome2.html'
	model = tax
	#paginate_by = 4
	
	def dispatch(self, request, *args, **kwargs):
		return super(screenhome2, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(screenhome2, self).get_queryset()
		self.data=data.filter(status=True).order_by('id')
		return self.data
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(screenhome2, self).get_context_data(*args, **kwargs)
		context_data.update({'urlroot': urlroot,})
		return context_data
	

class Form_filter_screenlistsearch2(forms.Form):
	#q = forms.CharField(label='Поиск', help_text='Введите слово для поиска', widget=forms.TextInput(attrs={'class': 'form-control inputkeyboard','autocomplete': 'off', 'oninput': 'listsearch(this);',}), max_length=100, required=True)
	q = forms.CharField(label='Поиск', help_text='Введите слово для поиска', widget=forms.TextInput(attrs={'class': 'form-control inputkeyboard','autocomplete': 'off', 'placeholder': u'Поиск',}), max_length=100, required=True)
	
class screenlist2(ListView):
	template_name = 'screenlist2.html'
	model = goods
	#paginate_by = 6
	
	def dispatch(self, request, *args, **kwargs):
		return super(screenlist2, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		self.data=super(screenlist2, self).get_queryset()
		
		try:
			self.tax = get_object_or_404(tax, id=self.kwargs['pk'])
		except:
			self.tax = get_object_or_404(tax, id=2)

		#поиск	
		f=Form_filter_screenlistsearch2(self.request.GET)
		

		if f.is_valid():
			fdata = f.cleaned_data
			#self.data=self.data.filter(Q(catalogshow=True), Q(status=True), Q(touchscreen=True)).distinct()
			self.data=self.data.filter(Q(status=True), Q(touchscreen=True)).distinct()
			#фильтрация
			if fdata['q']:
				self.data=self.data.filter(Q(name__icontains=fdata['q']) | Q(name__search=fdata['q']) | Q(bname__icontains=fdata['q']) | Q(bname__search=fdata['q']))
		else:
			#########################################
			########обработка дочерних категорий#####
			#########################################
			taxin=tax.objects.filter(id=self.tax.id).values('id')
			#берем дочернии категории, если есть
			taxparent = tax.objects.filter(parent__in=taxin).values('id')
			if taxparent:
				taxin = taxparent
			#########################################
			
			self.data=self.data.filter(Q(catalogshow=True), Q(status=True), Q(touchscreen=True), Q(tax__in=taxin)).distinct()
			
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
		context_data = super(screenlist2, self).get_context_data(*args, **kwargs)
		context_data.update({'leftmenu': tax.objects.filter(status=True).order_by('id'),})
		context_data.update({'tax': self.tax,})
		context_data.update({'form': Form_filter_screenlistsearch2(self.request.GET),})
		context_data.update({'urlroot': urlroot,})
		return context_data
		
		
@csrf_exempt
def screenshowvideocount2(request, pk):
	if request.method == 'GET':
		data = get_object_or_404(goods, id=pk)
		data.showvideocount = data.showvideocount+1
		data.save()
		tmp={'res': 1, 'data': u'count',}
		return HttpResponse(json.dumps(tmp), content_type='application/json')
		
	tmp={'res': 0, 'data': u'bad',}
	return HttpResponse(json.dumps(tmp), content_type='application/json')
		
