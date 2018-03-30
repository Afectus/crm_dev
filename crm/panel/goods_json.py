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

from django.db.models import Min, Max, Sum, Count, Avg, Q, F, Func, Value, IntegerField, FloatField, CharField, Case, When, ExpressionWrapper

from django.db.models.functions import Cast, Trunc, TruncMonth, ExtractYear, ExtractMonth, ExtractWeek, ExtractWeekDay, ExtractDay

from django.db.models.expressions import RawSQL

from ckeditor.widgets import CKEditorWidget

from django.core.mail import send_mail

from dj.views import *
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




@csrf_exempt
def motivation_report_list_json(request):
	log.info('start=motivation_report_list_json')
	log.info('url=%s' % request.get_full_path())
	log.info('request.body=%s' % request.body)
	if request.method == 'POST' or request.method == 'GET':
		#старт отчета
		jdata=[]
		now = datetime.datetime.now()
		start=now.replace(day=1)
		
		#основная выборка данных
		cdata =  checkitem.objects.all()
		#отсекаем чеки по дате
		cdata = cdata.filter(fcheck__time__month=now.month, fcheck__time__year=now.year) 

		cdata=cdata.exclude(fcheck__process='copy') #отсекаем копии
		cdata=cdata.exclude(fcheck__status='Аннулированный')
		#c=data.exclude(fcheck__status='Архивный')
		cdata=cdata.exclude(fcheck__status='Отложенный')
		cdata=cdata.exclude(fcheck__status='Пробитый')
		cdata=cdata.filter(fcheck__operation='sale') #только продажи
		
		cdata = cdata.exclude(goods__isnull=True) #отсекаем чеки без товаров, если отключить, в выдаче может присутствовать None, не будет влиять на расчет мотивации #НУЖНО ПРОВЕРИТЬ ПОЧЕМУ ЧЕКИ БЕЗ ТОВАРОВ
		
		cdata = cdata.exclude(goods__motivationinpoints1__isnull=True) #отсекаем чеки без товаров и товары без привязанной категории, если отключить, в выдаче может присутствовать None
		
		for i in shop.objects.all(): #for i in shop.objects.filter(id=6):
			data=cdata.filter(fcheck__shop=i) #фильтр по магазину
			
			#план продаж
			plandata=i.saleplanshop_set.filter(sdate__month=now.month).order_by('sdate')
			plansum=False
			planstart=False
			plantotal=False
			
			if plandata.exists():
				plan=plandata.last()
				plansum=plan.value
				planstart=plan.sdate
				plantotal=data.aggregate(Sum('sum'))['sum__sum']
				
			#выборка полей
			data=data.values(
				'goods__motivationinpoints1__ratio', 
				'goods__motivationinpoints1__name', 
				'goods__motivationinpoints1__id'
				)
			
			#МОТИВАЦИЯ #сумма цен проданных товаров
			data=data.annotate(
				leftcol=Sum('col'),
				rightcol=Sum('col'), #переопределяется RawSQL
				leftsum=Sum('sum'),
				rightsum=Sum('price'), #переопределяется RawSQL
				leftbonusper=F('goods__motivationinpoints1__percent'),
				rightbonusper=F('goods__motivationinpoints1__dpercent'),
				)

			
			#RIGHTCOL
			#rightcol = goodsinstock.objects.filter(goods__motivationinpoints1__ratio=10)
			#rightcol = col.aggregate(s=Sum('value'))
			#data=data.annotate(cc=F('goods__motivationinpoints1__ratio'))
			#data=data.annotate(rightcol=RawSQL('SELECT SUM(value) FROM node_goodsinstock INNER JOIN node_goods_goodsinstock ON (node_goodsinstock.id = node_goods_goodsinstock.goodsinstock_id) INNER JOIN node_goods ON (node_goods_goodsinstock.goods_id = node_goods.id) INNER JOIN node_goodsmotivationratiosum ON (node_goods.motivationinpoints1_id = node_goodsmotivationratiosum.id) WHERE node_goodsmotivationratiosum.ratio = node_goods.motivationinpoints1_ratio', ()))

			#RIGHTSUM
			#rightsum = goods.objects.filter(motivationinpoints1__ratio=10)
			#rightsum=rightsum.annotate(sum=ExpressionWrapper(F('price')*Sum('goodsinstock__value'), output_field=FloatField()))
			#rightsum = rightsum.aggregate(s=Sum('sum'))
			
			
			#rightsum=goodsinstock.objects.filter(goods__motivationinpoints1__ratio=data['goods__motivationinpoints1__ratio']).aggregate(Sum('goods__price'))['goods__price__sum']
			#rightsum=1000
			data=data.annotate(
				leftbonussum=(F('leftsum')/100)*F('leftbonusper'),
				rightbonussum=(F('rightsum')/100)*F('rightbonusper'),
				)
			
			data=data.annotate(leftres=F('leftbonussum')*i.motivationratio)
			data=data.annotate(rightres=F('rightcol')*F('rightbonussum')*i.motivationratio)
			
			#МОТИВАЦИЯ - ДЕМОТИВАЦИЯ = totalres
			data=data.annotate(totalres=ExpressionWrapper(F('leftres')-F('rightres'), output_field=FloatField()))
			#
			
			#ТОТАЛЬНЫЙ ПОДСЧЕТ
			#leftrighttotal=data.aggregate(leftrighttotal=Sum('totalres'))['leftrighttotal'] #сумма заработанных бонусов
			lefttotalcol=data.aggregate(lefttotalcol=Sum('leftcol'))['lefttotalcol'] #общее количество товаров
			
			data=data.order_by('goods__motivationinpoints1__ratio') #сортировка

			if data.exists():
				#формирование json
				jshop={}
				jshop['id']=i.id
				jshop['name']=i.name
				jshop['mratio']=i.motivationratio
				jshop['lefttotalcol']=lefttotalcol
				#план продаж магазина
				jshop['planstart']=planstart
				jshop['plansum']=plansum
				jshop['plantotal']=plantotal
				#
				jshop['list']=[]
				
				
				lefttotal=0
				righttotal=0
				leftrighttotal=0
				for iter in data:
					#
					iter['rightcol']=goodsinstock.objects.filter(goods__motivationinpoints1__id=iter['goods__motivationinpoints1__id']).aggregate(s=Sum('value'))['s']
					#
					iter['rightsum'] = goods.objects.filter(motivationinpoints1__id=iter['goods__motivationinpoints1__id']).annotate(sum=ExpressionWrapper(F('price')*Sum('goodsinstock__value'), output_field=FloatField())).aggregate(s=Sum('sum'))['s']
					#
					iter['rightbonussum']=(iter['rightsum']/100)*iter['rightbonusper']
					#
					iter['rightres']=iter['rightbonussum']*i.motivationratio
					#
					iter['totalres']=iter['leftres']-iter['rightres']
					#
					#
					jshop['list'].append(iter)
					#
					lefttotal=lefttotal+iter['leftres']
					righttotal=righttotal+iter['rightres']
					leftrighttotal=leftrighttotal+iter['totalres']
					
				#
				jdata.append(jshop)
				#
				jshop['lefttotal']=lefttotal
				jshop['righttotal']=righttotal
				jshop['leftrighttotal']=leftrighttotal

		return render_to_response('motivation_json.html', {'object_list': jdata, 'startdate': start, 'enddate': now,})		

	
		

'''
@csrf_exempt
def motivation_report_list_json(request):
	log.info('start=motivation_report_list_json')
	log.info('url=%s' % request.get_full_path())
	log.info('request.body=%s' % request.body)
	if request.method == 'POST' or request.method == 'GET':
		#старт отчета
		jdata=[]
		now = datetime.datetime.now()
		start=now.replace(day=1)
		
		#основная выборка данных

		#отсекаем чеки по дате
		cdata = checkitem.objects.filter(fcheck__time__month=now.month, fcheck__time__year=now.year)

		# maindata=maindata.exclude(checkitem__fcheck__process='copy') #отсекаем копии
		# maindata=maindata.exclude(checkitem__fcheck__status='Аннулированный')
		# #maindata=maindata.exclude(checkitem__fcheck__status='Архивный')
		# maindata=maindata.exclude(checkitem__fcheck__status='Отложенный')
		# maindata=maindata.exclude(checkitem__fcheck__status='Пробитый')
		# maindata=maindata.filter(checkitem__fcheck__operation='sale') #только продажи
		
		# maindata = maindata.exclude(checkitem__goods__isnull=True) #отсекаем чеки без товаров, если отключить, в выдаче может присутствовать None, не будет влиять на расчет мотивации #НУЖНО ПРОВЕРИТЬ ПОЧЕМУ ЧЕКИ БЕЗ ТОВАРОВ
		
		# maindata = maindata.exclude(goods__motivationinpoints1__isnull=True) #отсекаем чеки без товаров и товары без привязанной категории, если отключить, в выдаче может присутствовать None
		
		maindata = goods.objects.filter(checkitem__in=cdata.values('id'))
		
		for i in shop.objects.all(): #for i in shop.objects.filter(id=6):
			data=maindata.filter(checkitem__fcheck__shop=i) #фильтр по магазину
			
			#план продаж
			plandata=i.saleplanshop_set.filter(sdate__month=now.month).order_by('sdate')
			plansum=False
			planstart=False
			plantotal=False
			
			if plandata.exists():
				plan=plandata.last()
				plansum=plan.value
				planstart=plan.sdate
				plantotal=data.aggregate(s=Sum('checkitem__sum'))['s']
				
			#выборка полей
			data=data.values(
				'motivationinpoints1__ratio', 
				'motivationinpoints1__name', 
				'motivationinpoints1__id'
				)
			
			#МОТИВАЦИЯ #сумма цен проданных товаров
			data=data.annotate(
				leftcol=Sum('checkitem__col'),
				rightcol=Sum('goodsinstock__value'),
				leftsum=Sum('checkitem__price'),
				rightsum=Sum('goodsinstock__goods__price'),
				leftbonusper=F('motivationinpoints1__percent'),
				rightbonusper=F('motivationinpoints1__dpercent'),
				)

			data=data.annotate(
				leftbonussum=(F('leftsum')/100)*F('leftbonusper'),
				rightbonussum=(F('rightsum')/100)*F('rightbonusper'),
				)
			
			
			data=data.annotate(rightcol=RawSQL("select count(id) from node_goods where price = %s", (200,)))
			
			data=data.annotate(leftres=F('leftcol')*F('leftbonussum')*i.motivationratio)
			data=data.annotate(rightres=F('rightcol')*F('rightbonussum')*i.motivationratio)
			
			#МОТИВАЦИЯ - ДЕМОТИВАЦИЯ = totalres
			data=data.annotate(totalres=ExpressionWrapper(F('leftres')-F('rightres'), output_field=FloatField()))
			#
			
			#ТОТАЛЬНЫЙ ПОДСЧЕТ
			totalsum=data.aggregate(totalsum=Sum('totalres'))['totalsum'] #сумма заработанных бонусов
			lefttotalcol=data.aggregate(lefttotalcol=Sum('leftcol'))['lefttotalcol'] #общее количество товаров
			
			data=data.order_by('motivationinpoints1__ratio') #сортировка

			if data.exists():
				#формирование json
				jshop={}
				jshop['id']=i.id
				jshop['name']=i.name
				jshop['mratio']=i.motivationratio
				jshop['totalsum']=totalsum
				jshop['lefttotalcol']=lefttotalcol
				#план продаж магазина
				jshop['planstart']=planstart
				jshop['plansum']=plansum
				jshop['plantotal']=plantotal
				#
				jshop['list']=[]
				
				for iter in data:
					#iter['rightsum']=rightsum
					jshop['list'].append(iter)
					pass
					
				#
				jdata.append(jshop)
				#

		return render_to_response('motivation_json1.html', {'object_list': jdata, 'startdate': start, 'enddate': now,})		


'''

		