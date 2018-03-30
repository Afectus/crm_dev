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

class pictgallery_add(CreateView):
	model = pictgallery
	template_name = 'pictgallery_add.html'
	fields = ['desc', 'pict']

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.user = profileuser.objects.filter(user=self.request.user).first()
		instance.save()
		return super(pictgallery_add, self).form_valid(form)

	def get_success_url(self):
		return reverse('pictgallery:pictgallery_list')

class pictgallery_list(ListView): 
	template_name = 'pictgallery_list.html' 
	model = pictgallery
	# paginate_by = 6

	# def dispatch(self, request, *args, **kwargs): 
	#	 return super(pictgallery_list, self).dispatch(request, *args, **kwargs) 

	def get_queryset(self): 
		data=super(pictgallery_list, self).get_queryset() 
		data = data.filter(user=profileuser.objects.filter(user=self.request.user).first()) #for get_context_data 
		return data 

class pictgallery_edit(UpdateView):
	model = pictgallery
	template_name = 'pictgallery_add.html'
	fields = ['desc', 'pict']

	def get_object(self, queryset=None):
		self.data=super(pictgallery_edit, self).get_object()
		if self.data.user != profileuser.objects.filter(user=self.request.user).first():
			raise PermissionDenied
		return self.data

	def get_success_url(self):
		return reverse('pictgallery:pictgallery_list')


class pictgallery_del(DeleteView): 
	template_name = '_confirm_delete.html' 
	model = pictgallery

	def dispatch(self, request, *args, **kwargs):
		self.data=super(pictgallery_del, self).get_object()
		print(profileuser.objects.filter(user=self.request.user).first())
		if self.data.user != profileuser.objects.filter(user=self.request.user).first():
			raise PermissionDenied
		return super(pictgallery_del, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(pictgallery_del, self).get_context_data(**kwargs)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = reverse('pictgallery:pictgallery_list')
		return context

	def get_success_url(self):
		return reverse('pictgallery:pictgallery_list')
