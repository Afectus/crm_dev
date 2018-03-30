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

from django.urls import reverse

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
from acl.models import *
from order.models import *
from panel.form import *
from panel.models import *
from sms.views import *
from sms.models import *
from bitrix.models import *
from worktask.models import *
from log.models import *
from acl.views import get_object_or_denied


import logging
log = logging.getLogger(__name__)



def django_debugtoolbar_show(request):
    return not request.is_ajax() and request.user and request.user.username == "disc"



class home(TemplateView):
	template_name = "index.html"

	def dispatch(self, request, *args, **kwargs):
		return super(home, self).dispatch(request, *args, **kwargs)
	
	def get_context_data(self, *args, **kwargs):
		context_data = super(home, self).get_context_data(*args, **kwargs)
		#context_data.update({'goodfix': goodfix.objects.filter(status='open').order_by('-id')})
		
		#task
		#context_data.update({'mytask': usertask.objects.filter(status='open', executor__user=self.request.user).order_by('-id')})
		#context_data.update({'freetask': usertask.objects.filter(status='open', type='free').exclude(executor__user=self.request.user).order_by('-id')})
		
		#план продаж
		#context_data.update({'lastexc1c': commonlog.objects.filter(name='ex1c').order_by('-ctime').first()})

		#context_data.update({'saleplanshop': saleplanshop.objects.filter(shop__profileuser__user=self.request.user).order_by('-edate')[:6]})
		
		'''
		#МОТИВАЦИЯ
		now = datetime.datetime.now()
		m = now.month
		y = now.year
		#data = shop.objects.filter(check__time__range=(s, e)) #отсекаем чеки по дате

		data = shop.objects.filter(check__time__year=y, check__time__month=m) #отсекаем чеки по месяцу и году

		#data = data.filter(check__checkitem__goods__isnull=False) #отсекаем чеки без товаров, если отключить, в выдаче может присутствовать None, не будет влиять на расчет мотивации #НУЖНО ПРОВЕРИТЬ ПОЧЕМУ ЧЕКИ БЕЗ ТОВАРОВ

		data=data.values('name', 'motivationratio', 'check__checkitem__goods__motivationinpoints') #выборка полей

		data=data.annotate(c=Sum('check__checkitem__col')) #подсчет количества чеков

		#data=data.annotate(r1=F('c')*F('motivationratio'), r2=F('c'))
		data=data.annotate(bonus=F('c'), r=F('c'))
		data=data.order_by('name', 'check__checkitem__goods__motivationinpoints') #сортировка

		if data.exists():
			for i in data:
				try:
					mrs=motivationratiosum.objects.get(demotivation=False, ratio=i['check__checkitem__goods__motivationinpoints'])
				except:
					pass
				else:
					#i['r2']=i['r1']*mrs.sum
					#print 'shop=%s' % i['name'], 'mr=%s' % i['motivationratio'], 'points=%s' % i['check__checkitem__goods__motivationinpoints'], 'col=%s' %i['c'], 'col*mr=%s' % i['r1'], 'r2=%s' % i['r2']
					#print i
					i['r']=i['c']*mrs.sum*i['motivationratio']
					i['bonus']=mrs.sum
					#print 'shop=%s' % i['name'], 'mr=%s' % i['motivationratio'], 'points=%s' % i['check__checkitem__goods__motivationinpoints'], 'col=%s' %i['c'], 'bonus=%s' % mrs.sum, 'col*bonus*mr=%s' % i['r']

		context_data.update({'motivation': data})
		'''
		
		return context_data






		
		

#ОТЗЫВЫ
@method_decorator(permission_required('bitrix.add_review'), name='dispatch')	
class panel_review_list(ListView):
	template_name = 'review_list.html'
	model = review
	paginate_by = 10
	
	def dispatch(self, request, *args, **kwargs):
		#if not gameserver.objects.filter(user=request.user).exists():
		#	return HttpResponseRedirect("/panel")
		return super(panel_review_list, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(panel_review_list, self).get_queryset()
		self.data=data.filter().order_by('-id')
		return self.data
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(panel_review_list, self).get_context_data(*args, **kwargs)
		#context_data.update({'command': True,})
		return context_data		
		
@method_decorator(permission_required('bitrix.add_review'), name='dispatch')	
class panel_review_edit(UpdateView):
	model = review
	template_name = 'review_edit.html'
	success_url = '/review/list/'
	fields = ['status', 'uname', 'subj', 'order', 'message', 'comment', ]
	
	def dispatch(self, request, *args, **kwargs):
		#self.data = get_object_or_404(self.model, status=True, id=self.kwargs['pk'], user=self.request.user)
		return super(panel_review_edit, self).dispatch(request, *args, **kwargs)
	
	#def get_object(self, queryset=None):
	#	return get_object_or_404(self.model, status=True, id=self.kwargs['pk'], user=self.request.user)
		
	def get_context_data(self, **kwargs):
		context = super(panel_review_edit, self).get_context_data(**kwargs)
		#context['servername'] = self.data.name
		return context
		
	def form_valid(self, form):
		#гасим купон
		#order.objects.filter(user=self.request.user, coupon__type__exact='changepassnick', stattus__exact='paid').update(status='used', desc2='changepassnick old pass=%s' % self.data.passwd)
		return super(panel_review_edit, self).form_valid(form)
	
	
	
	
@method_decorator(permission_required('sms.add_smsreport'), name='dispatch')
class sendsms(FormView):
	template_name = 'sendsms.html'
	success_url = '/sendsms/?send=true'
	form_class = Form_sms

	def dispatch(self, request, *args, **kwargs):
		return super(sendsms, self).dispatch(request, *args, **kwargs)

	#def get_success_url(self):
	#	return '/sendsms/?send=true'
	
	#def get_initial(self):
		#подставляем id 
		#return {'id':self.kwargs['pk'],}

	def get_context_data(self, **kwargs):
		context = super(sendsms, self).get_context_data(**kwargs)
		#context['nickname'] = self.data.name
		return context
		
	def form_valid(self, form):
		cd = form.cleaned_data
		sms4b(self.request.user, cd['phone'], cd['message'])
		return super(sendsms, self).form_valid(form)
		
		

#отправка смс покупателю
@method_decorator(permission_required('sms.add_smsreport'), name='dispatch')
class sendsms2b(FormView):
	template_name = 'sendsms2b.html'
	success_url = '/sendsms2b/?send=true'
	form_class = Form_sms2b

	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(buyer, id=self.kwargs['pk'])
		return super(sendsms2b, self).dispatch(request, *args, **kwargs)

	def get_success_url(self):
		return '/sendsms2b/%s/?send=true' % self.data.id
	
	#def get_initial(self):
		#подставляем id 
		#return {'id':self.kwargs['pk'],}

	def get_context_data(self, **kwargs):
		context = super(sendsms2b, self).get_context_data(**kwargs)
		context['buyer'] = self.data
		return context
		
	def form_valid(self, form):
		cd = form.cleaned_data
		phone = '8%s' % self.data.phone
		sms4b(self.request.user, phone, cd['message'])
		return super(sendsms2b, self).form_valid(form)


	
	
@method_decorator(permission_required('sms.add_smsreport'), name='dispatch')
class ownsmsreport_list(ListView):
	template_name = 'smsreport_list.html'
	model = smsreport
	paginate_by = 20
	
	def dispatch(self, request, *args, **kwargs):
		return super(ownsmsreport_list, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(ownsmsreport_list, self).get_queryset()
		try:
			u=User.objects.get(username='smsqsend')
		except:
			data=data.filter(user=self.request.user) #выбираем основной запрос
		else:
			data=data.filter(user__in=[u, self.request.user])
			
		return data
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(ownsmsreport_list, self).get_context_data(*args, **kwargs)
		#сколько отправил пользователь за сегодня
		ucount=self.model.objects.filter(user=self.request.user,  time__gt=datetime.date.today()).count()
		#сколько отправил робот за сегодня
		try:
			qcount=self.model.objects.filter(user__username='smsqsend',	 time__gt=datetime.date.today()).count()
		except:
			qcount=0
			

		context_data.update({'ucount': ucount,})
		context_data.update({'qcount': qcount,})
		context_data.update({'total': self.model.objects.all().count(),})
		return context_data
		
		
		
@method_decorator(permission_required('sms.add_smstemplate'), name='dispatch')
class smstemplate_list(ListView):
	template_name = 'smstemplate_list.html'
	model = smstemplate
	paginate_by = 20
	
	def dispatch(self, request, *args, **kwargs):
		return super(smstemplate_list, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(smstemplate_list, self).get_queryset()
		data=data.order_by('-sort') #выбираем основной запрос
		return data
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(smstemplate_list, self).get_context_data(*args, **kwargs)
		#context_data.update({'req': self.req,})
		return context_data

	
	
	
@method_decorator(permission_required('sms.add_smstemplate'), name='dispatch')	
class smstemplate_edit(UpdateView):
	model = smstemplate
	template_name = 'smstemplate_edit.html'
	success_url = '/smstemplate/list/'
	fields = ['status', 'name', 'sort', 'message', ]
	
	def dispatch(self, request, *args, **kwargs):
		return super(smstemplate_edit, self).dispatch(request, *args, **kwargs)

		
		
		
		
class Form_smsqsend_list(forms.Form):
	#q = forms.CharField(label='Поиск', help_text='Введите слово для поиска', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'off'}), max_length=100, required=False)

	send = forms.ChoiceField(label='Статус', widget=forms.Select(attrs={'class': 'form-control'}), choices=(('false', 'В очереди'), ('all', 'Все'),('true', 'Отправлено'),), initial='all', required=False)

	

@method_decorator(permission_required('sms.add_smsqsend'), name='dispatch')
class smsqsend_list(ListView):
	template_name = 'smsqsend_list.html'
	model = smsqsend
	#paginate_by = 40
	
	def dispatch(self, request, *args, **kwargs):
		#get_object_or_denied(self.request.user, 'goods_list_public', 'L') #проверяем права
		return super(smsqsend_list, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(smsqsend_list, self).get_queryset()
		data=data.all() #выбираем основной запрос
		
		f=Form_smsqsend_list(self.request.GET)
		
		
		req = ''
		paging = 40
		
		if f.is_valid():
			fdata = f.cleaned_data
			#фильтрация
			# if fdata['q']:
				# req = '%s&q=%s' % (req, fdata['q'])
				# data=data.filter(Q(id__icontains=fdata['q']) | Q(id1c__icontains=fdata['q']) | Q(idbitrix__icontains=fdata['q']) | Q(name__icontains=fdata['q']) | Q(name__search=fdata['q']) | Q(namefull__search=fdata['q']) | Q(namefull__icontains=fdata['q']) | Q(art__icontains=fdata['q']) | Q(bname__search=fdata['q']) | Q(bname__icontains=fdata['q']))

			if fdata['send'] == 'true':
				req = '%s&send=%s' % (req, self.request.GET['send'])
				data=data.filter(send=True)
			elif fdata['send'] == 'false':
				req = '%s&send=%s' % (req, self.request.GET['send'])
				data=data.filter(send=False)
			elif fdata['send'] == 'all':
				req = '%s&send=%s' % (req, self.request.GET['send'])
				data=data
			else:
				data=data.filter(send=False)
				
		self.req = req

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

		return pdata
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(smsqsend_list, self).get_context_data(*args, **kwargs)
		context_data.update({'req': self.req,})
		context_data.update({'count': self.p.count,})
		context_data.update({'form': Form_smsqsend_list(self.request.GET, initial={'q': '123',})})
		context_data.update({'urlpage': reverse('panel:smsqsend_list'),})
		return context_data
		
		
@method_decorator(permission_required('sms.add_smsqsend'), name='dispatch')	
class smsqsend_edit(UpdateView):
	model = smsqsend
	template_name = 'smsqsend_edit.html'
	success_url = '/smsqsend/list/'
	fields = ['status', 'message', ]
	saveonclose = True #Кнопка Сохранить и закрыть
	
	def dispatch(self, request, *args, **kwargs):
		data = get_object_or_404(self.model, send=False, id=self.kwargs['pk'])
		return super(smsqsend_edit, self).dispatch(request, *args, **kwargs)	
		
	def get_success_url(self):
		url = '/smsqsend/list/'
		if self.saveonclose:
			url = reverse('panel:saveonclose')
		return url
		#return self.request.GET['next']


		
@method_decorator(permission_required('sms.add_smsqsend'), name='dispatch')	
class smsqsend_detail(DetailView):
	model = smsqsend
	template_name = 'smsqsend_detail.html'
	
	def dispatch(self, request, *args, **kwargs):
		data = get_object_or_404(self.model, id=self.kwargs['pk'])
		return super(smsqsend_detail, self).dispatch(request, *args, **kwargs)	


		
@method_decorator(permission_required('sms.add_smsqsend'), name='dispatch')
class smsqsend_del(DeleteView):
	model = smsqsend
	template_name = '_confirm_delete.html'
	success_url = '/smsqsend/list/'

	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(self.model, send=False, id=self.kwargs['pk'])
		return super(smsqsend_del, self).dispatch(request, *args, **kwargs)
	
	#def get_object(self, queryset=None):
	#	return get_object_or_404(self.model, id=self.kwargs['pk'])
		
	def get_context_data(self, **kwargs):
		context = super(smsqsend_del, self).get_context_data(**kwargs)
		context['object'] = self.data.id
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = '/smsqsend/list/'
		return context
		

#@csrf_exempt
@permission_required('sms.add_smsqsend')
def smsqsend_add(request, pk):
	if request.method == 'GET':
		try:
			data = buyer.objects.get(id=pk)
		except:
			pass
		else:
			t=smstemplate.objects.all().order_by('-sort')
			t=t.first() #берем первый шаблон
			m=t.message
			#фио
			m=m.replace('(f)', data.f)
			m=m.replace('(i)', data.i)
			m=m.replace('(o)', data.o)
			m=m.replace('(url)', 'babah24.ru')
			#пол
			if data.sex:
				if data.sex == 'male':
					m=m.replace('(mr)', u'Уважаемый')
				if data.sex == 'female':
					m=m.replace('(mr)', u'Уважаемая')
			else:
				m=m.replace('(mr)', u'Ув.')
			#backlinkurl
			backhash = backlink_generator();
			m=m.replace('(backurl)', 'babah24.ru/?back=%s' % backhash)
			#redirect from nginx
			#m=m.replace('(backurl2)', 'babah24.ru/back_%s' % backhash)
			#
			
			#бонусы
			databonus=data.discountcard_set.all().aggregate(s=Sum('bonus'))['s']
			if databonus > float(1):
				bonus = round(float(databonus))
				m=m.replace('(bonus)', '%.0f' % bonus)
			else:
				m=m.replace('(bonus)', '')
	
			#	
			#добавляем имя ребенка
			if 'childid' in request.GET:
				try:
					c=child.objects.get(id=request.GET['childid'])
				except:
					pass
				else:
					m=m.replace('(childname)', c.name)
			m=m.replace('(childname)', '') #if empty, replace to ''

			s=smsqsend(status=True, buyer=data, message=m, backurl=backhash)
			s.save()
			tmp={'res': 1, 'data': s.id,}
			return HttpResponse(json.dumps(tmp), content_type='application/json')
	tmp={'res': 0, 'data': u'bad',}
	return HttpResponse(json.dumps(tmp), content_type='application/json')
	
	

@permission_required('sms.add_smsqsend')
def smsqsend_clear(request):
	if request.method == 'GET':
		smsqsend.objects.filter(send=False).delete()
	return HttpResponseRedirect('/smsqsend/list')
	
	
@csrf_exempt
def checkbackurl(request, backurl):
	if request.method == 'GET':
		data = smsqsend.objects.filter(back=False, backurl=backurl)
		if data.exists():
			data.update(back=True)
			tmp={'res': 1}
			return HttpResponse(json.dumps(tmp), content_type='application/json')
	tmp={'res': 0, 'data': u'bad',}
	return HttpResponse(json.dumps(tmp), content_type='application/json')
	
	
class user_password(FormView):
	template_name = 'user_password.html'
	form_class = Form_change_password
	success_url = "/user/login?passwd=change"

	def form_valid(self, form):
		cd = form.cleaned_data
		u = User.objects.get(id__exact=self.request.user.id)
		u.set_password(cd['password'])
		u.save()
		auth.logout(self.request)
		return super(user_password, self).form_valid(form)
		

		
		
		
		
		
		
		
		
		
##ДЕТИ
class Form_filter_child(forms.Form):
	q = forms.CharField(label='Поиск', help_text='Введите слово для поиска', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'off'}), max_length=100, required=False)
	
	dm = forms.BooleanField(label="Фильтр только день и месяц (игнорировать год)", required=False, initial=True,)
	
	bdstart = forms.DateField(label="Д.Р. Старт", help_text='День рождения от', input_formats=['%d-%m-%y', '%d-%m-%Y',], required=False, widget=forms.TextInput(attrs={'class':'form-control datepicker',  'data-dateformat': "dd-mm-yy"}))
	bdend = forms.DateField(label="Д.Р. Конец", help_text='День рождения до', input_formats=['%d-%m-%y', '%d-%m-%Y',], required=False, widget=forms.TextInput(attrs={'class':'form-control datepicker',	 'data-dateformat': "dd-mm-yy"}))
	
	age = []
	age.append(('', '---'))
	for i in range(1,18):
		age.append((i,i))

	agestart = forms.ChoiceField(label="Возраст от", help_text='От скольки лет', required=False, choices=age)
	ageend = forms.ChoiceField(label="Возраст до", help_text='До скольки лет', required=False, choices=age)
	
	#sort = forms.ChoiceField(label='Сортировка', help_text='Сортировать по полю', widget=forms.Select(attrs={'class': 'form-control'}), choices=(('id', 'id'),('bday', 'Д. Рождения'),('f', 'Фамилия'),('i', 'Имя'),('o', 'Отчество')), required=False)
	
	#согласие на рассылку
	adv = forms.ChoiceField(label='Согласие на рассылку', widget=forms.Select(attrs={'class': 'form-control'}), choices=(('all', 'Все'),('true', 'Да'),('false', 'Нет'),), initial='all', required=False)

	
@method_decorator(permission_required('node.add_child'), name='dispatch')
class panel_child_list(ListView):
	template_name = 'child_list.html'
	model = child
	#paginate_by = 10
	
	def dispatch(self, request, *args, **kwargs):
		return super(panel_child_list, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(panel_child_list, self).get_queryset()
		
		data=data.all() #выбираем основной запрос
		
		f=Form_filter_child(self.request.GET)
		
		
		
		req = ''
		
		if f.is_valid():
			fdata = f.cleaned_data
			#фильтрация
			if fdata['q']:
				req = '%s&q=%s' % (req, fdata['q'])
				data=data.filter(Q(id__icontains=fdata['q']) | Q(id1c__icontains=fdata['q']) | Q(name__icontains=fdata['q']))
			
			
			if fdata['bdstart'] and fdata['bdend']:
				req = '%s&bdstart=%s' % (req, self.request.GET['bdstart'])
				req = '%s&bdend=%s' % (req, self.request.GET['bdend'])
				if fdata['dm'] == True: #фильтр только день месяц, игнорировать год
					req = '%s&dm=%s' % (req, self.request.GET['dm'])
					s = fdata['bdstart']
					e = fdata['bdend']
					count = (e-s).days
					count=count+1
					dlist = []
					for x in range(0, count):
						dlist.append(s + datetime.timedelta(days=x))
					dindex = []
					for date in dlist:
						dindex.append(date.strftime("%d%m")) 
					data=data.filter(bdayindex__in=dindex)	 
				else: #полный фильтр день месяц год
					data=data.filter(bday__range=(fdata['bdstart'], fdata['bdend']))
			
			
			if fdata['agestart'] and fdata['ageend']:
				req = '%s&agestart=%s' % (req, self.request.GET['agestart'])
				req = '%s&ageend=%s' % (req, self.request.GET['ageend'])

				'''
				agestart = fdata['agestart']
				ageend = fdata['ageend']
				start = datetime.datetime.now().date()
				end = datetime.datetime.now().date()
				startyear = start.year - int(agestart)
				start = start.replace(year=startyear)
				end = end.replace(year=startyear+(int(ageend)-int(agestart)))
				print start, end
				data=data.filter(bday__range=(start, end))
				'''
				agestart = fdata['agestart']
				ageend = fdata['ageend']
				
				start = datetime.datetime.now().date()
				end = datetime.datetime.now().date()
				
				#startyear = start.year - int(agestart)
				#start = start.replace(year=startyear)
				#end = end.replace(year=startyear+(int(ageend)-int(agestart)))
				
				filterstart = start.year - int(agestart)
				filterend =	 start.year - int(ageend)
				
				start = start.replace(year=filterstart)
				end =  end.replace(year=filterend)
				
				#print start, end
				data=data.filter(bday__range=(end, start))
				

			#if fdata['sort']:
			#	req = '%s&sort=%s' % (req, self.request.GET['sort'])
			#	data=data.order_by(fdata['sort'])
			
			if fdata['adv']:
				req = '%s&adv=%s' % (req, self.request.GET['adv'])
				if fdata['adv'] == 'true':
					data=data.filter(buyer__adv=True)
				if fdata['adv'] == 'false':
					data=data.filter(buyer__adv=False)

			
		self.req = req
			
		#data=data.order_by('-id')

		
		#paginator
		self.p = Paginator(data, 20)
		page = self.kwargs['page']
		#print self.p.number()
		try:
			pdata = self.p.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			pdata = self.p.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			pdata = self.p.page(self.p.num_pages)
		
		
		return pdata
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(panel_child_list, self).get_context_data(*args, **kwargs)
		context_data.update({'req': self.req,})
		context_data.update({'count': self.p.count,})
		context_data.update({'form': Form_filter_child(self.request.GET),})
		return context_data


#@csrf_exempt
@permission_required('panel.add_childbook')
def childbook_add(request, pk):
	if request.method == 'GET':
		try:
			data = child.objects.get(id=pk)
		except:
			pass
		else:
			childbook.objects.create(child=data)
			tmp={'res': 1, 'data': data.id,}
			return HttpResponse(json.dumps(tmp), content_type='application/json')
	tmp={'res': 0, 'data': u'bad',}
	return HttpResponse(json.dumps(tmp), content_type='application/json')
		

@method_decorator(permission_required('panel.add_childbook'), name='dispatch')
class childbook_list(ListView):
	template_name = 'childbook_list.html'
	model = childbook
	paginate_by = 20
	
	def dispatch(self, request, *args, **kwargs):
		return super(childbook_list, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(childbook_list, self).get_queryset()
		#data=data.filter(user=self.request.user) #выбираем основной запрос
		return data
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(childbook_list, self).get_context_data(*args, **kwargs)
		#context_data.update({'req': self.req,})
		return context_data	
		
		
@method_decorator(permission_required('panel.add_childbook'), name='dispatch')		
class childbook_del(DeleteView):
	model = childbook
	template_name = '_confirm_delete.html'
	success_url = '/childbook/list/'

	def dispatch(self, request, *args, **kwargs):
		self.data = get_object_or_404(self.model, id=self.kwargs['pk'])
		return super(childbook_del, self).dispatch(request, *args, **kwargs)
	
	#def get_object(self, queryset=None):
	#	return get_object_or_404(self.model, id=self.kwargs['pk'])
		
	def get_context_data(self, **kwargs):
		context = super(childbook_del, self).get_context_data(**kwargs)
		context['object'] = self.data.id
		context['msg'] = u'Вы уверены что хотите удалить '
		context['back_url'] = '/childbook/list/'
		return context


@permission_required('panel.add_childbook')
def childbook_clear(request):
	if request.method == 'GET':
		childbook.objects.all().delete()
	return HttpResponseRedirect('/childbook/list')
		
		
@method_decorator(permission_required('panel.add_childbook'), name='dispatch')
class childbook_text(childbook_list):
	template_name = 'childbook_text.html'
	paginate_by = 1000
	
	
	
#@csrf_exempt
@permission_required('sms.add_smsqsend')
def makecall(request, pk):
	if request.method == 'GET':
		try:
			data = buyer.objects.get(id=pk)
		except:
			pass
		else:
			m=mobilon(request.user, data.phone)
			if m:
				tmp={'res': 1, 'data': data.id,}
				return HttpResponse(json.dumps(tmp), content_type='application/json')
	tmp={'res': 0, 'data': u'bad',}
	return HttpResponse(json.dumps(tmp), content_type='application/json')

	
	
	
	
@method_decorator(permission_required('sms.add_smsreport'), name='dispatch')
class owncallreport_list(ListView):
	template_name = 'callreport_list.html'
	model = callreport
	paginate_by = 20
	
	def dispatch(self, request, *args, **kwargs):
		return super(owncallreport_list, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(owncallreport_list, self).get_queryset()
		data=data.filter(user=self.request.user) #выбираем основной запрос
		return data
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(owncallreport_list, self).get_context_data(*args, **kwargs)
		#сколько отправил пользователь за сегодня
		ucount=self.model.objects.filter(user=self.request.user,  time__gt=datetime.date.today()).count()	
		context_data.update({'ucount': ucount,})
		return context_data
		
		
		
		
		
		
		

#@method_decorator(permission_required('panel.add_goodfix'), name='dispatch')
class panel_goodfix_add(CreateView):
	model = goodfix
	template_name = 'panel_goodfix_add.html'
	#form_class = Form_create_nickname
	success_url = '/panel/goodfix/add/?success=true'
	fields = ['goods', 'priority', 'link', 'name', 'message',]
	
	def dispatch(self, request, *args, **kwargs):
		return super(panel_goodfix_add, self).dispatch(request, *args, **kwargs)

	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
			form = super(panel_goodfix_add, self).get_form(form_class)
			form.fields['goods'].widget.attrs['data-placeholder'] = 'Choose a Country'
			form.fields['goods'].widget.attrs['class'] = 'chosen-select'
			return form
		return form_class(**self.get_form_kwargs())
	
	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.user = self.request.user
		instance.save() 
		return super(panel_goodfix_add, self).form_valid(form)
		

@method_decorator(permission_required('panel.add_goodfix'), name='dispatch')
class panel_goodfix_list(ListView):
	template_name = 'panel_goodfix_list.html'
	model = goodfix
	paginate_by = 20
	
	def dispatch(self, request, *args, **kwargs):
		return super(panel_goodfix_list, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(panel_goodfix_list, self).get_queryset()
		#data=data.filter(user=self.request.user) #выбираем основной запрос
		return data
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(panel_goodfix_list, self).get_context_data(*args, **kwargs)
		#context_data.update({'req': self.req,})
		return context_data		
		
		
@method_decorator(permission_required('panel.add_goodfix'), name='dispatch')	
class panel_goodfix_edit(UpdateView):
	model = goodfix
	template_name = 'panel_goodfix_edit.html'
	success_url = '/panel/goodfix/list/'
	fields = ['status', ]
	
	def dispatch(self, request, *args, **kwargs):
		#data = get_object_or_404(self.model, status=True, id=self.kwargs['pk'])
		return super(panel_goodfix_edit, self).dispatch(request, *args, **kwargs)
		
		
		
		
		
		
		
		
		
		
		
		
		
#discounts скидки
@method_decorator(permission_required('node.add_discounts'), name='dispatch')
class discount_list(ListView):
	template_name = 'discount_list.html'
	model = discounts
	paginate_by = 20
		
@method_decorator(permission_required('node.add_discounts'), name='dispatch')
class discount_add(CreateView):
	model = discounts
	template_name = 'discount_add.html'
	success_url = '/discount/list'
	fields = ['status', 'id1c', 'name',]

@method_decorator(permission_required('node.add_discounts'), name='dispatch')
class discount_edit(UpdateView):
	model = discounts
	template_name = 'discount_edit.html'
	success_url = '/discount/list'
	fields = ['status', 'id1c', 'name',]
#################
			
#goodscert сертификаты
@method_decorator(permission_required('node.add_goodscert'), name='dispatch')
class goodscert_list(ListView):
	template_name = 'goodscert_list.html'
	model = goodscert
	paginate_by = 80
		
@method_decorator(permission_required('node.add_goodscert'), name='dispatch')
class goodscert_add(CreateView):
	model = goodscert
	template_name = 'goodscert_add.html'
	success_url = '/goodscert/list'
	fields = ['name', 'datestart', 'dateend', 'pdf', 'org',]

@method_decorator(permission_required('node.add_goodscert'), name='dispatch')
class goodscert_edit(UpdateView):
	model = goodscert
	template_name = 'goodscert_edit.html'
	success_url = '/goodscert/list'
	fields = ['name', 'datestart', 'dateend', 'pdf', 'org',]
#################




#привязка сертификата к множеству товаров
class Form_goodscert_goods(forms.Form):
	inputcert = forms.ModelChoiceField(label="Сертификат", queryset = goodscert.objects.all(),required=True)
	inputgoods = forms.ModelMultipleChoiceField(label="Товары", help_text='Выбрать несколько товаров', queryset = goods.objects.all(), required=True)

@method_decorator(permission_required('node.add_goodscert'), name='dispatch')
class goodscert_goods(FormView):
	template_name = 'goodscert_goods.html'
	success_url = '/goodscert/list/'
	form_class = Form_goodscert_goods
	
	def dispatch(self, request, *args, **kwargs):
		return super(goodscert_goods, self).dispatch(request, *args, **kwargs)

	# def get_context_data(self, **kwargs):
		# context = super(goodscert_goods, self).get_context_data(**kwargs)
		# #context['nickname'] = self.data.name
		# return context
		
	def form_valid(self, form):
		cd = form.cleaned_data
		cd['inputgoods'].update(goodscert=cd['inputcert'])
		#НЕ ЗАБЫТЬ ОБРАБОТКУ ТОВАРОВ ИЗ CONVERSATION.CSV ДЛЯ СЕРТИФИКАТОВ
		return super(goodscert_goods, self).form_valid(form)



#@method_decorator(permission_required('panel.add_saleplanshop'), name='dispatch')
class saleplanshop_list(ListView):
	template_name = 'saleplanshop_list.html'
	model = saleplanshop
	#paginate_by = 20
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'motivation_list', 'R') #проверяем права
		return super(saleplanshop_list, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		data=super(saleplanshop_list, self).get_queryset()
		#self.data=data.filter(user=self.request.user).order_by('-id')
		self.data=data.all().order_by('-edate')
		return self.data
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(saleplanshop_list, self).get_context_data(*args, **kwargs)
		#context_data.update({'command': True,})
		return context_data



#@method_decorator(permission_required('panel.add_saleplanshop'), name='dispatch')
class saleplanshop_add(CreateView):
	model = saleplanshop
	template_name = 'saleplanshop_add.html'
	success_url = '/panel/saleplanshop/list'
	fields = ['name', 'value', 'shop', 'sdate', 'edate',]

	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'motivation_list', 'R') #проверяем права
		#self.b = get_object_or_404(self.model, id=self.kwargs['pk'])
		return super(saleplanshop_add, self).dispatch(request, *args, **kwargs)
	
	#def get_success_url(self):
	#	return '%s/%s' % (self.success_url, self.hashkey)
	
	def get_context_data(self, **kwargs):
		context = super(saleplanshop_add, self).get_context_data(**kwargs)
		#context['object'] = self.b
		return context
	
	#def get_initial(self):
	#	return {'user': self.request.user}
		
	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
			form = super(saleplanshop_add, self).get_form(form_class)
			#form.fields['buyer'].widget=forms.HiddenInput()
			#form.fields['buyer'].widget.attrs['readonly'] = True
			#form.fields['user'].widget=forms.HiddenInput()
			return form
		return form_class(**self.get_form_kwargs())
	
	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.save()
		return super(saleplanshop_add, self).form_valid(form)

#@method_decorator(permission_required('panel.add_saleplanshop'), name='dispatch')
class saleplanshop_edit(UpdateView):
	model = saleplanshop
	template_name = 'saleplanshop_edit.html'
	success_url = '/panel/saleplanshop/list'
	fields = ['name', 'value', 'shop', 'sdate', 'edate',]
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_denied(self.request.user, 'motivation_list', 'R') #проверяем права
		#self.e = get_object_or_404(self.model, id=self.kwargs['pk'], user=request.user)
		return super(saleplanshop_edit, self).dispatch(request, *args, **kwargs)
	
	#def get_success_url(self):
	#	return '%s/%s' % (self.success_url, self.hashkey)
	
	def get_context_data(self, **kwargs):
		context = super(saleplanshop_edit, self).get_context_data(**kwargs)
		#context['object'] = self.get_object()
		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.save()
		return super(saleplanshop_edit, self).form_valid(form)



		
		
		
		
		
		
		
		
		
		
		
		
		
		

		


@permission_required('node.add_buyer')
def getphone(request, pk):
	if request.method == 'GET':
		b=get_object_or_404(buyer, id=pk)
		res={'res': 1, 'phone': b.phone}
		return HttpResponse(json.dumps(res), content_type='application/json')

	res={'res': 0, 'data': u'Ошибка',}
	return HttpResponse(json.dumps(res), content_type='application/json')
		

#Редактировать собственный профиль пользователя		
class own_user_profile_edit(UpdateView):
	model = profileuser
	template_name = 'own_user_profile_edit.html'
	success_url = '/user/profile'
	fields = ['photo', 'position', 'phonemobile', 'phonework', ]
	
	def dispatch(self, request, *args, **kwargs):
		self.e = get_object_or_404(self.model, user=request.user)
		return super(own_user_profile_edit, self).dispatch(request, *args, **kwargs)
	
	#def get_success_url(self):
	#	return '/user/profile/%s' % (self.get_object().id)
	
	def get_object(self, queryset=None):
		return get_object_or_404(self.model, user=self.request.user)
	
	def get_context_data(self, **kwargs):
		context = super(own_user_profile_edit, self).get_context_data(**kwargs)
		context['object'] = self.get_object()
		return context
		
		
		
class user_restore(FormView):
	template_name = 'restore.html'
	success_url = '/user/login?send=true'
	form_class = Form_user_restore
	
	def dispatch(self, request, *args, **kwargs):
		#self.data = get_object_or_404(sticker, id=self.kwargs['pk'], status=True)
		#проверяем на наличие купона на изминение стикера
		#o = order.objects.filter(user=request.user, coupon__type__exact='sticker', status__exact='paid').first()
		#if not o:
		#	c = coupon.objects.get(type__exact='sticker')
		#	return HttpResponseRedirect('/order/%s' % c.id)
		return super(user_restore, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(user_restore, self).get_context_data(**kwargs)
		#context['nickname'] = self.data.name
		return context
		
	def form_valid(self, form):
		cd = form.cleaned_data
		p=profileuser.objects.get(phone=cd['phone'])
		newpass = password_generator()
		p.user.set_password(newpass)
		p.user.save()
		sms4b(None, '8%s' % cd['phone'], 'login: %s pass: %s' % (p.user.username, newpass))
		
		#удаляем предыдущие связи
		#d = stickerowner.objects.filter(user=self.request.user, nickname=cd['nickname']).delete()
		#создаем новую
		#c = stickerowner.objects.create(user=self.request.user, nickname=cd['nickname'], sticker=cd['sticker'])
		#гасим купон
		#order.objects.filter(user=self.request.user, coupon__type__exact='sticker', status__exact='paid').update(status='used', desc2='changesticker to %s' % self.kwargs['pk'])
		return super(user_restore, self).form_valid(form)
		

@permission_required('panel.delete_imagebase')
def imagebase_del(request, pk):
	tmp={'res': 0, 'data': u'Ошибка',}
	if request.method == 'POST' or request.method == 'GET':
		try:
			data=imagebase.objects.get(id=pk)
		except:
			tmp={'res': 0, 'data': 'error',}
		else:
			data.delete()
			tmp={'res': 1, 'data': 'delete',}
	return HttpResponse(json.dumps(tmp), content_type='application/json')	
		
