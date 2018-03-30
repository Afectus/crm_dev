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
from acl.views import get_object_or_denied

from .models import *

from notify.models import *
from django.urls import reverse

import logging
log = logging.getLogger(__name__)



class organazier_calendar(TemplateView):
	template_name = 'organazier_calendar.html'
	
	def get_context_data(self, **kwargs):
		context = super(organazier_calendar, self).get_context_data(**kwargs)
		context['object_list'] = organizer.objects.filter(user=self.request.user)
		return context

class organizer_add(CreateView):
	model = organizer
	template_name = '_edit2.html'
	fields = ['name', 'stime', 'etime', 'desc']

	# def get_form(self, form_class=None):
	# 	if form_class is None:
	# 		form_class = self.get_form_class()
	# 		form = super(organizer_add, self).get_form(form_class)
	# 		form.fields['stime'].widget.attrs['class'] = 'form-control datetimepicker'
	# 		form.fields['etime'].widget.attrs['class'] = 'form-control datetimepicker'
	# 		#form.fields['sdate'].input_formats=['%d-%m-%y', '%d-%m-%Y',]
	# 		#form.fields['edate'].input_formats=['%d-%m-%y', '%d-%m-%Y',]
	# 		return form
	# 	return form_class(**self.get_form_kwargs())

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.user = self.request.user
		instance.save()
		return super(organizer_add, self).form_valid(form)

	def get_success_url(self):
		return reverse('organizer:organizer_list')

class organizer_list(ListView): 
	template_name = 'organizer_list.html' 
	model = organizer
	# paginate_by = 6

	def dispatch(self, request, *args, **kwargs): 
		 return super(organizer_list, self).dispatch(request, *args, **kwargs) 

	def get_queryset(self): 
		data=super(organizer_list, self).get_queryset() 
		data = data.filter(user=self.request.user) #for get_context_data 
		return data 

class organizer_edit(UpdateView):
	model = organizer
	template_name = '_edit2.html'
	fields = ['name', 'stime', 'etime', 'desc']

	def get_object(self, queryset=None):
		self.data=super(organizer_edit, self).get_object()
		if self.data.user != self.request.user:
			raise PermissionDenied
		return self.data

	def get_success_url(self):
		return reverse('organizer:organizer_list')


class organizer_del(DeleteView): 
	template_name = '_confirm_delete.html' 
	model = organizer

	def dispatch(self, request, *args, **kwargs):
		self.data=super(organizer_del, self).get_object()
		if self.data.user != self.request.user:
			raise PermissionDenied
		return super(organizer_del, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(organizer_del, self).get_context_data(**kwargs)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = reverse('organizer:organizer_list')
		return context

	def get_success_url(self):
		return reverse('organizer:organizer_list')
	
	