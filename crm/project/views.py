# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse
from django.http import Http404
from django.contrib.auth.models import User

from django import forms

import time
import requests
import datetime
from django.utils import timezone
# Create your views here.
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView

from django.views.generic import DetailView, DeleteView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.core.files.storage import default_storage

from dj.views import *
from .models import *
from notify.models import *
from telegramtemplate.models import *
from django.urls import reverse


list_ext_pictures = ['jpg', 'jpeg', 'tif', 'tiff', 'png', 'bmp', 'gif', 'jpe']

class FileFieldForm(forms.Form):
	file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

def get_message(typetemplate, user, path, projectname, stepname):
	# Переменные шаблона:<br>
	# (today) - Сегодняшняя дата<br>
	# (user) - Пользователь<br>
	# (url) - Ссылка на объект (crm.babah24.ru)<br>
	# (projectname) - Название проекта<br>
	# (stepname) - Название этапа проекта<br>
	#today = datetime.date.today()
	now = datetime.datetime.now()

	fullname = '%s %s' % (user.first_name, user.last_name)
	
	t = telegramtemplate.objects.filter(name=typetemplate)
	t = t.first()
	message = t.message
	message = message.replace('(today)', now.strftime('%d-%m-%Y %H:%M:%S'))
	message = message.replace('(user)', fullname)
	message = message.replace('(url)', 'crm.babah24.ru%s' % path)
	message = message.replace('(projectname)', projectname)
	
	if stepname:
		message = message.replace('(stepname)', stepname)
	
	return message

def send_message(iuser, message):
	nh=notifyhandler.objects.get(name='telegram')
	try:
		nuk=notifyuserkey.objects.get(user=iuser, handler=nh)
	except:
		pass
	else: 
		nq=notifyqueue.objects.create(user=iuser, handler=nh, value=message)

def project_steps_json(request, pk):
	data = projectstep.objects.filter(project__id=pk)
	jdata = {}
	if data.exists():
		jdata = data
		# for i in data:
		# 	jdata['id'] = i.id
		# 	jdata['name'] = i.name
		# 	jdata['sort'] = i.sort
		# 	jdata['executor'] = i.executor
		# 	jdata['edate'] = i.edate

	return render_to_response('project_steps_json.html', {'object_list': jdata})

def projectstep_up(request, pk): 
	data = get_object_or_404(projectstep, id=pk)
	data.sort = data.sort + 100
	data.save()
	jdata = data
	return HttpResponse(status=204)

def projectstep_down(request, pk): 
	data = get_object_or_404(projectstep, id=pk)
	data.sort = data.sort - 100
	data.save()
	jdata = data
	return HttpResponse(status=204)

class project_add(CreateView):
	model = project
	template_name = '_edit2.html'
	fields = ['name', 'desc', 'executor', 'plansum']
	# success_url = reverse('project:project_list')

	# def dispatch(self, request, *args, **kwargs):
	#	  self.data = get_object_or_404(project, user=self.request.user)
	#	  return super(project_detail, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.user = self.request.user
		instance.save()
		self.data = instance
		return super(project_add, self).form_valid(form)

	def get_success_url(self):
		return reverse('project:project_list')

class project_list(ListView): 
	template_name = 'project_list.html' 
	model = project 
	paginate_by = 20

	def dispatch(self, request, *args, **kwargs): 
		return super(project_list, self).dispatch(request, *args, **kwargs) 

	def get_queryset(self): 
		data=super(project_list, self).get_queryset() 
		# data = data.filter(user=self.request.user) #for get_context_data 
		return data 

class project_edit(UpdateView):
	model = project
	template_name = '_edit2.html'
	fields = ['name', 'desc', 'executor', 'plansum']
	#success_url = reverse('project:project_list')

#	  def dispatch(self, request, *args, **kwargs):
#		  get_object_or_404(self.model, status='created', id=self.kwargs['pk'], user=request.user)
#		  return super(project_edit, self).dispatch(request, *args, **kwargs)
	
	def get_object(self, queryset=None):
		self.data=super(project_edit, self).get_object()
		if self.data.user != self.request.user:
			raise PermissionDenied
		return self.data

	def get_success_url(self):
		path_project = reverse('project:project_detail',args=[self.data.id])
		# отсылаем сообщение об изменении проекта
		if self.data.status == 'created':
			# проверяем шаблон и отправляем сообщения в чат
			value_chat = get_message('ttcpc', self.data.user, path_project, self.data.name, None)
			send_message(User.objects.get(username='telegram_chat'), value_chat)
			# проверяем шаблон и отправляем сообщения исполнителям
			value_executor = get_message('ttcpe', self.data.user, path_project, self.data.name, None)
			for e in self.data.executor.all().exclude(user=self.data.user):
				send_message(e.user, value_executor)
			
		return path_project

class project_changestatus(UpdateView):
	model = project
	template_name = '_edit2.html'
	fields = ['status']
	#success_url = reverse('project:project_list')

#	  def dispatch(self, request, *args, **kwargs):
#		  get_object_or_404(self.model, status='created', id=self.kwargs['pk'], user=request.user)
#		  return super(project_edit, self).dispatch(request, *args, **kwargs)
	
	def get_object(self, queryset=None):
		self.data=super(project_changestatus, self).get_object()
		if self.data.user != self.request.user:
			raise PermissionDenied
		return self.data

	def get_success_url(self):
		path_project = reverse('project:project_detail',args=[self.data.id])	   
		# отсылаем сообщение о публикации проекта
		if self.data.status == 'created':
			# проверяем шаблон и отправляем сообщения в чат
			value_chat = get_message('ttppc', self.data.user, path_project, self.data.name, None)
			send_message(User.objects.get(username='telegram_chat'), value_chat)
			# проверяем шаблон и отправляем сообщения исполнителям
			value_executor = get_message('ttppe', self.data.user, path_project, self.data.name, None)
			for e in self.data.executor.all().exclude(user=self.data.user):
				send_message(e.user, value_executor)
		#отсылаем сообщение об архивации проекта
		elif self.data.status == 'archived':
			# проверяем шаблон и отправляем сообщения в чат
			value_chat = get_message('ttapc', self.data.user, path_project, self.data.name, None)
			send_message(User.objects.get(username='telegram_chat'), value_chat)
			# проверяем шаблон и отправляем сообщения исполнителям
			value_executor = get_message('ttape', self.data.user, path_project, self.data.name, None)
			for e in self.data.executor.all().exclude(user=self.request.user):
				send_message(e.user, value_executor)	
		return path_project

class project_detail(CreateView): 
	template_name = 'project_detail.html' 
	model = projectcomment
	fields = ['value']

	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(project, id=self.kwargs['pk'])
		return super(project_detail, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.user = self.request.user
		# instance.project = self.data
		instance.save()
		self.data.projectcomment.add(instance)

		if self.data.status == 'created':
			path_project = reverse('project:project_detail',args=[self.data.id])
			# проверяем шаблон и отправляем сообщения в чат
			value_chat = get_message('ttacp', self.request.user, path_project, self.data.name, None)
			send_message(User.objects.get(username='telegram_chat'), value_chat)
			# проверяем шаблон и отправляем сообщения исполнителям
			value_executor = get_message('ttacp', self.request.user, path_project, self.data.name, None)
			for e in self.data.executor.all().exclude(user=self.request.user):
				send_message(e.user, value_executor) 

		return super(project_detail, self).form_valid(form)

	def get_context_data(self, *args, **kwargs):
		context_data = super(project_detail, self).get_context_data(*args, **kwargs)
		context_data.update({'object': self.data,})
		return context_data

	def get_success_url(self):
		return reverse('project:project_detail',args=[self.data.id])

class project_pict_add(FormView): 
	form_class = FileFieldForm
	template_name = 'project_file_add.html'	 # Replace with your template.

	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(project, id=self.kwargs['pk'], user=self.request.user)
		return super(project_pict_add, self).dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		files = request.FILES.getlist('file_field')

		if form.is_valid():
			for f in files:
				instance = projectpict.objects.create(pict=f, desc=f.name)
				instance.save()
				self.data.pict.add(instance)
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def get_success_url(self):
		return reverse('project:project_detail',args=[self.data.id])

class project_pict_del(DeleteView): 
	template_name = '_confirm_delete.html' 
	model = projectpict

	def dispatch(self, request, *args, **kwargs):
		return super(project_pict_del, self).dispatch(request, *args, **kwargs)
	
	def get_object(self, queryset=None):
		self.data=super(project_pict_del, self).get_object()
		if self.data.project_set.all().first().user != self.request.user:
			raise PermissionDenied
		return self.data
	
	def get_context_data(self, **kwargs):
		context = super(project_pict_del, self).get_context_data(**kwargs)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = reverse('project:project_detail',args=[self.data.project_set.all().first().id])
		return context

	def get_success_url(self):
		return reverse('project:project_detail',args=[self.data.project_set.all().first().id])

# class FileFieldView(FormView):
#	  form_class = FileFieldForm
#	  template_name = 'project_file_add.html'  # Replace with your template.
#	  # success_url = '...'	 # Replace with your URL or reverse().

#	  def post(self, request, *args, **kwargs):
#		  form_class = self.get_form_class()
#		  form = self.get_form(form_class)
#		  files = request.FILES.getlist('file_field')

#		  if form.is_valid():
#			  self.data = get_object_or_404(project, id=self.kwargs['pk'], user=self.request.user)
#			  for f in files:
#				  instance = projectfile.objects.create(sourcefile=f, desc=f.name)
#				  instance.save()
#				  self.data.file.add(instance)
#			  return self.form_valid(form)
#		  else:
#			  return self.form_invalid(form)
	
	# def get_success_url(self):
	#	  return reverse('project:project_detail',args=[self.data.id])

class project_file_add(FormView): 
	form_class = FileFieldForm
	template_name = 'project_file_add.html'	 # Replace with your template.

	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(project, id=self.kwargs['pk'], user=self.request.user)
		return super(project_file_add, self).dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		files = request.FILES.getlist('file_field')

		if form.is_valid():
			for f in files:
				
				fileext = re.compile(r'^.*\.(?P<ext>\w+)$').match(f.name).group('ext')
				
				if fileext in list_ext_pictures:
					instance = projectpict.objects.create(pict=f, desc=f.name)
					instance.save()
					self.data.pict.add(instance)
				else:
					instance = projectfile.objects.create(sourcefile=f, desc=f.name)
					instance.save()
					self.data.file.add(instance)

			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def get_success_url(self):
		return reverse('project:project_detail',args=[self.data.id])
	
class project_file_del(DeleteView): 
	template_name = '_confirm_delete.html'
	model = projectfile

	def dispatch(self, request, *args, **kwargs):
		return super(project_file_del, self).dispatch(request, *args, **kwargs)
	
	def get_object(self, queryset=None):
		self.data=super(project_file_del, self).get_object()
		if self.data.project_set.all().first().user != self.request.user:
			raise PermissionDenied
		return self.data

	def get_context_data(self, **kwargs):
		context = super(project_file_del, self).get_context_data(**kwargs)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = reverse('project:project_detail',args=[self.data.project_set.all().first().id])
		return context


	def get_success_url(self):
		return reverse('project:project_detail',args=[self.data.project_set.all().first().id])

class projectcomment_edit(UpdateView):
	model = projectcomment
	template_name = '_edit2.html'
	fields = ['value']

	def dispatch(self, request, *args, **kwargs):
		return super(projectcomment_edit, self).dispatch(request, *args, **kwargs)
	
	def get_object(self, queryset=None):
		self.data=super(projectcomment_edit, self).get_object()
		if self.data.user != self.request.user:
			raise PermissionDenied
		return self.data

	def get_success_url(self):
		return reverse('project:project_detail',args=[self.data.project_set.all().first().id])

class projectcomment_del(DeleteView): 
	template_name = '_confirm_delete.html' 
	model = projectcomment

	def dispatch(self, request, *args, **kwargs):
		return super(projectcomment_del, self).dispatch(request, *args, **kwargs)
	
	def get_object(self, queryset=None):
		self.data=super(projectcomment_del, self).get_object()
		if self.data.user != self.request.user:
			raise PermissionDenied
		return self.data
	
	def get_context_data(self, **kwargs):
		context = super(projectcomment_del, self).get_context_data(**kwargs)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = reverse('project:project_detail',args=[self.data.project_set.all().first().id])
		return context

	def get_success_url(self):
		return reverse('project:project_detail',args=[self.data.project_set.all().first().id])

class projectcomment_pict_add(FormView):
	form_class = FileFieldForm
	template_name = 'project_file_add.html'	 # Replace with your template.

	def dispatch(self, request, *args, **kwargs):
		self.comment = get_object_or_404(projectcomment, id=self.kwargs['pk'], user=request.user)
		return super(projectcomment_pict_add, self).dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		files = request.FILES.getlist('file_field')

		if form.is_valid():
			for f in files:
				instance = projectpict.objects.create(pict=f, desc=f.name)
				instance.save()
				self.comment.pict.add(instance)
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def get_success_url(self):
		return reverse('project:project_detail',args=[self.comment.project_set.all().first().id])
	
class projectcomment_pict_del(DeleteView):
	model = projectpict
	template_name = '_confirm_delete.html'
	
	def dispatch(self, request, *args, **kwargs):
		return super(projectcomment_pict_del, self).dispatch(request, *args, **kwargs)

	def get_object(self, queryset=None):
		self.data=super(projectcomment_pict_del, self).get_object()
		if self.data.projectcomment_set.all().first().user != self.request.user:
			raise PermissionDenied
		return self.data
	
	def get_context_data(self, **kwargs):
		context = super(projectcomment_pict_del, self).get_context_data(**kwargs)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = reverse('project:project_detail',args=[self.data.projectcomment_set.all().first().project_set.all().first().id])
		return context

	def get_success_url(self):
		return reverse('project:project_detail',args=[self.data.projectcomment_set.all().first().project_set.all().first().id])

class projectcomment_file_add(FormView):
	form_class = FileFieldForm
	template_name = 'project_file_add.html'	 # Replace with your template.

	def dispatch(self, request, *args, **kwargs):
		self.comment = get_object_or_404(projectcomment, id=self.kwargs['pk'], user=request.user)
		return super(projectcomment_file_add, self).dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		files = request.FILES.getlist('file_field')

		if form.is_valid():
			for f in files:
				
				fileext = re.compile(r'^.*\.(?P<ext>\w+)$').match(f.name).group('ext')
				
				if fileext in list_ext_pictures:
					instance = projectpict.objects.create(pict=f, desc=f.name)
					instance.save()
					self.comment.pict.add(instance)
				else:
					instance = projectfile.objects.create(sourcefile=f, desc=f.name)
					instance.save()
					self.comment.file.add(instance)

			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def get_success_url(self):
		return reverse('project:project_detail',args=[self.comment.project_set.all().first().id])

class projectcomment_file_del(DeleteView): 
	template_name = '_confirm_delete.html' 
	model = projectfile

	def dispatch(self, request, *args, **kwargs):
		return super(projectcomment_file_del, self).dispatch(request, *args, **kwargs)

	def get_object(self, queryset=None):
		self.data=super(projectcomment_file_del, self).get_object()
		if self.data.projectcomment_set.all().first().user != self.request.user:
			raise PermissionDenied
		return self.data

	def get_context_data(self, **kwargs):
		context = super(projectcomment_file_del, self).get_context_data(**kwargs)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = reverse('project:project_detail',args=[self.data.projectcomment_set.all().first().project_set.all().first().id])
		return context

	def get_success_url(self):
		return reverse('project:project_detail',args=[self.data.projectcomment_set.all().first().project_set.all().first().id])

################# projectstep ################

class projectstep_add(CreateView):
	model = projectstep
	template_name = '_edit2.html'
	fields = ['projectstep', 'name', 'executor', 'distributor', 'edate', 'desc', 'sort']
#	  success_url = reverse('project:project_list'),comment 

	def dispatch(self, request, *args, **kwargs):
		self.p = get_object_or_404(project, id=self.kwargs['pk'], user=self.request.user)
		return super(projectstep_add, self).dispatch(request, *args, **kwargs)
	
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
			form = super(projectstep_add, self).get_form(form_class)
			# form.fields['sdate'].widget.attrs['class'] = 'form-control datepicker'
			form.fields['edate'].widget.attrs['class'] = 'form-control datepicker'
			#form.fields['sdate'].input_formats=['%d-%m-%y', '%d-%m-%Y',]
			#form.fields['edate'].input_formats=['%d-%m-%y', '%d-%m-%Y',]
			form.fields['projectstep'].queryset=projectstep.objects.filter(project=self.p)
			return form
		return form_class(**self.get_form_kwargs())
	
	def form_invalid(self, form):
		response = super().form_invalid(form)
		if self.request.is_ajax():
			return JsonResponse(form.errors, status=400)
		else:
			return response

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.user = self.request.user
		instance.project = self.p
		instance.save()
		self.projectstep = instance
		return super(projectstep_add, self).form_valid(form)
	
	
#	  #def get_context_data(self, *args, **kwargs):
#	  #	   context_data = super(projectstep_add, self).get_context_data(*args, **kwargs)
#	  #	   context_data.update({'object': self.data,})
#	  #	   return context_data

	def get_success_url(self):
		if self.p.status == 'created':
			#send telegram
			path_projectstep = reverse('project:projectstep_detail',args=[self.projectstep.id])
			
			# проверяем шаблон и отправляем сообщения в чат
			value_chat = get_message('ttapsc', self.p.user, path_projectstep, self.p.name, self.projectstep.name)
			send_message(User.objects.get(username='telegram_chat'), value_chat)
			# проверяем шаблон и отправляем сообщения исполнителям
			value_executor = get_message('ttapse', self.p.user, path_projectstep, self.p.name, self.projectstep.name)
			for e in self.projectstep.executor.all().exclude(user=self.p.user):
				send_message(e.user, value_executor)

		return reverse('project:project_detail',args=[self.p.id])

class projectstep_edit(UpdateView):
	model = projectstep
	template_name = '_edit2.html'
	fields = ['id', 'name', 'executor', 'distributor', 'edate', 'desc', 'sort']

	def dispatch(self, request, *args, **kwargs):
		# self.data = get_object_or_404(projectstep, id=self.kwargs['pk'])
		return super(projectstep_edit, self).dispatch(request, *args, **kwargs)
	
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
			form = super(projectstep_edit, self).get_form(form_class)
			# form.fields['sdate'].widget.attrs['class'] = 'form-control datepicker'
			form.fields['edate'].widget.attrs['class'] = 'form-control datepicker'
			#form.fields['sdate'].input_formats=['%d-%m-%y', '%d-%m-%Y',]
			#form.fields['edate'].input_formats=['%d-%m-%y', '%d-%m-%Y',]
			return form
		return form_class(**self.get_form_kwargs())

	def get_object(self, queryset=None):
		self.data=super(projectstep_edit, self).get_object()
		if self.data.project.user != self.request.user:
			raise PermissionDenied
		return self.data

	def get_success_url(self):
		path_projectstep = reverse('project:projectstep_detail',args=[self.data.id])
		if self.data.project.status == 'created':
			#send telegram	 
			# проверяем шаблон и отправляем сообщения в чат
			value_chat = get_message('ttcpsc', self.data.project.user, path_projectstep, self.data.project.name, self.data.name)
			send_message(User.objects.get(username='telegram_chat'), value_chat)
			# проверяем шаблон и отправляем сообщения исполнителям
			value_executor = get_message('ttcpse', self.data.project.user, path_projectstep, self.data.project.name, self.data.name)
			for e in self.data.executor.all().exclude(user=self.request.user):
				send_message(e.user, value_executor)

		return path_projectstep

class projectstep_detail(CreateView): 
	template_name = 'projectstep_detail.html' 
	model = projectcomment
	fields = ['value']

	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(projectstep, id=self.kwargs['pk'])
		return super(projectstep_detail, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.user = self.request.user
		#instance.project = self.data.project
		instance.save()
		self.data.projectcomment.add(instance)
		
		if self.data.project.status == 'created':
			#send telegram
			path_projectstep = reverse('project:projectstep_detail',args=[self.data.id])
			# проверяем шаблон и отправляем сообщения в чат
			value_chat = get_message('ttacps', self.request.user, path_projectstep, self.data.project.name, self.data.name)
			send_message(User.objects.get(username='telegram_chat'), value_chat)
			# проверяем шаблон и отправляем сообщения исполнителям
			value_executor = get_message('ttacps', self.request.user, path_projectstep, self.data.project.name, self.data.name)
			for e in self.data.executor.all().exclude(user=self.request.user):
				send_message(e.user, value_executor)

		return super(projectstep_detail, self).form_valid(form)

	def get_context_data(self, *args, **kwargs):
		context_data = super(projectstep_detail, self).get_context_data(*args, **kwargs)
		context_data.update({'object': self.data,})
		return context_data

	def get_success_url(self):
		return reverse('project:projectstep_detail',args=[self.data.id])

class projectstep_del(DeleteView): 
	template_name = '_confirm_delete.html' 
	model = projectstep

	def dispatch(self, request, *args, **kwargs):
		return super(projectstep_del, self).dispatch(request, *args, **kwargs)
	
	def get_object(self, queryset=None):
		self.data=super(projectstep_del, self).get_object()
		if self.data.project.user != self.request.user:
			raise PermissionDenied
		return self.data

	def get_context_data(self, **kwargs):
		context = super(projectstep_del, self).get_context_data(**kwargs)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = reverse('project:project_detail',args=[self.data.project.id])
		return context

	def get_success_url(self):
		return reverse('project:project_detail',args=[self.data.project.id])


class projectstep_success(UpdateView):
	model = projectstep
	template_name = '_edit2.html'
	fields = ['status']

	def dispatch(self, request, *args, **kwargs):
		# self.data = get_object_or_404(projectstep, id=self.kwargs['pk'])
		return super(projectstep_success, self).dispatch(request, *args, **kwargs)
	
	def get_object(self, queryset=None):
		self.data=super(projectstep_success, self).get_object()
		if self.data.project.user != self.request.user:
			raise PermissionDenied
		
		if self.data.projectstep is not None:
			if self.data.projectstep.status == True:
				raise Http404()
		return self.data

	def get_success_url(self):
		path_projectstep = reverse('project:projectstep_detail',args=[self.data.id])
		#send telegram
		if self.data.project.status == 'created':
			# проверяем шаблон и отправляем сообщения в чат
			value_chat = get_message('tteps', self.request.user, path_projectstep, self.data.project.name, self.data.name)
			send_message(User.objects.get(username='telegram_chat'), value_chat)
			# проверяем шаблон и отправляем сообщения исполнителям
			value_executor = get_message('tteps', self.request.user, path_projectstep, self.data.project.name, self.data.name)
			for e in self.data.executor.all().exclude(user=self.request.user):
				send_message(e.user, value_executor)
		return path_projectstep


class projectstep_pict_add(FormView):
	form_class = FileFieldForm
	template_name = 'project_file_add.html'	 # Replace with your template.

	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(projectstep, id=self.kwargs['pk'], project__user=self.request.user)
		return super(projectstep_pict_add, self).dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		files = request.FILES.getlist('file_field')

		if form.is_valid():
			for f in files:
				instance = projectpict.objects.create(pict=f, desc=f.name)
				instance.save()
				self.data.pict.add(instance)
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def get_success_url(self):
		return reverse('project:projectstep_detail',args=[self.data.id])

class projectstep_pict_del(DeleteView): 
	template_name = '_confirm_delete.html' 
	model = projectpict

	def dispatch(self, request, *args, **kwargs):
		return super(projectstep_pict_del, self).dispatch(request, *args, **kwargs)
	
	def get_object(self, queryset=None):
		self.data=super(projectstep_pict_del, self).get_object()
		if self.data.projectstep_set.first().project.user != self.request.user:
			raise PermissionDenied
		return self.data

	def get_context_data(self, **kwargs):
		context = super(projectstep_pict_del, self).get_context_data(**kwargs)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = reverse('project:projectstep_detail',args=[self.data.projectstep_set.all().first().project.id])
		return context

	def get_success_url(self):
		return reverse('project:projectstep_detail',args=[self.data.projectstep_set.all().first().project.id])

class projectstep_file_add(FormView):
	form_class = FileFieldForm
	template_name = 'project_file_add.html'	 # Replace with your template.

	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(projectstep, id=self.kwargs['pk'], project__user=self.request.user)
		return super(projectstep_file_add, self).dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		files = request.FILES.getlist('file_field')

		if form.is_valid():
			for f in files:
				
				fileext = re.compile(r'^.*\.(?P<ext>\w+)$').match(f.name).group('ext')
				
				if fileext in list_ext_pictures:
					instance = projectpict.objects.create(pict=f, desc=f.name)
					instance.save()
					self.data.pict.add(instance)
				else:
					instance = projectfile.objects.create(sourcefile=f, desc=f.name)
					instance.save()
					self.data.file.add(instance)

			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def get_success_url(self):
		return reverse('project:projectstep_detail',args=[self.data.id])

class projectstep_file_del(DeleteView): 
	template_name = '_confirm_delete.html'
	model = projectfile

	def dispatch(self, request, *args, **kwargs):
		return super(projectstep_file_del, self).dispatch(request, *args, **kwargs)
	
	def get_object(self, queryset=None):
		self.data=super(projectstep_file_del, self).get_object()
		if self.data.projectstep_set.first().project.user != self.request.user:
			raise PermissionDenied
		return self.data
	
	def get_context_data(self, **kwargs):
		context = super(projectstep_file_del, self).get_context_data(**kwargs)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = reverse('project:projectstep_detail',args=[self.data.projectstep_set.all().first().id])
		return context

	def get_success_url(self):
		return reverse('project:projectstep_detail',args=[self.data.projectstep_set.all().first().id])

class projectstepcomment_edit(UpdateView):
	model = projectcomment
	template_name = '_edit2.html'
	fields = ['value']

	def dispatch(self, request, *args, **kwargs):
		return super(projectstepcomment_edit, self).dispatch(request, *args, **kwargs)
	
	def get_object(self, queryset=None):
		self.data=super(projectstepcomment_edit, self).get_object()
		if self.data.user != self.request.user:
			raise PermissionDenied
		return self.data

	def get_success_url(self):
		return reverse('project:projectstep_detail',args=[self.data.projectstep_set.all().first().id])

class projectstepcomment_del(DeleteView): 
	template_name = '_confirm_delete.html' 
	model = projectcomment

	def dispatch(self, request, *args, **kwargs):
		return super(projectstepcomment_del, self).dispatch(request, *args, **kwargs)
	
	def get_object(self, queryset=None):
		self.data=super(projectstepcomment_del, self).get_object()
		if self.data.user != self.request.user:
			raise PermissionDenied
		return self.data

	def get_context_data(self, **kwargs):
		context = super(projectstepcomment_del, self).get_context_data(**kwargs)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = reverse('project:projectstep_detail',args=[self.data.projectstep_set.all().first().id])
		return context

	def get_success_url(self):
		return reverse('project:projectstep_detail',args=[self.data.projectstep_set.all().first().id])

class projectstepcomment_pict_add(FormView):
	form_class = FileFieldForm
	template_name = 'project_file_add.html'	 # Replace with your template.

	def dispatch(self, request, *args, **kwargs):
		self.comment = get_object_or_404(projectcomment, id=self.kwargs['pk'], user=request.user)
		return super(projectstepcomment_pict_add, self).dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		files = request.FILES.getlist('file_field')

		if form.is_valid():
			for f in files:
				instance = projectpict.objects.create(pict=f, desc=f.name)
				instance.save()
				self.comment.pict.add(instance)
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def get_success_url(self):
		return reverse('project:projectstep_detail',args=[self.comment.projectstep_set.all().first().id])

class projectstepcomment_pict_del(DeleteView):
	model = projectpict
	template_name = '_confirm_delete.html'
	
	def dispatch(self, request, *args, **kwargs):
		return super(projectstepcomment_pict_del, self).dispatch(request, *args, **kwargs)

	def get_object(self, queryset=None):
		self.data=super(projectstepcomment_pict_del, self).get_object()
		if self.data.projectcomment_set.all().first().user != self.request.user:
			raise PermissionDenied
		return self.data
	
	def get_context_data(self, **kwargs):
		context = super(projectstepcomment_pict_del, self).get_context_data(**kwargs)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = reverse('project:projectstep_detail',args=[self.data.projectcomment_set.all().first().projectstep_set.all().first().id])
		return context

	def get_success_url(self):
		return reverse('project:projectstep_detail',args=[self.data.projectcomment_set.all().first().projectstep_set.all().first().id])

class projectstepcomment_file_add(FormView): 
	form_class = FileFieldForm
	template_name = 'project_file_add.html'	 # Replace with your template.

	def dispatch(self, request, *args, **kwargs):
		self.comment = get_object_or_404(projectcomment, id=self.kwargs['pk'], user=request.user)
		return super(projectstepcomment_file_add, self).dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		files = request.FILES.getlist('file_field')

		if form.is_valid():
			for f in files:
				
				fileext = re.compile(r'^.*\.(?P<ext>\w+)$').match(f.name).group('ext')
				
				if fileext in list_ext_pictures:
					instance = projectpict.objects.create(pict=f, desc=f.name)
					instance.save()
					self.comment.pict.add(instance)
				else:
					instance = projectfile.objects.create(sourcefile=f, desc=f.name)
					instance.save()
					self.comment.file.add(instance)

			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def get_success_url(self):
		return reverse('project:projectstep_detail',args=[self.comment.projectstep_set.all().first().id])


class projectstepcomment_file_del(DeleteView): 
	template_name = '_confirm_delete.html' 
	model = projectfile

	def dispatch(self, request, *args, **kwargs):
		return super(projectstepcomment_file_del, self).dispatch(request, *args, **kwargs)

	def get_object(self, queryset=None):
		self.data=super(projectstepcomment_file_del, self).get_object()
		if self.data.projectcomment_set.all().first().user != self.request.user:
			raise PermissionDenied
		return self.data
	
	def get_context_data(self, **kwargs):
		context = super(projectstepcomment_file_del, self).get_context_data(**kwargs)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = reverse('project:projectstep_detail',args=[self.data.projectcomment_set.all().first().projectstep_set.all().first().id])
		return context

	def get_success_url(self):
		return reverse('project:projectstep_detail',args=[self.data.projectcomment_set.all().first().projectstep_set.all().first().id])


class projectstep_cost_add(CreateView): 
	template_name = '_edit2.html'
	fields = ['typecost', 'name', 'distributor', 'costsum']
	model = projectstepcost

	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(projectstep, id=self.kwargs['pk'])
		return super(projectstep_cost_add, self).dispatch(request, *args, **kwargs)
	
	def get_form(self, form_class=None):

		if self.data.project.user != self.request.user and self.request.user not in [e.user for e in self.data.executor.all()]:
			raise PermissionDenied

		if form_class is None:
			form_class = self.get_form_class()
			form = super(projectstep_cost_add, self).get_form(form_class)
			#form.fields['distributor'].queryset=distributor.objects.filter(projectstep=self.data)
			form.fields['distributor'].queryset=distributor.objects.all()
			form.fields['typecost'].initial='plan'
			if self.data.project.user !=self.request.user:
				form.fields['typecost'].initial='fact'
				form.fields['typecost'].widget.attrs['disabled'] = True
				form.fields['typecost'].required=False
			return form
		return form_class(**self.get_form_kwargs())

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.user = self.request.user
		instance.projectstep = self.data
		instance.save()
		# self.data.cost.add(instance)
		return super(projectstep_cost_add, self).form_valid(form)

	def get_success_url(self):
		return reverse('project:projectstep_detail',args=[self.data.id])

