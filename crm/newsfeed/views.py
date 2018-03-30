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

from django import forms

from dj.views import *
from .models import *
from newsfeed.models import *
from notify.models import *
from django.urls import reverse
from panel.models import profileuser
from telegramtemplate.models import *


# Получаем шаблон из бд
def get_message(typetemplate, user, path):
	# Переменные шаблона:<br>
	# (today) - Сегодняшняя дата<br>
	# (user) - Пользователь<br>
	# (url) - Ссылка на объект (crm.babah24.ru)<br>
	#today = datetime.date.today()
	now = datetime.datetime.now()

	fullname = user.first_name + " " + user.last_name

	t = telegramtemplate.objects.filter(name=typetemplate)
	t = t.first()
	message = t.message
	message = message.replace('(today)', now.strftime('%d-%m-%Y %H:%M:%S'))
	message = message.replace('(user)', str(fullname))
	message = message.replace('(url)', 'crm.babah24.ru%s' % path)
	
	return message

# отправляем сообщения в очередь
def send_message(iuser, message):
	nh=notifyhandler.objects.get(name='telegram_chat')
	nq=notifyqueue.objects.create(handler=nh, value=message)

#### Форма добавления файлов
class FileFieldForm(forms.Form):
	file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

###############################3

class news_detail(DetailView):
	model = news
	template_name = 'news_detail.html'

	# def dispatch(self, request, *args, **kwargs): 
	# 	self.data=super(news_detail, self).get_object()
	# 	if profileuser.objects.filter(user=self.request.user).first() not in self.data.readers.all():
	# 		raise PermissionDenied
	# 	return super(news_detail, self).dispatch(request, *args, **kwargs) 

	#def get_success_url(self):
	#	return reverse('newsfeed:news_list')

class news_add(CreateView):
	model = news
	template_name = 'news_add.html'
	fields = ['name', 'text']

	# def get_form(self, form_class=None):
	# 	if form_class is None:
	# 		form_class = self.get_form_class()
	# 		form = super(news_add, self).get_form(form_class)
	# 		form.fields['readers'].queryset = profileuser.objects.filter(status='on').exclude(user__username='telegram_chat').exclude(user__username='telegram_chat2').exclude(user__username='telegram_test')
	# 		return form
	# 	return form_class(**self.get_form_kwargs())

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.user = profileuser.objects.filter(user=self.request.user).first()
		# instance.readers = profileuser.objects.filter(status='on')
		instance.save()

		path = reverse('newsfeed:news_detail', args=[instance.id])
		# print(path)
		value_chat = get_message('news_add', instance.user.user, path)
		send_message(User.objects.get(username='telegram_chat'), value_chat)

		return super(news_add, self).form_valid(form)

	def get_success_url(self):
		return reverse('newsfeed:news_list')

class news_list(ListView): 
	template_name = 'news_list.html' 
	model = news
	# paginate_by = 6

	# def dispatch(self, request, *args, **kwargs): 
	#	  return super(news_list, self).dispatch(request, *args, **kwargs) 

	# def get_queryset(self): 
	# 	data=super(news_list, self).get_queryset() 
	# 	data = data.filter(readers__user=self.request.user) #for get_context_data 
	# 	return data

class news_edit(UpdateView):
	model = news
	template_name = '_edit2.html'
	fields = ['name', 'text']

	def get_object(self, queryset=None):
		self.data=super(news_edit, self).get_object()
		if self.data.user.user != self.request.user:
			raise PermissionDenied
		return self.data
	
	# def get_form(self, form_class=None):
	# 	if form_class is None:
	# 		form_class = self.get_form_class()
	# 		form = super(news_edit, self).get_form(form_class)
	# 		form.fields['readers'].queryset = profileuser.objects.filter(status='on').exclude(user__username='telegram_chat').exclude(user__username='telegram_chat2').exclude(user__username='telegram_test')
	# 		return form
	# 	return form_class(**self.get_form_kwargs())
	
	def get_success_url(self):
		return reverse('newsfeed:news_list')


class news_del(DeleteView): 
	template_name = '_confirm_delete.html' 
	model = news

	def dispatch(self, request, *args, **kwargs):
		return super(news_del, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(news_del, self).get_context_data(**kwargs)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = reverse('newsfeed:news_list')
		return context

	def get_success_url(self):
		return reverse('newsfeed:news_list')



class news_pict_add(FormView): 
	form_class = FileFieldForm
	template_name = 'news_file_add.html'	 # Replace with your template.

	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(news, id=self.kwargs['pk'], user__user=self.request.user)
		return super(news_pict_add, self).dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		files = request.FILES.getlist('file_field')

		if form.is_valid():
			for f in files:
				instance = newspicture.objects.create(pict=f, desc=f.name, news=self.data)
				instance.save()
			return self.form_valid(form)
		else:
			
			return self.form_invalid(form)

	def get_success_url(self):
		return reverse('newsfeed:news_detail',args=[self.data.id])

class news_pict_del(DeleteView): 
	template_name = '_confirm_delete.html' 
	model = newspicture

	def dispatch(self, request, *args, **kwargs):
		return super(news_pict_del, self).dispatch(request, *args, **kwargs)
	
	def get_object(self, queryset=None):
		self.data=super(news_pict_del, self).get_object()
		if self.data.news.user.user != self.request.user:
			raise PermissionDenied
		return self.data
	
	def get_context_data(self, **kwargs):
		context = super(news_pict_del, self).get_context_data(**kwargs)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = reverse('newsfeed:news_detail',args=[self.data.news.id])
		return context

	def get_success_url(self):
		return reverse('newsfeed:news_detail',args=[self.data.news.id])
