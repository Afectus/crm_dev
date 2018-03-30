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
from django.db.models import Q, F

from ckeditor.widgets import CKEditorWidget

from dj.views import *
from acl.views import *

from django.core.mail import send_mail


from node.templatetags.nodetag import *

from node.models import *
from .models import *
from .diagram import *

import logging
log = logging.getLogger(__name__)


######### bizplist

class bizplist_list(ListView):
	template_name = "bizplist_list.html"
	model = bizplist
	paginate_by = 40

	def dispatch(self, request, *args, **kwargs):
		#get_object_or_denied(self.request.user, 'bizprocessshow', 'R')
		return super(bizplist_list, self).dispatch(request, *args, **kwargs)
	
	def get_queryset(self):
		data=super(bizplist_list, self).get_queryset().order_by('-id')
		return data
	
	def get_context_data(self, *args, **kwargs):
		context_data = super(bizplist_list, self).get_context_data(*args, **kwargs)
		#context_data.update({'goodfix': goodfix.objects.filter(status='open').order_by('-id')})
		return context_data


class bizplist_add(CreateView):	
	template_name = "_edit2.html"
	model = bizplist
	fields = ['name']
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'bizprocess', 'R')
		return super(bizplist_add, self).dispatch(request, *args, **kwargs)

	def get_success_url(self):
		return reverse('bizprocess:bizplist_list')


class bizplist_edit(UpdateView):
	template_name = "_edit2.html"
	model = bizplist
	fields = ['name']
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'bizprocess', 'U')
		return super(bizplist_edit, self).dispatch(request, *args, **kwargs)
	
	def get_success_url(self):
		return reverse('bizprocess:bizplist_list')

# class bizplist_detail уже есть в diagram.py!!!
class bizplist_table_detail(bizplist_detail):	
	template_name = "bizpstep_table_detail.html"

######### bizpstep

class bizpstep_add_parent(CreateView):	
	template_name = "_edit2.html"
	model = bizpstep
	fields = ['name', 'sort', 'head', 'bizpstepexecutor', 'desc', 'fulltext']
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'bizprocess', 'R')
		self.data = get_object_or_404(bizplist, id=self.kwargs['pk'])
		return super(bizpstep_add_parent, self).dispatch(request, *args, **kwargs)
	
	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.process = self.data
		instance.save()
		return super(bizpstep_add_parent, self).form_valid(form)

	def get_success_url(self):
		return reverse('bizprocess:bizplist_table_detail', args=[self.data.id])

class bizpstep_add_child(CreateView):	
	template_name = "_edit2.html"
	model = bizpstep
	fields = ['name', 'sort', 'head', 'bizpstepexecutor', 'desc', 'fulltext']
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'bizprocess', 'R')
		self.data = get_object_or_404(bizpstep, id=self.kwargs['pk'])
		return super(bizpstep_add_child, self).dispatch(request, *args, **kwargs)
	
	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.parent = self.data
		instance.process = self.data.process
		instance.save()
		return super(bizpstep_add_child, self).form_valid(form)

	def get_success_url(self):
		return reverse('bizprocess:bizpstep_table_detail', args=[self.data.id])


class bizpstep_table_detail(bizpstep_detail):	
	template_name = "bizpstep_table_detail.html"


class bizpstep_del(DeleteView):	
	template_name = "_confirm_delete.html"
	model = bizpstep
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'bizprocess', 'R')
		return super(bizpstep_del, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(bizpstep_del, self).get_context_data(**kwargs)
		context['msg'] = u'Вы уверены, что хотите удалить?'
		context['back_url'] = reverse('bizprocess:bizplist_list')
		return context

	def get_success_url(self):
		return reverse('bizprocess:bizplist_list')

class bizpstep_del_parent(DeleteView):	
	template_name = "_confirm_delete.html"
	model = bizpstep
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'bizprocess', 'R')
		self.data = get_object_or_404(bizpstep, id=self.kwargs['pk'])
		return super(bizpstep_del_parent, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(bizpstep_del_parent, self).get_context_data(**kwargs)
		context['msg'] = u'Вы уверены, что хотите удалить?'
		context['back_url'] = reverse('bizprocess:bizplist_table_detail', args=[self.data.process.id])
		return context

	def get_success_url(self):
		return reverse('bizprocess:bizplist_table_detail', args=[self.data.process.id])

class bizpstep_del_child(DeleteView):	
	template_name = "_confirm_delete.html"
	model = bizpstep
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'bizprocess', 'R')
		self.data = get_object_or_404(bizpstep, id=self.kwargs['pk'])
		return super(bizpstep_del_child, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(bizpstep_del_child, self).get_context_data(**kwargs)
		context['msg'] = u'Вы уверены, что хотите удалить?'
		context['back_url'] = reverse('bizprocess:bizpstep_table_detail', args=[self.data.parent.id])
		return context

	def get_success_url(self):
		return reverse('bizprocess:bizpstep_table_detail', args=[self.data.parent.id])

class bizpstep_edit(UpdateView):	
	template_name = "_edit2.html"
	model = bizpstep
	fields = ['name', 'sort', 'head', 'bizpstepexecutor', 'desc', 'fulltext']
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'bizprocess', 'R')
		return super(bizpstep_edit, self).dispatch(request, *args, **kwargs)
	
	def get_success_url(self):
		return reverse('bizprocess:bizplist_list')

class bizpstep_edit_parent(UpdateView):	
	template_name = "_edit2.html"
	model = bizpstep
	fields = ['name', 'sort', 'head', 'bizpstepexecutor', 'desc', 'fulltext']
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'bizprocess', 'R')
		self.data = get_object_or_404(bizpstep, id=self.kwargs['pk'])
		return super(bizpstep_edit_parent, self).dispatch(request, *args, **kwargs)
	
	def get_success_url(self):
		return reverse('bizprocess:bizplist_table_detail', args=[self.data.process.id])

class bizpstep_edit_child(UpdateView):	
	template_name = "_edit2.html"
	model = bizpstep
	fields = ['name', 'sort', 'head', 'bizpstepexecutor', 'desc', 'fulltext']
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'bizprocess', 'R')
		self.data = get_object_or_404(bizpstep, id=self.kwargs['pk'])
		return super(bizpstep_edit_child, self).dispatch(request, *args, **kwargs)
	
	def get_success_url(self):
		return reverse('bizprocess:bizpstep_table_detail', args=[self.data.parent.id])
