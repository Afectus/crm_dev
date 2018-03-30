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
from order.models import *
from panel.form import *
from panel.models import *
from panel.form import *
from sms.views import *
from sms.models import *
from bitrix.models import *
from worktask.models import *
from log.models import *
from personal.models import *

from acl.views import get_object_or_denied

import logging
log = logging.getLogger(__name__)



		
		
#@method_decorator(permission_required('node.add_goods'), name='dispatch')
class personal_list(ListView):
	template_name = 'personal_list.html'
	model = profileuser
	#paginate_by = 10
	
	def dispatch(self, request, *args, **kwargs):
		return super(personal_list, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(personal_list, self).get_queryset()
		#data=data.all() #выбираем основной запрос
		self.currentstatus = None
		if 'status' in self.request.GET:
			data = data.filter(status=self.request.GET['status'])
			self.currentstatus=self.request.GET['status']
		return data.order_by('id')
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(personal_list, self).get_context_data(*args, **kwargs)
		context_data.update({'currentstatus': self.currentstatus,})
		context_data.update({'status': self.model._meta.get_field('status').choices,})
		return context_data


		
#@method_decorator(permission_required('panel.add_profileuser'), name='dispatch')
class personal_edit(UpdateView):
	model = profileuser
	template_name = 'personal_edit.html'
	success_url = '/personal/list/'
	fields = ['photo', 'status', 'bday', 'position', 'phonemobile', 'phonework', 'address', 'email', 'edu', 'diplom', 'message', ]
	
	def dispatch(self, request, *args, **kwargs):
		#self.e = get_object_or_404(self.model, user=request.user)
		get_object_or_denied(self.request.user, 'personal', 'R') #проверяем права
		return super(personal_edit, self).dispatch(request, *args, **kwargs)
	
	def get_success_url(self):
		return '/personal/detail/%s' % (self.get_object().id)
	
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
			form = super(personal_edit, self).get_form(form_class)
			#form.fields['bday'].input_formats=['%d.%m.%y', '%d.%m.%Y',]
			return form
		return form_class(**self.get_form_kwargs())
	
	#def get_object(self, queryset=None):
		#return get_object_or_404(self.model, user=self.request.user)
	
	def get_context_data(self, **kwargs):
		context = super(personal_edit, self).get_context_data(**kwargs)
		context['object'] = self.get_object()
		return context
	

	
#@method_decorator(permission_required('panel.add_profileuser'), name='dispatch')
class personal_detail(DetailView):
	model = profileuser
	template_name = 'personal_detail.html'
	
	def dispatch(self, request, *args, **kwargs):
		#self.data = get_object_or_404(self.model, id=self.kwargs['pk'])
		get_object_or_denied(self.request.user, 'personal', 'R') #проверяем права
		return super(personal_detail, self).dispatch(request, *args, **kwargs)
		
	def get_context_data(self, **kwargs):
		context = super(personal_detail, self).get_context_data(**kwargs)
		#context['servername'] = self.data.name
		return context	
	

	

#@method_decorator(permission_required('node.add_goods'), name='dispatch')
class personal_signature(DetailView):
	model = profileuser
	template_name = 'personal_signature.html'
	
	def dispatch(self, request, *args, **kwargs):
		#self.data = get_object_or_404(self.model, id=self.kwargs['pk'])
		return super(personal_signature, self).dispatch(request, *args, **kwargs)

	def get_object(self, queryset=None):
		data = profileuser.objects.get(user__id=self.kwargs['pk'])
		return data
		
	def get_context_data(self, **kwargs):
		context = super(personal_signature, self).get_context_data(**kwargs)
		#context['servername'] = self.data.name
		return context

		
		
#@method_decorator(permission_required('personal.add_personalchild'), name='dispatch')
class personal_add_child(CreateView):
	model = personalchild
	template_name = 'personal_add_child.html'
	success_url = '/personal/list/?success=true'
	fields = ['profileuser', 'name', 'bday',]
	
	def dispatch(self, request, *args, **kwargs):
		self.pu=get_object_or_404(profileuser, id=self.kwargs['pk'])
		get_object_or_denied(self.request.user, 'personal', 'R') #проверяем права
		return super(personal_add_child, self).dispatch(request, *args, **kwargs)
		
	def get_success_url(self):
		return '/personal/detail/%s' % (self.pu.id)
	
	def get_initial(self):
		return {'profileuser':self.pu,}

	def form_valid(self, form):
		#instance = form.save(commit=False)
		#instance.user = self.request.user
		#instance.save()
		#self.data = instance
		return super(personal_add_child, self).form_valid(form)	

#@method_decorator(permission_required('personal.add_personalchild'), name='dispatch')		
class personal_remove_child(DeleteView):
	model = personalchild
	template_name = '_confirm_delete.html'
	success_url = '/personal/list/?success=true'
	
	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(self.model, id=self.kwargs['pk'])
		get_object_or_denied(self.request.user, 'personal', 'R') #проверяем права
		return super(personal_remove_child, self).dispatch(request, *args, **kwargs)
	
	def get_success_url(self):
		return '/personal/detail/%s' % (self.data.profileuser.id)
		
	def get_context_data(self, **kwargs):
		context = super(personal_remove_child, self).get_context_data(**kwargs)
		#context['object'] = mark_safe('<a href="%s">файл</a>' % self.data.sourcefile.url)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = '/personal/detail/%s' % (self.data.profileuser.id)
		return context
		
		
#@method_decorator(permission_required('personal.add_personalchild'), name='dispatch')	
class personal_edit_child(UpdateView):
	model = personalchild
	template_name = 'personal_edit_child.html'
	success_url = '/personal/list/'
	fields = ['name', 'bday',]
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'personal', 'R') #проверяем права
		self.data = get_object_or_404(self.model, id=self.kwargs['pk'])
		return super(personal_edit_child, self).dispatch(request, *args, **kwargs)

	def get_success_url(self):
		return '/personal/detail/%s' % (self.data.profileuser.id)	

		

#подвиги персонала	
#@method_decorator(permission_required('personal.add_personalfeat'), name='dispatch')
class personal_add_feat(CreateView):
	model = personalfeat
	template_name = 'personal_add_feat.html'
	success_url = '/personal/list/?success=true'
	fields = ['profileuser', 'ctime', 'name', 'message']
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'personal', 'R') #проверяем права
		self.pu=get_object_or_404(profileuser, id=self.kwargs['pk'])
		return super(personal_add_feat, self).dispatch(request, *args, **kwargs)
		
	def get_success_url(self):
		return '/personal/detail/%s' % (self.pu.id)
	
	def get_initial(self):
		return {'profileuser':self.pu,}

	def form_valid(self, form):
		#instance = form.save(commit=False)
		#instance.user = self.request.user
		#instance.save()
		#self.data = instance
		return super(personal_add_feat, self).form_valid(form)	

#@method_decorator(permission_required('personal.add_personalfeat'), name='dispatch')		
class personal_remove_feat(DeleteView):
	model = personalfeat
	template_name = '_confirm_delete.html'
	success_url = '/personal/list/?success=true'
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'personal', 'R') #проверяем права
		self.data = get_object_or_404(self.model, id=self.kwargs['pk'])
		return super(personal_remove_feat, self).dispatch(request, *args, **kwargs)
	
	def get_success_url(self):
		return '/personal/detail/%s' % (self.data.profileuser.id)
		
	def get_context_data(self, **kwargs):
		context = super(personal_remove_feat, self).get_context_data(**kwargs)
		#context['object'] = mark_safe('<a href="%s">файл</a>' % self.data.sourcefile.url)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = '/personal/detail/%s' % (self.data.profileuser.id)
		return context
		
		
#@method_decorator(permission_required('personal.add_personalfeat'), name='dispatch')	
class personal_edit_feat(UpdateView):
	model = personalfeat
	template_name = 'personal_edit_feat.html'
	success_url = '/personal/list/'
	fields = ['ctime', 'name', 'message']
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'personal', 'R') #проверяем права
		self.data = get_object_or_404(self.model, id=self.kwargs['pk'])
		return super(personal_edit_feat, self).dispatch(request, *args, **kwargs)

	def get_success_url(self):
		return '/personal/detail/%s' % (self.data.profileuser.id)	
		
	
class personal_detail_feat(DetailView):
	model = personalfeat
	template_name = 'personal_detail_feat.html'


#подвиги персонала	
#@method_decorator(permission_required('personal.add_personalfeat'), name='dispatch')
class personal_add_feat_image(CreateView):
	model = imagebase
	template_name = '_edit2.html'
	success_url = '/personal/list/?success=true'
	fields = ['pict',]
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'personal', 'R') #проверяем права
		self.data=get_object_or_404(personalfeat, id=self.kwargs['pk'])
		return super(personal_add_feat_image, self).dispatch(request, *args, **kwargs)
		
	def get_success_url(self):
		return '/personal/detail/feat/%s' % (self.data.id)
	
	#def get_initial(self):
	#	return {'profileuser':self.data,}

	def form_valid(self, form):
		instance = form.save(commit=False)
		#instance.user = self.request.user
		instance.save()
		self.data.pict.add(instance)
		return super(personal_add_feat_image, self).form_valid(form)		
	
	
	
	
	
	
	
#анкеты сотрудников
#@method_decorator(permission_required('personal.add_personalanketa'), name='dispatch')
class personalanketa_list(ListView):
	template_name = 'personalanketa_list.html'
	model = personalanketa
	#paginate_by = 10
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'personal', 'R') #проверяем права
		return super(personalanketa_list, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(personalanketa_list, self).get_queryset()
		#data=data.filter(status=True) #выбираем основной запрос
		return data
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(personalanketa_list, self).get_context_data(*args, **kwargs)
		#context_data.update({'req': self.req,})
		return context_data

#@method_decorator(permission_required('personal.add_personalanketa'), name='dispatch')
class personalanketa_add(CreateView):
	model = personalanketa
	template_name = 'personalanketa_add.html'
	success_url = '/personalanketa/list/?success=true'
	fields = ['profileuser', 'name', 'bday', 'phone', 'pict', 'message',]
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'personal', 'R') #проверяем права
		#self.data=get_object_or_404(profileuser, id=self.kwargs['pk'])
		return super(personalanketa_add, self).dispatch(request, *args, **kwargs)
		
	#def get_success_url(self):
		#return '/personalanketa/detail/%s' % (self.data.id)

	def get_initial(self):
		if 'pk' in self.kwargs:
			pu=profileuser.objects.get(id=self.kwargs['pk'])
			return {'profileuser': pu}
		return {}
		
	# def get_form(self, form_class=None):
		# if form_class is None:
			# form_class = self.get_form_class()
			# form = super(personalanketa_add, self).get_form(form_class)
			# form.fields['profileuser'].input_formats=['%d.%m.%y', '%d.%m.%Y',]
			# return form
		# return form_class(**self.get_form_kwargs())

	def form_valid(self, form):
		#instance = form.save(commit=False)
		#instance.user = self.request.user
		#instance.save()
		#self.data = instance
		return super(personalanketa_add, self).form_valid(form)	
		
#@method_decorator(permission_required('personal.add_personalanketa'), name='dispatch')
class personalanketa_edit(UpdateView):
	model = personalanketa
	template_name = 'personalanketa_edit.html'
	success_url = '/personalanketa/list/'
	fields = ['profileuser', 'status', 'name', 'bday', 'phone', 'pict', 'message',]
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'personal', 'R') #проверяем права
		#self.e = get_object_or_404(self.model, user=request.user)
		return super(personalanketa_edit, self).dispatch(request, *args, **kwargs)
	
	def get_success_url(self):
		#return '/personalanketa/edit/%s' % (self.get_object().id)
		return '/personalanketa/list#id%s' % (self.get_object().id)
	
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
			form = super(personalanketa_edit, self).get_form(form_class)
			#form.fields['bday'].input_formats=['%d.%m.%y', '%d.%m.%Y',]
			return form
		return form_class(**self.get_form_kwargs())
	
	#def get_object(self, queryset=None):
		#return get_object_or_404(self.model, user=self.request.user)
	
	def get_context_data(self, **kwargs):
		context = super(personalanketa_edit, self).get_context_data(**kwargs)
		context['object'] = self.get_object()
		return context
	

	
#@method_decorator(permission_required('personal.add_personalanketa'), name='dispatch')
class personalanketa_detail(DetailView):
	model = personalanketa
	template_name = 'personalanketa_detail.html'
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'personal', 'R') #проверяем права
		#self.data = get_object_or_404(self.model, id=self.kwargs['pk'])
		return super(personalanketa_detail, self).dispatch(request, *args, **kwargs)
		
	def get_context_data(self, **kwargs):
		context = super(personalanketa_detail, self).get_context_data(**kwargs)
		#context['servername'] = self.data.name
		return context	
	
	
	
		
class personaldata_edit(UpdateView):
	model = profileuser
	template_name = 'personaldata_edit.html'
	success_url = '/personal/list/'
	fields = ['passport', 'propiska', 'nprikaza', 'uvolen', 'funcworker', 'inn', 'snils',]
	
	def dispatch(self, request, *args, **kwargs):
		#self.e = get_object_or_404(self.model, user=request.user)
		get_object_or_denied(self.request.user, 'personaldata', 'R') #проверяем права
		return super(personaldata_edit, self).dispatch(request, *args, **kwargs)
	
	def get_success_url(self):
		return '/personal/detail/%s' % (self.get_object().id)
	
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
			form = super(personaldata_edit, self).get_form(form_class)
			#form.fields['bday'].input_formats=['%d.%m.%y', '%d.%m.%Y',]
			return form
		return form_class(**self.get_form_kwargs())
	
	#def get_object(self, queryset=None):
		#return get_object_or_404(self.model, user=self.request.user)
	
	def get_context_data(self, **kwargs):
		context = super(personaldata_edit, self).get_context_data(**kwargs)
		context['object'] = self.get_object()
		return context
	