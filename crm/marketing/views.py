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
from .models import *

import logging
log = logging.getLogger(__name__)

	
	
	
	
@method_decorator(permission_required('marketing.add_marketing_report'), name='dispatch')
class marketing_report_list(ListView):
	template_name = 'marketing_report_list.html'
	model = marketing_report
	paginate_by = 60
	
	def dispatch(self, request, *args, **kwargs):
		return super(marketing_report_list, self).dispatch(request, *args, **kwargs)
	
	
@method_decorator(permission_required('marketing.add_marketing_report'), name='dispatch')
class marketing_report_add(CreateView):
	model = marketing_report
	template_name = 'marketing_report_add.html'
	#form_class = Form_create_nickname
	success_url = '/marketing/report/list/?success=true'
	fields = ['name', 'cdate', 'creator', 'place', 'comment', 'usepersonal', 'col', ]
	
	def dispatch(self, request, *args, **kwargs):
		#self.data = get_object_or_404(marketing_report, id=self.kwargs['pk'])
		return super(marketing_report_add, self).dispatch(request, *args, **kwargs)
	
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
			form = super(marketing_report_add, self).get_form(form_class)
			form.fields['cdate'].widget=forms.TextInput(attrs={'class':'mydatepicker1'})
			form.fields['cdate'].input_formats=['%d-%m-%y', '%d-%m-%Y', '%d/%m/%y', '%d/%m/%Y', '%d.%m.%y', '%d.%m.%Y']
			#form.fields['cdate'].help_text=('формат %d-%m-%Y')
			return form
		return form_class(**self.get_form_kwargs())
	
	#def get_success_url(self):
	#	return '/marketing/report/detail/%s' % (self.data.id)


@method_decorator(permission_required('marketing.add_marketing_report'), name='dispatch')
class marketing_report_edit(UpdateView):
	model = marketing_report
	template_name = 'marketing_report_edit.html'
	success_url = '/marketing/report/list/?success=true'
	fields = ['name', 'cdate', 'creator', 'place', 'comment', 'usepersonal', 'col', ]
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_404(self.model, id=self.kwargs['pk'])
		return super(marketing_report_edit, self).dispatch(request, *args, **kwargs)

	def get_success_url(self):
		return '/marketing/report/detail/%s' % (self.get_object().id)				
		
		
@method_decorator(permission_required('marketing.add_marketing_report'), name='dispatch')
class marketing_report_detail(DetailView):
	model = marketing_report
	template_name = 'marketing_report_detail.html'
	
	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(self.model, id=self.kwargs['pk'])
		return super(marketing_report_detail, self).dispatch(request, *args, **kwargs)	
		
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(marketing_report_detail, self).get_context_data(*args, **kwargs)
		context_data.update({'sum': marketing_report_item.objects.filter(marketing_report=self.data).aggregate(s=Sum('sum'))['s'],})
		return context_data	
		
	
	
@method_decorator(permission_required('marketing.add_marketing_report'), name='dispatch')
class marketing_report_item_add(CreateView):
	model = marketing_report_item
	template_name = 'marketing_report_item_add.html'
	#form_class = Form_create_nickname
	success_url = '/marketing/report/list/?success=true'
	fields = ['name', 'sum', 'comment',]
	
	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(marketing_report, id=self.kwargs['pk'])
		return super(marketing_report_item_add, self).dispatch(request, *args, **kwargs)

	def get_success_url(self):
		return '/marketing/report/detail/%s' % (self.data.id)	
		
	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.marketing_report = self.data
		instance.save()
		return super(marketing_report_item_add, self).form_valid(form)
		
		
class marketing_report_item_del(DeleteView):
	model = marketing_report_item
	template_name = '_confirm_delete.html'
	success_url = '/marketing/report/list/?success=true'
	
	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(self.model, id=self.kwargs['pk'])
		return super(marketing_report_item_del, self).dispatch(request, *args, **kwargs)
	
	def get_success_url(self):
		return '/marketing/report/detail/%s' % (self.data.marketing_report.id)
		
	def get_context_data(self, **kwargs):
		context = super(marketing_report_item_del, self).get_context_data(**kwargs)
		#context['object'] = mark_safe('<a href="%s">файл</a>' % self.data.sourcefile.url)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = '/marketing/report/detail/%s' % (self.data.marketing_report.id)
		return context
		
@method_decorator(permission_required('marketing.add_marketing_report'), name='dispatch')
class marketing_report_item_edit(UpdateView):
	model = marketing_report_item
	template_name = 'marketing_report_item_edit.html'
	#form_class = Form_create_nickname
	success_url = '/marketing/report/list/?success=true'
	fields = ['name', 'sum', 'comment',]
	
	def dispatch(self, request, *args, **kwargs):
		self.data=get_object_or_404(self.model, id=self.kwargs['pk'])
		return super(marketing_report_item_edit, self).dispatch(request, *args, **kwargs)

	def get_success_url(self):
		return '/marketing/report/detail/%s' % (self.data.marketing_report.id)	
		
