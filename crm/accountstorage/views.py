# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.http import Http404
from django.contrib.auth.models import User

import time
import requests
import datetime
from django.utils import timezone
# Create your views here.
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView

from django.views.generic import DetailView, DeleteView
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView

from dj.views import *
from .models import *
from django.urls import reverse


# Create your views here.
class accountstorage_add(CreateView):
	model = accountstorage
	template_name = '_edit2.html'
	fields = ['name', 'login', 'password', 'comment', 'aclu']
  
	# def form_valid(self, form):
		# instance = form.save(commit=False)
		# instance.user = self.request.user
		# instance.save()
		# return super(accountstorage_add, self).form_valid(form)

	def get_success_url(self):
		return reverse('accountstorage:accountstorage_list')

#@method_decorator(permission_required('worktask.add_usertask'), name='dispatch') 
class accountstorage_list(ListView): 
	template_name = 'accountstorage_list.html' 
	model = accountstorage 
	paginate_by = 20

	def dispatch(self, request, *args, **kwargs): 
		return super(accountstorage_list, self).dispatch(request, *args, **kwargs) 

	def get_queryset(self): 
		data=super(accountstorage_list, self).get_queryset() 
		# data = data.filter(user=self.request.user) #for get_context_data 
		return data 


class accountstorage_edit(UpdateView):
	model = accountstorage
	template_name = '_edit2.html'
	fields = ['name', 'login', 'password', 'comment', 'aclu']
  
	def get_object(self, queryset=None):
		self.data=super(accountstorage_edit, self).get_object()
		aclcheck=self.data.aclu.filter(user=self.request.user, type='U')
		if not aclcheck.exists():
			raise Http404()
		return self.data

	def get_success_url(self):
		return reverse('accountstorage:accountstorage_list')

class accountstorage_detail(DetailView): 
	template_name = 'accountstorage_detail.html' 
	model = accountstorage
	fields = ['name', 'login', 'password', 'comment', 'aclu']

	def dispatch(self, request, *args, **kwargs):
		#self.data = get_object_or_404(accountstorage, id=self.kwargs['pk'])
		return super(accountstorage_detail, self).dispatch(request, *args, **kwargs)
	
	def get_object(self, queryset=None):
		self.data=super(accountstorage_detail, self).get_object()
		aclcheck=self.data.aclu.filter(user=self.request.user, type='R')
		if not aclcheck.exists() and self.request.user.id != 1 and self.request.user.id != 2:
			raise Http404()
		return self.data

	# def form_valid(self, form):
	#	  instance = form.save(commit=False)
	#	  instance.user = self.request.user
	#	  # instance.project = self.data
	#	  instance.save()
	#	  # self.data.projectcomment.add(instance)
	#	  return super(accountstorage_detail, self).form_valid(form)

	def get_success_url(self):
		return reverse('accountstorage:accountstorage_detail',args=[self.data.id])