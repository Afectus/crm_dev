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

from acl.views import *
from node.models import *
from panel.form import *
from .models import *
from projects.models import *

import logging
log = logging.getLogger(__name__)


	
#@method_decorator(permission_required('holiday.add_holiday'), name='dispatch')
class holiday_list(ListView):
	template_name = 'holiday_list.html'
	model = holiday
	paginate_by = 20
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'holiday', 'R')
		return super(holiday_list, self).dispatch(request, *args, **kwargs)
	
	def get_queryset(self):
		data=super(holiday_list, self).get_queryset()
		return data.filter(status=True)
	
	def get_context_data(self, *args, **kwargs):
		context_data = super(holiday_list, self).get_context_data(*args, **kwargs)
		context_data.update({'projects': projects.objects.filter(status=True)})
		return context_data
	
	
	
	
#@method_decorator(permission_required('holiday.add_holiday'), name='dispatch')
class holiday_add(CreateView):
	model = holiday
	template_name = '_add.html'
	success_url = '/holiday/list'
	fields = ['status', 'sdate', 'edate', 'user', 'message',]
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'holiday', 'R')
		return super(holiday_add, self).dispatch(request, *args, **kwargs)

	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
			form = super(holiday_add, self).get_form(form_class)
			#form.fields['sdate'].widget=forms.TextInput(attrs={'class':'form-control datepicker', 'data-dateformat': "dd-mm-yy"})
			#form.fields['edate'].widget.attrs['class'] = 'form-control datepicker'
			#form.fields['sdate'].widget=forms.TextInput(attrs={'class':'form-control datepicker', 'data-dateformat': "dd-mm-yy"})
			#form.fields['edate'].widget=forms.TextInput(attrs={'class':'form-control datepicker', 'data-dateformat': "dd-mm-yy"})
			form.fields['sdate'].widget.attrs['class'] = 'form-control datepicker'
			form.fields['edate'].widget.attrs['class'] = 'form-control datepicker'
			#form.fields['sdate'].input_formats=['%d-%m-%y', '%d-%m-%Y',]
			#form.fields['edate'].input_formats=['%d-%m-%y', '%d-%m-%Y',]
			return form
		return form_class(**self.get_form_kwargs())
	
	
#@method_decorator(permission_required('holiday.add_holiday'), name='dispatch')
class holiday_edit(UpdateView):
	model = holiday
	template_name = '_edit.html'
	success_url = '/holiday/list'
	fields = ['status', 'sdate', 'edate', 'user', 'message',]
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_404(self.model, id=self.kwargs['pk'])
		get_object_or_denied(self.request.user, 'holiday', 'R')
		return super(holiday_edit, self).dispatch(request, *args, **kwargs)


	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
			form = super(holiday_edit, self).get_form(form_class)
			#form.fields['sdate'].widget=forms.TextInput(attrs={'class':'form-control datepicker', 'data-dateformat': "dd-mm-yy"})
			#form.fields['edate'].widget.attrs['class'] = 'form-control datepicker'
			#form.fields['sdate'].widget=forms.TextInput(attrs={'class':'form-control datepicker', 'data-dateformat': "dd-mm-yy"})
			#form.fields['edate'].widget=forms.TextInput(attrs={'class':'form-control datepicker', 'data-dateformat': "dd-mm-yy"})
			form.fields['sdate'].widget.attrs['class'] = 'form-control datepicker'
			form.fields['edate'].widget.attrs['class'] = 'form-control datepicker'
			#form.fields['sdate'].input_formats=['%d-%m-%y', '%d-%m-%Y',]
			#form.fields['edate'].input_formats=['%d-%m-%y', '%d-%m-%Y',]
			return form
		return form_class(**self.get_form_kwargs())
	
	
	
	
	
	
	
	
	
