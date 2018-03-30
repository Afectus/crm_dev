# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
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
from notify.models import *
from django.urls import reverse


class instructions_detail(DetailView):
	model = instructions
	template_name = 'instructions_detail.html'

class instructions_detail_print(DetailView):
	model = instructions
	template_name = 'instructions_detail_print.html'

	# def get_object(self, queryset=None):
	#	  self.data=super(instructions_edit, self).get_object()
	#	  if self.data.user != self.request.user:
	#		  raise PermissionDenied
	#	  return self.data

	#def get_success_url(self):
	#	return reverse('instructions:instructions_list')




class instructions_add(CreateView):
	model = instructions
	template_name = 'instructions_add.html'
	fields = ['name', 'addressee', 'file', 'fulltext', ]

	def form_valid(self, form):
		instance = form.save(commit=False)
		# instance.user = self.request.user
		instance.save()
		return super(instructions_add, self).form_valid(form)

	def get_success_url(self):
		return reverse('instructions:instructions_list')

class instructions_list(ListView): 
	template_name = 'instructions_list.html' 
	model = instructions
	# paginate_by = 6

	# def dispatch(self, request, *args, **kwargs): 
	#	  return super(instructions_list, self).dispatch(request, *args, **kwargs) 

	# def get_queryset(self): 
	#	  data=super(instructions_list, self).get_queryset() 
	#	  data = data.filter(user=self.request.user) #for get_context_data 
	#	  return data 

class instructions_edit(UpdateView):
	model = instructions
	template_name = '_edit2.html'
	fields = ['name', 'addressee', 'file', 'fulltext', ]

	# def get_form(self, form_class=None):
		# if form_class is None:
			# form_class = self.get_form_class()
			# form = super(create_usertask, self).get_form(form_class)
			# form.fields['etime'].widget=forms.TextInput(attrs={'class':'mydatepicker1'})
			# form.fields['etime'].input_formats=['%d-%m-%y', '%d-%m-%Y',]
			# form.fields['etime'].help_text=('формат %d-%m-%Y')
			# return form
		# return form_class(**self.get_form_kwargs())

	# def get_object(self, queryset=None):
	#	  self.data=super(instructions_edit, self).get_object()
	#	  if self.data.user != self.request.user:
	#		  raise PermissionDenied
	#	  return self.data

	def get_success_url(self):
		return reverse('instructions:instructions_list')


class instructions_del(DeleteView): 
	template_name = '_confirm_delete.html' 
	model = instructions

	def dispatch(self, request, *args, **kwargs):
		return super(instructions_del, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(instructions_del, self).get_context_data(**kwargs)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = reverse('instructions:instructions_list')
		return context

	def get_success_url(self):
		return reverse('instructions:instructions_list')
