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


from django.db.models import Min, Max, Sum, Count, Avg
from django.db.models import Q, F

from ckeditor.widgets import CKEditorWidget

from dj.views import *


from django.core.mail import send_mail


from node.templatetags.nodetag import *

from node.models import *
from panel.models import *
from .models import *

import logging
log = logging.getLogger(__name__)


		
class log_list(TemplateView):
	template_name = "log_list.html"




class Form_filter_kassirlog(forms.Form):
	shop = forms.ModelMultipleChoiceField(label='Магазин', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), queryset=shop.objects.all(), required=False)
	

@method_decorator(permission_required('log.add_kassirlog'), name='dispatch')		
class log_kassir(ListView):
	template_name = "log_kassir.html"
	model = kassirlog
	#paginate_by = 20
	
	def dispatch(self, request, *args, **kwargs):
		return super(log_kassir, self).dispatch(request, *args, **kwargs)
	
	def get_queryset(self):
		data=super(log_kassir, self).get_queryset()
		
		data=data.all() #выбираем основной запрос
		
		f=Form_filter_kassirlog(self.request.GET)
		
		
		req = ''
		paging = 80
		
		if f.is_valid():
			fdata = f.cleaned_data
			#фильтрация
			if fdata['shop']:
				req = '%s&shop=%s' % (req, self.request.GET['shop'])
				puser = profileuser.objects.filter(shop__in=fdata['shop']).distinct().values('user__id')
				data=data.filter(user__in=puser).distinct()
				
		
		self.req = req
		self.data = data.filter().distinct()

		#paginator
		self.p = Paginator(data, paging)
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
		context_data = super(log_kassir, self).get_context_data(*args, **kwargs)
		context_data.update({'form': Form_filter_kassirlog(self.request.GET),})
		context_data.update({'req': self.req,})
		context_data.update({'count': self.p.count,})

		return context_data
		
		
