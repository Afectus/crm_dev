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


class library_book_add(CreateView):
	model = librarybook
	template_name = 'library_book_add.html'
	#form_class = Form_create_nickname
	success_url = '/library/book/list/?success=true'
	fields = ['name', 'desc', 'pict', 'sourcefile',]
	
	def dispatch(self, request, *args, **kwargs):
		return super(library_book_add, self).dispatch(request, *args, **kwargs)
		
	def get_success_url(self):
		return '/library/book/detail/%s' % (self.data.id)
	
	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.user = self.request.user
		instance.save()
		self.data = instance
		return super(library_book_add, self).form_valid(form)
					
class library_book_edit(UpdateView):
	model = librarybook
	template_name = 'library_book_edit.html'
	success_url = '/library/book/list/?success=true'
	fields = ['name', 'desc', 'pict', 'sourcefile',]
	
	def dispatch(self, request, *args, **kwargs):
		self.data=get_object_or_404(self.model, id=self.kwargs['pk'], user=request.user)
		return super(library_book_edit, self).dispatch(request, *args, **kwargs)

	def get_success_url(self):
		return '/library/book/detail/%s' % (self.data.id)	


class library_book_list(ListView):
	template_name = 'library_book_list.html'
	model = librarybook
	paginate_by = 60
	
	def dispatch(self, request, *args, **kwargs):
		return super(library_book_list, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(library_book_list, self).get_queryset()
		self.data = data #for get_context_data
		#data = data.filter(Q(user=self.request.user, status='close') | Q(type='free', status='close') | Q(executor__user=self.request.user, status='close')).distinct()
		return data
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(library_book_list, self).get_context_data(*args, **kwargs)
		#context_data.update({'task_create': self.data.filter(user=self.request.user, status='open'),})
		return context_data
		
	
class library_book_detail(CreateView):
	model = librarybookcomment
	template_name = 'library_book_detail.html'
	#form_class = Form_create_nickname
	success_url = '/library/book/list/?success=true'
	fields = ['message', 'pict', ]
	
	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(librarybook, id=self.kwargs['pk'])
		return super(library_book_detail, self).dispatch(request, *args, **kwargs)


	def get_context_data(self, *args, **kwargs):
		context_data = super(library_book_detail, self).get_context_data(*args, **kwargs)
		context_data.update({'liked': librarybooklike.objects.filter(librarybook__id=self.kwargs['pk'], user=self.request.user).exists(),})
		context_data.update({'object': self.data,})
		return context_data		
	
	def get_success_url(self):
		return '/library/book/detail/%s' % (self.data.id)
	
	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.librarybook = self.data
		instance.user = self.request.user
		instance.save()
		return super(library_book_detail, self).form_valid(form)
	
		
@csrf_exempt
def library_book_like(request, pk, value):
	if request.method == 'POST' or request.method == 'GET':
		res={'res': 0, 'data': u'Ошибка',}
		try:
			t=librarybook.objects.get(id=pk)
		except:
			pass
		else:
			lt=librarybooklike.objects.filter(librarybook__id=pk, user=request.user)
			if lt.exists():
				res = {'res': 1, 'liked': 1,}
				return HttpResponseRedirect('/library/book/detail/%s' % t.pk)
			else:
				librarybooklike.objects.create(librarybook=t, user=request.user, value=value).save()
				res = {'res': 1, 'liked': 0,}
				return HttpResponseRedirect('/library/book/detail/%s' % t.pk)
	return HttpResponse(json.dumps(res), content_type='application/json')
	