# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.shortcuts import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponsePermanentRedirect

from django.core.exceptions import PermissionDenied

from django import forms
from django.contrib.auth.models import User, Group

import json
from django.core import serializers

from django.http import QueryDict

from django.views.generic import DetailView, ListView, DeleteView
from django.views.generic.edit import CreateView, FormView, UpdateView, FormMixin
from django.views.generic.base import TemplateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt

from captcha.fields import CaptchaField
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

import datetime, time
from django.utils import formats

from .models import *

from dj.views import *
from sms.views import *


from node.models import *
from node.templatetags.nodetag import hidephone

from django.db.models import Sum, Count
from django.db.models import Q
from django.db.models.functions import Coalesce


#from node.templatetags.nodetags import node_count

import logging
log = logging.getLogger(__name__)

def validate_phone(value):
	p = re.compile('^9[0-9]{9}$')
	if not p.match(value):
		raise ValidationError(u'формат телефона должен быть например +79025112233. ')
	

class Formbuyerlogin(forms.Form):
	phone = forms.CharField(label='Мобильный телефон', help_text='Укажите мобильный телефон', widget=forms.TextInput(attrs={'class': 'form-control',}), max_length=10, required=True, validators=[validate_phone])
	
	code = forms.CharField(label='Проверочный код', widget=forms.TextInput(attrs={'class': 'form-control',}), max_length=6, required=False,)


@csrf_exempt
def buyerauthphone(request):
	log.info('buyerauthphone=%s' % 'start')
	tmp={'res': 0, 'data': u'Ошибка',}
	if request.method == 'POST' or request.method == 'GET':	
		form = Formbuyerlogin(request.POST)
		if form.is_valid():
			try:
				b=buyer.objects.get(phone=form.cleaned_data['phone'])
			except:
				tmp={'res': 0, 'data': u'Возможно вы не зарегистрированы в <a href="/info/club/" target="_blank">программе привилегий Бабах',}
				return HttpResponse(json.dumps(tmp), content_type='application/json')
			else:
				#задержка при отправке смс
				timeblock=b.authsmstime + datetime.timedelta(seconds=60)
				#print timeblock, datetime.datetime.now()
				if timeblock > datetime.datetime.now():
					tmp={'res': 2, 'data': u'Дождитесь ответа смс',}
					return HttpResponse(json.dumps(tmp), content_type='application/json')
				
				#
				code = sms_generator() #создаем код
				b.authcode = md5_generator(code) #пишем код в базу
				b.save()
				#отправляем смс
				log.info('Proverochnyj kod=%s' % code)
				text = u'Proverochnyj kod: %s' % code
				sms4b(None, '8%s' % b.phone, text)
				#
				tmp={'res': 1, 'data': 'generate code',}
	return HttpResponse(json.dumps(tmp), content_type='application/json')
	
@csrf_exempt
def buyerauthcode(request):
	tmp={'res': 0, 'data': u'Не верный проверочный код',}
	if request.method == 'POST' or request.method == 'GET':	
		form = Formbuyerlogin(request.POST)
		if form.is_valid():
			code = md5_generator(form.cleaned_data['code'])
			try:
				b=buyer.objects.get(phone=form.cleaned_data['phone'], authcode=code)
			except:
				tmp={'res': 0, 'data': u'Не верный проверочный код',}
			else:
				token = id_generator()
				b.authtoken = token
				b.authcode = ''
				b.save()
				tmp={'res': 1, 'data': token,}
	return HttpResponse(json.dumps(tmp), content_type='application/json')
	
	

@csrf_exempt
def buyerinfo(request, token):
	if request.method == 'POST' or request.method == 'GET':
		res={'res': 0, 'data': u'Ошибка',}
		try:
			b=buyer.objects.get(authtoken=token)
		except:
			pass
		else:
			res = {
				'res': 1, 
				'f': '***',
				'o': b.o, 
				'phone': hidephone(b.phone), 
				'bonus': b.discountcard_set.aggregate(s=Coalesce(Sum('bonus'),0))['s'], #b.bonus,
				'adv': b.adv,
			}
			if b.bday:
				res['bday'] = '%s-%s-****' % (b.bday.day, b.bday.month)
			else:
				res['bday'] = '-'
			
			if b.i:
				res['i'] = b.i
			else:
				res['i'] = '-'
				
			d=discountcard.objects.filter(buyer=b, status=True)
			if d.exists():
				res['dcard'] = d.first().name
			else:
				res['dcard'] = ''
				
			#отключение/включение рассылки
			if b.adv:
				res['advcontrol'] = '/api/buyer/adv/off/%s' % b.authtoken
			else:
				res['advcontrol'] = '/api/buyer/adv/on/%s' % b.authtoken
				
			#собираем все бонусы на всех картах
			res['bonus'] = b.discountcard_set.aggregate(s=Coalesce(Sum('bonus'),0))['s']
				
	return HttpResponse(json.dumps(res), content_type='application/json')
	
		
		
@csrf_exempt
def buyeradv(request, control, token):
	if request.method == 'POST' or request.method == 'GET':
		res={'res': 0, 'data': u'Ошибка',}
		try:
			b=buyer.objects.get(authtoken=token)
		except:
			pass
		else:
			if control == 'on':
				b.adv=True
			if control == 'off':
				b.adv=False
			b.save()
			res={'res': 1, 'data': u'adv',}
				
	#return HttpResponse(json.dumps(res), content_type='application/json')
	return HttpResponseRedirect('http://babah24.ru/c/buyer/')
		

		
class Formbuyermessage(forms.ModelForm):
	class Meta:
		model = buyermessage
		fields = ['message']	
		
@csrf_exempt
def buyermessagemake(request, token):
	tmp={'res': 0, 'data': u'Ошибка',}
	if request.method == 'POST' or request.method == 'GET':
		form = Formbuyermessage(request.POST)
		if form.is_valid():
			try:
				b=buyer.objects.get(authtoken=token)
			except:
				tmp={'res': 0, 'data': u'Ошибка',}
			else:
				#задержка при отправке
				tm = buyermessage.objects.filter().order_by('-ctime')
				if tm.exists():
					tm = tm.first()
					timeblock=tm.ctime + datetime.timedelta(seconds=10)
					if timeblock > datetime.datetime.now():
						tmp={'res': 0, 'data': u'Вы слишком часто отправляете запрос, подождите некоторое время.',}
						return HttpResponse(json.dumps(tmp), content_type='application/json')
				#
				bm = buyermessage.objects.create(buyer=b, message=form.cleaned_data['message'])
				tmp={'res': 1, 'data': bm.id,}
		else:
			tmp={'res': 0, 'data': u'Заполните форму',}
	return HttpResponse(json.dumps(tmp), content_type='application/json')




		
		
class Form_create_review(forms.ModelForm):
	cap = CaptchaField(label='Проверочное слово',)
	phone = forms.CharField(label='Мобильный телефон', help_text='Укажите мобильный телефон', max_length=11, required=True, validators=[validate_phone])
		
	class Meta:
		model = review
		fields = ['subj', 'uname', 'email', 'order', 'message']

@method_decorator(csrf_exempt, name='dispatch')
class review_create(CreateView):
	model = review
	template_name = 'bitrix/review_create.html'
	form_class = Form_create_review
	success_url = '/bitrix/review/add'
	#fields = ['uname', 'email', 'order', 'message']
	
	def dispatch(self, request, *args, **kwargs):
		#return HttpResponseRedirect('/order/%s' % c.id)
		return super(review_create, self).dispatch(request, *args, **kwargs)
	
	#def get_success_url(self):
	#	return '%s/%s' % (self.success_url, self.hashkey)
	
	#def get_context_data(self, **kwargs):
	#	context = super(review_create, self).get_context_data(**kwargs)
		#context['header'] = u'Добавить %s' % self.model._meta.verbose_name
	#	return context
	
	#def get_initial(self):
		#nodetype=self.request.GET.get('type', 'sound')
		#return {'type':nodetype,}
	
	#def get_form(self, form_class):
		#form = super(review_create, self).get_form(form_class)
		#form.fields['name'].widget=forms.TextInput({'class': 'form-control'})
		#form.fields['passwd'].widget=forms.TextInput({'class': 'form-control'})
		#return form
		
	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.phone = form.data['phone']
		instance.save() 
		#form.instance.phone = self.request.user
		#form.save()
		#r=review.objects.create(subj=form.instance.subj, uname=form.instance.uname, email=form.instance.email, phone=form.instance.phone, order=form.instance.order, message=form.instance.message)
		tmp={'res': 1,}
		return HttpResponse(json.dumps(tmp), content_type='application/json')
		return super(review_create, self).form_valid(form)
		
	def form_invalid(self, form):
		tmp={'res': 0, 'error': form.errors,}
		return HttpResponse(json.dumps(tmp), content_type='application/json')
		return super(review_create, self).form_invalid(form)

	
	

class bitrixreviewlist(ListView):
	template_name = 'bitrix_review_list.html'
	model = review
	#paginate_by = 1000
	
	def get_queryset(self):
		data=super(bitrixreviewlist, self).get_queryset()
		data=data.filter(status=True, subj='recall')
		return data
		
	def get_context_data(self, *args, **kwargs):
		context_data = super(bitrixreviewlist, self).get_context_data(*args, **kwargs)
		#context_data.update({'a':a,})
		return context_data
		
		
		
		
