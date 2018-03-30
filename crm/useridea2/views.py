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
from django.urls import reverse
from math import ceil


from django.db.models import Max, Sum, Count
from django.db.models import Q, F

from ckeditor.widgets import CKEditorWidget

from dj.views import *
from acl.views import *

from django.core.mail import send_mail


from node.templatetags.nodetag import *

from node.models import *
from order.models import *
from panel.form import *
from panel.models import *
from panel.form import *
from sms.views import *
from sms.models import *
from bitrix.models import *
from worktask.models import *
from notify.models import *
from telegramtemplate.models import *
from useridea2.models import *

import logging
log = logging.getLogger(__name__)

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

############################
class ideasection_add(CreateView):
	model = ideasection
	template_name = 'ideasection_add.html'
	fields = ['name']

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'ideasection', 'A')
		return super(ideasection_add, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		instance = form.save(commit=False)
		# instance.user = self.request.user
		instance.save()
		return super(ideasection_add, self).form_valid(form)

	def get_success_url(self):
		
		return reverse('useridea2:ideasection_list')

class ideasection_list(ListView): 
	template_name = 'ideasection_list.html' 
	model = ideasection
	# paginate_by = 6

	# def dispatch(self, request, *args, **kwargs): 
	#	  return super(ideasection_list, self).dispatch(request, *args, **kwargs) 

	# def get_queryset(self): 
	#	  data=super(ideasection_list, self).get_queryset() 
	#	  data = data.filter(user=self.request.user) #for get_context_data 
	#	  return data 

class ideasection_edit(UpdateView):
	model = ideasection
	template_name = '_edit2.html'
	fields = ['name']

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
	#	  self.data=super(ideasection_edit, self).get_object()
	#	  if self.data.user != self.request.user:
	#		  raise PermissionDenied
	#	  return self.data

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'ideasection', 'A')
		return super(ideasection_edit, self).dispatch(request, *args, **kwargs)

	def get_success_url(self):
		return reverse('useridea2:ideasection_list')


class ideasection_del(DeleteView): 
	template_name = '_confirm_delete.html' 
	model = ideasection

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'ideasection', 'A')
		return super(ideasection_del, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(ideasection_del, self).get_context_data(**kwargs)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = reverse('useridea2:ideasection_list')
		return context

	def get_success_url(self):
		return reverse('useridea2:ideasection_list')


class useridea_add(CreateView):
	model = useridea
	template_name = '_edit2.html'
	#form_class = Form_create_nickname
	fields = ['section', 'name', 'message']
	
	# def dispatch(self, request, *args, **kwargs):
	# 	return super(create_useridea, self).dispatch(request, *args, **kwargs)
	
	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.user = profileuser.objects.filter(user=self.request.user).first()
		instance.save()
		self.data = instance
		
		path = reverse('useridea2:useridea_detail', args=[self.data.id])
		print(path)
		value_chat = get_message('useridea_add', self.data.user.user, path)
		send_message(User.objects.get(username='telegram_chat'), value_chat)

		return super(useridea_add, self).form_valid(form)
	
	def get_success_url(self):
		return reverse('useridea2:ideasection_list')

class useridea_edit(UpdateView):
	model = useridea
	template_name = '_edit2.html'
	fields = [ 'name', 'message', ]
	
	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(self.model, id=self.kwargs['pk'], user__user=request.user)
		return super(useridea_edit, self).dispatch(request, *args, **kwargs)

	def get_success_url(self):
		return reverse('useridea2:useridea_detail', args=[self.data.id])

# class useridea_del(DeleteView):
# 	model = useridea
# 	template_name = '_confirm_delete.html'
	
# 	def dispatch(self, request, *args, **kwargs):
# 		self.data = get_object_or_404(useridea, id=self.kwargs['pk'], user__user=self.request.user)
# 		return super(useridea_edit, self).dispatch(request, *args, **kwargs)

# 	def form_valid(self, form):
# 		self.data.pict.all().delete()
# 		return super(useridea_add, self).form_valid(form)

# 	def get_success_url(self):
# 		return reverse('useridea2:useridea_detail', args=[self.data.id])


class useridea_pict_add(FormView): 
	form_class = FileFieldForm
	template_name = 'useridea_file_add.html'	 # Replace with your template.

	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(useridea, id=self.kwargs['pk'], user__user=self.request.user)
		return super(useridea_pict_add, self).dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		files = request.FILES.getlist('file_field')

		if form.is_valid():
			for f in files:
				instance = picture.objects.create(pict=f, desc=f.name)
				instance.save()
				self.data.pict.add(instance)
			return self.form_valid(form)
		else:
			
			return self.form_invalid(form)

	def get_success_url(self):
		return reverse('useridea2:useridea_detail',args=[self.data.id])

class useridea_pict_del(DeleteView): 
	template_name = '_confirm_delete.html' 
	model = picture

	def dispatch(self, request, *args, **kwargs):
		return super(useridea_pict_del, self).dispatch(request, *args, **kwargs)
	
	def get_object(self, queryset=None):
		self.data=super(useridea_pict_del, self).get_object()
		if self.data.useridea_set.all().first().user.user != self.request.user:
			raise PermissionDenied
		return self.data
	
	def get_context_data(self, **kwargs):
		context = super(useridea_pict_del, self).get_context_data(**kwargs)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = reverse('useridea2:useridea_detail',args=[self.data.useridea_set.all().first().id])
		return context

	def get_success_url(self):
		return reverse('useridea2:useridea_detail',args=[self.data.useridea_set.all().first().id])


class useridea_file_add(FormView): 
	form_class = FileFieldForm
	template_name = 'useridea_file_add.html'	 # Replace with your template.

	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(useridea, id=self.kwargs['pk'], user__user=self.request.user)
		return super(useridea_file_add, self).dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		files = request.FILES.getlist('file_field')

		if form.is_valid():
			for f in files:
				instance = file.objects.create(sourcefile=f, desc=f.name)
				instance.save()
				self.data.file.add(instance)
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def get_success_url(self):
		return reverse('useridea2:useridea_detail',args=[self.data.id])
	
class useridea_file_del(DeleteView): 
	template_name = '_confirm_delete.html'
	model = file

	def dispatch(self, request, *args, **kwargs):
		return super(useridea_file_del, self).dispatch(request, *args, **kwargs)
	
	def get_object(self, queryset=None):
		self.data=super(useridea_file_del, self).get_object()
		if self.data.useridea_set.all().first().user.user != self.request.user:
			raise PermissionDenied
		return self.data

	def get_context_data(self, **kwargs):
		context = super(useridea_file_del, self).get_context_data(**kwargs)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = reverse('useridea2:useridea_detail',args=[self.data.useridea_set.all().first().id])
		return context


	def get_success_url(self):
		return reverse('useridea2:useridea_detail',args=[self.data.useridea_set.all().first().id])


### операции с комментариями
	
class useridea_detail(CreateView):
	model = commentidea
	template_name = 'useridea2_detail.html'
	fields = ['message']
	
	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(useridea, id=self.kwargs['pk'])
		return super(useridea_detail, self).dispatch(request, *args, **kwargs)
	
	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.useridea = self.data
		instance.user = profileuser.objects.filter(user=self.request.user).first()
		instance.save()

		path = reverse('useridea2:useridea_detail', args=[self.data.id])
		# print(path)
		value_chat = get_message('useridea_comment_add', instance.user.user, path)
		send_message(User.objects.get(username='telegram_chat'), value_chat)

		return super(useridea_detail, self).form_valid(form)
	
	def get_context_data(self, *args, **kwargs):
		context_data = super(useridea_detail, self).get_context_data(*args, **kwargs)
		context_data.update({'liked': likeidea.objects.filter(useridea=self.data, user__user=self.request.user).exists(),})
		context_data.update({'object': self.data,})
		#
		# context_data.update({'file': fileidea.objects.filter(useridea=self.data, type='file'),})
		# context_data.update({'image': fileidea.objects.filter(useridea=self.data, type='image'),})
		return context_data
	
	def get_success_url(self):
		return reverse('useridea2:useridea_detail', args=[self.data.id])

class commentidea_edit(UpdateView):
	model = commentidea
	template_name = '_edit2.html'
	fields = ['message']

	def dispatch(self, request, *args, **kwargs):
		return super(commentidea_edit, self).dispatch(request, *args, **kwargs)
	
	def get_object(self, queryset=None):
		self.data=super(commentidea_edit, self).get_object()
		if self.data.user.user != self.request.user:
			raise PermissionDenied
		return self.data

	def get_success_url(self):
		return reverse('useridea2:useridea_detail',args=[self.data.useridea.id])

class commentidea_del(DeleteView): 
	template_name = '_confirm_delete.html' 
	model = commentidea

	def dispatch(self, request, *args, **kwargs):
		return super(commentidea_del, self).dispatch(request, *args, **kwargs)
	
	def get_object(self, queryset=None):
		self.data=super(commentidea_del, self).get_object()
		if self.data.user.user != self.request.user:
			raise PermissionDenied
		return self.data
	
	def get_context_data(self, **kwargs):
		context = super(commentidea_del, self).get_context_data(**kwargs)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = reverse('useridea2:useridea_detail',args=[self.data.useridea.id])
		return context

	def get_success_url(self):
		return reverse('useridea2:useridea_detail',args=[self.data.useridea.id])

class commentidea_pict_add(FormView):
	form_class = FileFieldForm
	template_name = 'useridea_file_add.html'	 # Replace with your template.

	def dispatch(self, request, *args, **kwargs):
		self.comment = get_object_or_404(commentidea, id=self.kwargs['pk'], user__user=self.request.user)
		return super(commentidea_pict_add, self).dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		files = request.FILES.getlist('file_field')

		if form.is_valid():
			for f in files:
				instance = picture.objects.create(pict=f, desc=f.name)
				instance.save()
				self.comment.pict.add(instance)
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def get_success_url(self):
		return reverse('useridea2:useridea_detail',args=[self.comment.useridea.id])
	
class commentidea_pict_del(DeleteView):
	model = picture
	template_name = '_confirm_delete.html'
	
	def dispatch(self, request, *args, **kwargs):
		return super(commentidea_pict_del, self).dispatch(request, *args, **kwargs)

	def get_object(self, queryset=None):
		self.data=super(commentidea_pict_del, self).get_object()
		if self.data.commentidea_set.all().first().user.user != self.request.user:
			raise PermissionDenied
		return self.data
	
	def get_context_data(self, **kwargs):
		context = super(commentidea_pict_del, self).get_context_data(**kwargs)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = reverse('useridea2:useridea_detail',args=[self.data.commentidea_set.all().first().useridea.id])
		return context

	def get_success_url(self):
		return reverse('useridea2:useridea_detail',args=[self.data.commentidea_set.all().first().useridea.id])

class commentidea_file_add(FormView):
	form_class = FileFieldForm
	template_name = 'useridea_file_add.html'	 # Replace with your template.

	def dispatch(self, request, *args, **kwargs):
		self.comment = get_object_or_404(commentidea, id=self.kwargs['pk'], user__user=request.user)
		return super(commentidea_file_add, self).dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		files = request.FILES.getlist('file_field')

		if form.is_valid():
			for f in files:
				instance = file.objects.create(sourcefile=f, desc=f.name)
				instance.save()
				self.comment.file.add(instance)
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def get_success_url(self):
		return reverse('useridea2:useridea_detail',args=[self.comment.useridea.id])

class commentidea_file_del(DeleteView): 
	template_name = '_confirm_delete.html' 
	model = file

	def dispatch(self, request, *args, **kwargs):
		return super(commentidea_file_del, self).dispatch(request, *args, **kwargs)

	def get_object(self, queryset=None):
		self.data=super(commentidea_file_del, self).get_object()
		if self.data.commentidea_set.all().first().user.user != self.request.user:
			raise PermissionDenied
		return self.data

	def get_context_data(self, **kwargs):
		context = super(commentidea_file_del, self).get_context_data(**kwargs)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = reverse('useridea2:useridea_detail',args=[self.data.commentidea_set.all().first().useridea.id])
		return context

	def get_success_url(self):
		return reverse('useridea2:useridea_detail',args=[self.data.commentidea_set.all().first().useridea.id])


#### like sdf sdf sdf 

# @csrf_exempt
def likeidea_add(request, pk, value):
	if request.method == 'POST' or request.method == 'GET':
		res={'res': 0, 'data': u'Ошибка',}
		try:
			t=useridea.objects.get(id=pk)
		except:
			pass
		else:
			lt=likeidea.objects.filter(useridea__id=pk, user=profileuser.objects.filter(user=request.user).first())
			if lt.exists():
				res = {'res': 1, 'liked': 1,}
				return HttpResponseRedirect(reverse('useridea2:useridea_detail', args=[t.id]))
				# return HttpResponseRedirect('/useridea/detail/%s' % t.pk)
			else:
				li = likeidea.objects.create(useridea=t, user=profileuser.objects.filter(user=request.user).first(), value=value)
				li.save()
				res = {'res': 1, 'liked': 0,}

				# t.rating = ceil((t.rating + int(li.value))/(t.likeidea_set.all().count()))
				t.rating = ceil(t.rating + int(li.value))
				t.save()
				return HttpResponseRedirect(reverse('useridea2:useridea_detail', args=[t.id]))
				# return HttpResponseRedirect('/useridea/detail/%s' % t.pk)
	return HttpResponse(json.dumps(res), content_type='application/json')
	


class useridea_change_status(UpdateView):
	model = useridea
	template_name = '_edit2.html'
	fields = ['status']
	#success_url = reverse('useridea:useridea_list')

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'ideasection', 'A')
		self.data=super(useridea_change_status, self).get_object()
		return super(useridea_change_status, self).dispatch(request, *args, **kwargs)
	
	def get_success_url(self):
		return reverse('useridea2:useridea_detail',args=[self.data.id])