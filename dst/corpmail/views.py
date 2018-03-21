# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponseRedirect
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

from django.views.generic import DetailView, DeleteView
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView

from django.db.models import Q

from dj.views import *
from .models import *
from notify.models import *
from django.urls import reverse
from corpmail.models import *
from telegramtemplate.models import *


def get_message(typetemplate, user, path):
    # Переменные шаблона:<br>
    # (today) - Сегодняшняя дата<br>
	# (user) - Пользователь<br>
	# (url) - Ссылка на объект (crm.babah24.ru)<br>
    today = datetime.date.today()

    t = telegramtemplate.objects.filter(name=typetemplate)
    t = t.first()
    message = t.message
    message = message.replace('(today)', str(today))
    message = message.replace('(user)', str(user))
    message = message.replace('(url)', 'crm.babah24.ru%s' % path)
    return message

class LetterForm(forms.Form):
	addressee_field = forms.ModelMultipleChoiceField(label='Адресат[ы]', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12'}), queryset=profileuser.objects.all(), required=True)
	name_field = forms.CharField(label='Тема', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'on'}), max_length=200, required=True)
	desc_field = forms.CharField(label='Содержание', widget=forms.Textarea(attrs={'class': 'form-control','autocomplete': 'on', 'size': '10'}), max_length=3000, required=False)
	file_field = forms.FileField(label='Вложенные файлы',widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

class ReplyForm(forms.Form):
	name_field = forms.CharField(label='Тема', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'on'}), max_length=200, required=True)
	desc_field = forms.CharField(label='Содержание', widget=forms.Textarea(attrs={'class': 'form-control','autocomplete': 'on', 'size': '10'}), max_length=3000, required=False)
	file_field = forms.FileField(label='Файлы',widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

class corpmail_add(FormView): 
	form_class = LetterForm
	template_name = 'corpmail_add.html'	 # Replace with your template.

	def dispatch(self, request, *args, **kwargs):
		# self.data = get_object_or_404(corpmail, id=self.kwargs['pk'], user=self.request.user)
		return super(corpmail_add, self).dispatch(request, *args, **kwargs)
	
	def form_valid(self, form):
		fdata = form.cleaned_data
		files = self.request.FILES.getlist('file_field')
		# addressees = self.request.POST.getlist('addressee_field')
		#print fdata['name_field']

		for a in fdata['addressee_field']:
			data = corpmail.objects.create(user=profileuser.objects.get(user=self.request.user), addressee=a)
			data.name = fdata['name_field']
			data.desc = fdata['desc_field']

			for f in files:
				cfile = corpmailfile.objects.create(sourcefile=f, name=f.name, corpmail=data)
				cfile.save()

			data.save()

		#рассылка
		nh = notifyhandler.objects.get(name='telegram')
		message = get_message('corpmail_add', self.request.user, reverse('corpmail:corpmail_detail', args=[data.id]))
		
		for i in fdata['addressee_field']:
			try:
				nuk = notifyuserkey.objects.get(user=i.user, handler=nh)
			except:
				pass
			else:
				nq = notifyqueue.objects.create(user=i.user, handler=nh, value=message)
		
		return super(corpmail_add, self).form_valid(form)

	def get_success_url(self):
		return reverse('corpmail:corpmail_inbox')

class corpmail_inbox(ListView): 
	template_name = 'corpmail_inbox.html' 
	model = corpmail
	paginate_by = 30

	def dispatch(self, request, *args, **kwargs): 
		return super(corpmail_inbox, self).dispatch(request, *args, **kwargs) 

	def get_queryset(self): 
		data=super(corpmail_inbox, self).get_queryset()
		data = data.filter(addressee__user=self.request.user)
		self.count = data.filter(status='created').count()
		data = data.filter(Q(status='created') | Q(status='read'))
		return data

	def get_context_data(self, *args, **kwargs):
		context_data = super(corpmail_inbox, self).get_context_data(*args, **kwargs)
		context_data['count_unread'] = self.count
		return context_data

class corpmail_sent(ListView): 
	template_name = 'corpmail_sent.html' 
	model = corpmail
	paginate_by = 30

	def dispatch(self, request, *args, **kwargs): 
		return super(corpmail_sent, self).dispatch(request, *args, **kwargs) 

	def get_queryset(self): 
		data=super(corpmail_sent, self).get_queryset()
		self.count = data.filter(addressee__user=self.request.user).filter(status='created').count()
		data = data.filter(user__user=self.request.user)
		return data

	def get_context_data(self, *args, **kwargs):
		context_data = super(corpmail_sent, self).get_context_data(*args, **kwargs)
		context_data['count_unread'] = self.count
		return context_data


class corpmail_toarchive(UpdateView):
	model = corpmail
	template_name = '_edit2.html'
	fields = ['status']

	def get_object(self, queryset=None):
		self.data=super(corpmail_toarchive, self).get_object()
		if self.request.user != self.data.addressee.user:
			raise PermissionDenied
		return self.data

	def get_success_url(self):
		return reverse('corpmail:corpmail_inbox')

class corpmail_detail(FormView): 
	form_class = ReplyForm
	template_name = 'corpmail_detail.html'	 # Replace with your template.
	paginate_by = 1

	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(corpmail, id=self.kwargs['pk'])
		if self.request.user == self.data.user.user or self.request.user == self.data.addressee.user:
			if self.request.user == self.data.addressee.user and self.data.status != 'archived':
				self.data.status = 'read'
			self.data.save()
		else:
			raise PermissionDenied	
		return super(corpmail_detail, self).dispatch(request, *args, **kwargs)
	
	def form_valid(self, form):
		fdata = form.cleaned_data
		files = self.request.FILES.getlist('file_field')
		data = corpmail.objects.create(user=profileuser.objects.get(user=self.request.user), addressee = self.data.user)
		
		for f in files:
			cfile = corpmailfile.objects.create(sourcefile=f, name=f.name, corpmail=data)
			cfile.save()
	
		data.name = fdata['name_field']
		data.desc = fdata['desc_field']

		if self.data.corpmail != None:
			data.corpmail = self.data.corpmail
		else:
			data.corpmail = self.data

		data.save()
		self.dataid = data.id

		#рассылка
		nh=notifyhandler.objects.get(name='telegram')
		message=get_message('corpmail_reply', self.request.user, reverse('corpmail:corpmail_detail',args=[data.id]))
		try:
			nuk=notifyuserkey.objects.get(user=self.data.user.user, handler=nh)
		except:
			pass
		else: 
			nq=notifyqueue.objects.create(user=self.data.user.user, handler=nh, value=message)
			
		return super(corpmail_detail, self).form_valid(form)
	
	def get_context_data(self, *args, **kwargs):
		context_data = super(corpmail_detail, self).get_context_data(*args, **kwargs)
		context_data.update({'object': self.data,})
		return context_data

	def get_success_url(self):
		return reverse('corpmail:corpmail_detail', args=[self.dataid])

class corpmail_detailsent(DetailView): 
	model = corpmail
	template_name = 'corpmail_detailsent.html'	 # Replace with your template.
	# paginate_by = 1

	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(corpmail, id=self.kwargs['pk'])
		if self.request.user == self.data.user.user or self.data.addressee.all().filter(user=self.request.user):
			pass
		else:
			raise PermissionDenied
		# self.data = get_object_or_404(corpmail, id=self.kwargs['pk'], user=self.request.user)
		return super(corpmail_detailsent, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context_data = super(corpmail_detailsent, self).get_context_data(*args, **kwargs)
		context_data.update({'object': self.data,})
		return context_data

	def get_success_url(self):
		return reverse('corpmail:corpmail_sent')



# class corpmail_edit(UpdateView):
#	  model = corpmail
#	  template_name = 'corpmail_add.html'
#	  fields = ['desc', 'addressee']

#	  def get_object(self, queryset=None):
#		  self.data=super(corpmail_edit, self).get_object()
#		  if self.data.user != self.request.user:
#			  raise PermissionDenied
#		  return self.data

#	  def get_success_url(self):
#		  return reverse('corpmail:corpmail_list')


# class corpmail_del(DeleteView): 
# 	template_name = '_confirm_delete.html' 
# 	model = corpmail

# 	def dispatch(self, request, *args, **kwargs):
# 		return super(corpmail_del, self).dispatch(request, *args, **kwargs)
	
# 	def get_object(self, queryset=None):
# 		self.data=super(corpmail_del, self).get_object()
# 		if self.data.user != self.request.user:
# 			raise PermissionDenied
# 		return self.data

# 	def get_context_data(self, **kwargs):
# 		context = super(corpmail_del, self).get_context_data(**kwargs)
# 		context['msg'] = u'Вы уверены что хотите удалить '
# 		context['back_url'] = reverse('corpmail:corpmail_list')
# 		return context

# 	def get_success_url(self):
# 		for f in self.data.file.all():
# 			f.delete()
# 		return reverse('corpmail:corpmail_list')

# class corpmail_reply(FormView): 
# 	form_class = ReplyForm
# 	template_name = 'corpmail_add.html'	 # Replace with your template.

# 	def dispatch(self, request, *args, **kwargs):
# 		# self.data = get_object_or_404(corpmail, id=self.kwargs['pk'], user=self.request.user)
# 		return super(corpmail_reply, self).dispatch(request, *args, **kwargs)

# 	def post(self, request, *args, **kwargs):
    	
# 		self.data = get_object_or_404(corpmail, id=self.kwargs['pk'])
		
# 		form_class = self.get_form_class()
# 		form = self.get_form(form_class)
# 		files = request.FILES.getlist('file_field')
# 		name = request.POST['name_field']
# 		desc = request.POST['desc_field']

# 		if form.is_valid():
# 			data = corpmail.objects.create(user=profileuser.objects.get(user=self.request.user))
# 			for f in files:
# 				instance = corpmailfile.objects.create(sourcefile=f, name=f.name)
# 				instance.save()
# 				data.file.add(instance)
			
# 			data.addressee.add(profileuser.objects.get(user=self.data.user))
# 			data.name = name
# 			data.desc = desc
# 			data.save()
			
# 			#рассылка
# 			nh=notifyhandler.objects.get(name='telegram')
# 			message=get_message('corpmail_reply', self.request.user, reverse('corpmail:corpmail_list'))
# 			try:
# 				nuk=notifyuserkey.objects.get(user=self.data.user.user, handler=nh)
# 			except:
# 				print 'corpmail except'
# 				pass	
# 			else: 
# 				nq=notifyqueue.objects.create(user=self.data.user.user, handler=nh, value=message)
			
# 			return self.form_valid(form)
# 		else:
# 			return self.form_invalid(form)

# 	def get_success_url(self):
# 		return reverse('corpmail:corpmail_list')
