from django.shortcuts import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse
from django.http import Http404
from django.contrib.auth.models import User
from django import forms

from django.utils import timezone

from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView

from django.views.generic import DetailView, DeleteView
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView

import time
import requests
import datetime


from dj.views import *
from .models import *
from acl.views import *
from notify.models import *
from node.models import *
from django.urls import reverse
from telegramtemplate.models import *

list_notification = ['admin', 'disc']

def get_message(typetemplate, user, path):
	# Переменные шаблона:<br>
	# (today) - Сегодняшняя дата<br>
	# (user) - Пользователь<br>
	# (url) - Ссылка на объект (crm.babah24.ru)<br>
	today = datetime.date.today()

	fullname = user.first_name + " " + user.last_name

	t = telegramtemplate.objects.filter(name=typetemplate)
	t = t.first()
	message = t.message
	message = message.replace('(today)', str(today))
	message = message.replace('(user)', str(fullname))
	message = message.replace('(url)', 'crm.babah24.ru%s' % path)
	return message

# grantchoice=(('L', 'Список'), ('R', 'Чтение'), ('С', 'Создание'), ('U', 'Редактирование'),)

#################################################
###### категории документооборота ###############
#################################################

class docflow_category_add(CreateView):
	model = docflow_category
	template_name = '_edit2.html'
	fields = ['name']

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'docflow_category', 'C')
		return super(docflow_category_add, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		instance = form.save(commit=False)
		# instance.user = self.request.user
		instance.save()
		return super(docflow_category_add, self).form_valid(form)

	def get_success_url(self):
		return reverse('docflow:docflow_category_list')

class docflow_category_list(ListView): 
	template_name = 'docflow_category_list.html' 
	model = docflow_category

class docflow_category_edit(UpdateView):
	model = docflow_category
	template_name = '_edit2.html'
	fields = ['name']

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'docflow_category', 'U')
		return super(docflow_category_edit, self).dispatch(request, *args, **kwargs)

	def get_success_url(self):
		return reverse('docflow:docflow_category_list')

class docflow_category_del(DeleteView): 
	template_name = '_confirm_delete.html' 
	model = docflow_category

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'docflow_category', 'U')
		return super(docflow_category_del, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(docflow_category_del, self).get_context_data(**kwargs)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = reverse('docflow:docflow_category_list')
		return context

	def get_success_url(self):
		return reverse('docflow:docflow_category_list')

##############################################################
###### операции с расходным ордером документооборота #########
##############################################################
# class cash_payment_voucher_detail(DetailView):
# 	model = cash_payment_voucher
# 	template_name = 'cash_payment_voucher_detail.html'

class VoucherForm(forms.Form):
	name_field = forms.CharField(label='Основание', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'on'}), max_length=255, required=False)
	category_field = forms.ModelChoiceField(label='Категория', widget=forms.Select(attrs={'class': 'form-control', 'size': '10'}), queryset=docflow_category.objects.all(), required=True)
	addressee_field = forms.ModelChoiceField(label='Кому выдана', widget=forms.Select(attrs={'class': 'form-control', 'size': '10'}), queryset=profileuser.objects.all(), required=False)
	sum_field = forms.FloatField(label='Выданная сумма', required=True)
	file_field = forms.FileField(label='Вложенные файлы', widget=forms.ClearableFileInput(attrs={'multiple': True}), required=True)
	comment_field = forms.CharField(label='Комментарий', widget=forms.Textarea(attrs={'class': 'form-control','autocomplete': 'on', 'size': '10'}), max_length=3000, required=False)

class cash_payment_voucher_add(FormView):
	form_class = VoucherForm
	template_name = 'cash_payment_voucher_add.html'
	
	# def dispatch(self, request, *args, **kwargs):
	# 	return super(cash_payment_voucher_add, self).dispatch(request, *args, **kwargs)
	
	def form_valid(self, form):		
		fdata = form.cleaned_data
		files = self.request.FILES.getlist('file_field')
		addressee = fdata['addressee_field']
		category = fdata['category_field']
		sum = fdata['sum_field']
		name = fdata['name_field']
		comment = fdata['comment_field']

		# print(fdata)

		data = cash_payment_voucher.objects.create(
			name=name,
			user=profileuser.objects.get(user=self.request.user),
			addressee=addressee,
			sum=sum,
			category=category,
			comment=comment)
	
		data.save()
	
		for f in files:
			dfile = docflowfile.objects.create(sourcefile=f, name=f.name, voucher=data)
			dfile.save()

		# instance = form.save(commit=False)
		# instance.user = profileuser.objects.get(user=self.request.user)
		# instance.save()

		#рассылка
		nh = notifyhandler.objects.get(name='telegram')
		message = get_message('vaucher_add', self.request.user, reverse('docflow:cash_payment_voucher_admin_list'))
		
		for ln in list_notification:
			try:
				nuk = notifyuserkey.objects.get(user=User.objects.get(username=ln), handler=nh)
			except:
				pass
			else:
				nq = notifyqueue.objects.create(user=User.objects.get(username=ln), handler=nh, value=message)

		return super(cash_payment_voucher_add, self).form_valid(form)

	def get_success_url(self):
		return reverse('docflow:cash_payment_voucher_list')

# ордер на контрагента

class VoucherkontragentForm(VoucherForm):
	addressee_field = forms.ModelChoiceField(label='Кому выдана', widget=forms.Select(attrs={'class': 'form-control', 'size': '10'}), queryset=kontragent.objects.all(), required=False)

class cash_payment_voucher_kontragent_add(FormView):
	form_class = VoucherkontragentForm
	template_name = 'cash_payment_voucher_add.html'

	def form_valid(self, form):		
		fdata = form.cleaned_data
		files = self.request.FILES.getlist('file_field')
		kontragent = fdata['addressee_field']
		category = fdata['category_field']
		sum = fdata['sum_field']
		name = fdata['name_field']
		comment = fdata['comment_field']

		# print(fdata)

		data = cash_payment_voucher.objects.create(
			name=name,
			user=profileuser.objects.get(user=self.request.user),
			kontragent=kontragent,
			sum=sum,
			category=category,
			comment=comment)
	
		data.save()
	
		for f in files:
			dfile = docflowfile.objects.create(sourcefile=f, name=f.name, voucher=data)
			dfile.save()

		# instance = form.save(commit=False)
		# instance.user = profileuser.objects.get(user=self.request.user)
		# instance.save()

		#рассылка
		nh = notifyhandler.objects.get(name='telegram')
		message = get_message('vaucher_add', self.request.user, reverse('docflow:cash_payment_voucher_admin_list'))
		
		for ln in list_notification:
			try:
				nuk = notifyuserkey.objects.get(user=User.objects.get(username=ln), handler=nh)
			except:
				pass
			else:
				nq = notifyqueue.objects.create(user=User.objects.get(username=ln), handler=nh, value=message)

		return super(cash_payment_voucher_kontragent_add, self).form_valid(form)

	def get_success_url(self):
		return reverse('docflow:cash_payment_voucher_list')


class cash_payment_voucher_list(ListView): 
	template_name = 'cash_payment_voucher_list.html' 
	model = cash_payment_voucher
	# paginate_by = 6

	# def dispatch(self, request, *args, **kwargs): 
	#	  return super(cash_payment_voucher_list, self).dispatch(request, *args, **kwargs) 

	def get_queryset(self): 
		data=super(cash_payment_voucher_list, self).get_queryset() 
		data = data.filter(user=profileuser.objects.get(user=self.request.user)) #for get_context_data 
		return data 

class Form_filter_cash_payment_voucher(forms.Form):
	q = forms.CharField(label='Поиск по основанию', help_text='Введите слово для поиска', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'off'}), max_length=100, required=False)
	status =forms.ChoiceField(label='Статус', widget=forms.Select(attrs={'class': 'form-control', 'size': '2',}), choices=CLIST, required=False)
	category = forms.ModelMultipleChoiceField(label='Категория', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), queryset=docflow_category.objects.all(), required=False)
	user = forms.ModelMultipleChoiceField(label='Кем выдана', widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '12',}), queryset=profileuser.objects.all(), required=False)	
	paging = forms.BooleanField(label='На одной странице', initial=True, required=False)

class cash_payment_voucher_admin_list(ListView): 
	template_name = 'cash_payment_voucher_admin_list.html' 
	model = cash_payment_voucher

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'docflow_admin', 'L')
		return super(cash_payment_voucher_admin_list, self).dispatch(request, *args, **kwargs) 

	def get_queryset(self):
		data=super(cash_payment_voucher_admin_list, self).get_queryset()
		data=data.all() #выбираем основной запрос
		f=Form_filter_cash_payment_voucher(self.request.GET)
		
		req = ''
		paging = 40
		
		if f.is_valid():
			fdata = f.cleaned_data
			print(fdata['status'])
			#фильтрация
			if fdata['q']:
				req = '%s&q=%s' % (req, fdata['q'])
				data=data.filter(name=fdata['q'])

			if fdata['status']:
				req = '%s&status=%s' % (req, self.request.GET['status'])
				data=data.filter(status=fdata['status']) #distinct() если выбирается из нескольких категорий		
			
			if fdata['category']:
				req = '%s&category=%s' % (req, self.request.GET['category'])
				data=data.filter(category__in=fdata['category']) #distinct() если выбирается из нескольких категорий		
			
			if fdata['user']:
				req = '%s&user=%s' % (req, self.request.GET['user'])
				data = data.filter(user__in=fdata['user'])

			if fdata['paging']:
				req = '%s&paging=%s' % (req, self.request.GET['paging'])
				paging = 1000
				
		self.req = req
	
		data=data.order_by('-ctime')
	
		#paginator
		self.p = Paginator(data, paging)
		#page = self.kwargs['page']
		xpage = self.request.GET.get('xpage', default=1)
		#print self.p.number()
		try:
			pdata = self.p.page(xpage)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			pdata = self.p.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			pdata = self.p.page(self.p.num_pages)
		
		# print(pdata)
		return pdata
		
	
	def get_context_data(self, *args, **kwargs):
		context_data = super(cash_payment_voucher_admin_list, self).get_context_data(*args, **kwargs)
		context_data.update({'req': self.req,})
		context_data.update({'count': self.p.count,})
		context_data.update({'form': Form_filter_cash_payment_voucher(self.request.GET)}),
		context_data.update({'urlpage': reverse('docflow:cash_payment_voucher_admin_list'),})
		return context_data

class cash_payment_voucher_edit(UpdateView):
	model = cash_payment_voucher
	template_name = '_edit2.html'
	fields = ['name', 'category', 'sum', 'addressee', 'kontragent', 'comment']

	def get_object(self, queryset=None):
		self.data=super(cash_payment_voucher_edit, self).get_object()
		if self.data.user.user != self.request.user or self.data.status == 'approved':
			raise PermissionDenied
		return self.data

	def get_success_url(self):
		return reverse('docflow:cash_payment_voucher_list')

class cash_payment_voucher_change_status(UpdateView):
	model = cash_payment_voucher
	template_name = '_edit2.html'
	fields = ['status']

	def get_success_url(self):
		return reverse('docflow:cash_payment_voucher_list')


class cash_payment_voucher_del(DeleteView): 
	template_name = '_confirm_delete.html' 
	model = cash_payment_voucher

	def get_object(self, queryset=None):
		self.data=super(cash_payment_voucher_del, self).get_object()
		if self.data.user.user != self.request.user or self.data.status == 'approved':
			raise PermissionDenied
		return self.data
	
	def get_context_data(self, **kwargs):
		context = super(cash_payment_voucher_del, self).get_context_data(**kwargs)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = reverse('docflow:cash_payment_voucher_list')
		return context

	def get_success_url(self):
		return reverse('docflow:cash_payment_voucher_list')

class addfileForm(forms.Form):
	file_field = forms.FileField(label='Документы',widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

#### операция с файлами #####

class docflowfile_add(FormView): 
	template_name = 'cash_payment_voucher_add.html' 
	form_class = addfileForm

	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(cash_payment_voucher, id=self.kwargs['pk'],user__user=self.request.user)
		if self.data.user.user != self.request.user or self.data.status == 'approved':
			raise PermissionDenied
		return super(docflowfile_add, self).dispatch(request, *args, **kwargs)
	
	def form_valid(self, form):
		files = self.request.FILES.getlist('file_field')
	
		for f in files:
			cfile = docflowfile.objects.create(voucher=self.data, sourcefile=f, name=f)
			cfile.save()
		return super(docflowfile_add, self).form_valid(form)

	def get_success_url(self):
		return reverse('docflow:cash_payment_voucher_list')

class docflowfile_del(DeleteView): 
	template_name = '_confirm_delete.html' 
	model = docflowfile

	def get_object(self, queryset=None):
		self.data = get_object_or_404(docflowfile, id=self.kwargs['pk'],voucher__user__user=self.request.user)
		if self.data.voucher.user.user != self.request.user or self.data.voucher.status == 'approved':
			raise PermissionDenied
		return self.data
	
	def get_context_data(self, **kwargs):
		context = super(docflowfile_del, self).get_context_data(**kwargs)
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = reverse('docflow:cash_payment_voucher_list')
		return context

	def get_success_url(self):
		return reverse('docflow:cash_payment_voucher_list')

##################################################
################КОНТРАГЕНТЫ	######################
##################################################

# class kontragent_list(ListView):
# 	template_name = 'kontragent_list.html'
# 	model = kontragent
# 	paginate_by = 20

# 	def get_queryset(self):
# 		data=super(kontragent_list, self).get_queryset()
# 		data=data.filter(kontragentmenu__aclu__user=self.request.user, kontragentmenu__aclu__type='R')
# 		self.dm=None
# 		if 'pk' in self.kwargs:
# 			self.dm=get_object_or_404(kontragentmenu, id=self.kwargs['pk'], aclu__user=self.request.user, aclu__type='R')
# 			data=data.filter(kontragentmenu=self.dm)
# 		return data
		
# 	def get_context_data(self, *args, **kwargs):
# 		context_data = super(kontragent_list, self).get_context_data(*args, **kwargs)
# 		context_data.update({'kontragentmenu': kontragentmenu.objects.filter(aclu__user=self.request.user, aclu__type='R'),})
# 		context_data.update({'dm': self.dm})
# 		return context_data

# class kontragent_add(CreateView):
# 	model = kontragent
# 	template_name = 'kontragent_add.html'
# 	success_url = '/kontragent/list'
# 	fields = ['name', 'kontragentmenu', 'c', 'tax2', 'a', 'b', 'desc', 'pricefile', 'pricefile2', 'pricefile3',]
	
# 	def dispatch(self, request, *args, **kwargs):
# 		get_object_or_denied(self.request.user, 'kontragent', 'R')
# 		return super(kontragent_add, self).dispatch(request, *args, **kwargs)

# class kontragent_edit(UpdateView):
# 	model = kontragent
# 	template_name = 'kontragent_edit.html'
# 	success_url = '/kontragent/list'
# 	fields = ['name', 'kontragentmenu', 'c', 'tax2', 'a', 'b', 'desc', 'pricefile', 'pricefile2', 'pricefile3',]
	
# 	def dispatch(self, request, *args, **kwargs):
# 		get_object_or_denied(self.request.user, 'kontragent', 'R')
# 		get_object_or_404(self.model, id=self.kwargs['pk'])
# 		return super(kontragent_edit, self).dispatch(request, *args, **kwargs)

# class kontragentmenu_edit(UpdateView):
# 	model = kontragentmenu
# 	template_name = 'kontragentmenu_edit.html'
# 	success_url = '/kontragent/list'
# 	fields = ['aclu',]
	
# 	def dispatch(self, request, *args, **kwargs):
# 		get_object_or_denied(self.request.user, 'kontragent', 'R')
# 		get_object_or_404(self.model, id=self.kwargs['pk'])
# 		return super(kontragentmenu_edit, self).dispatch(request, *args, **kwargs)

# ##############################
