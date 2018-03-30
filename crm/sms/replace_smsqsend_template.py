#!/usr/bin/python
# -*- coding: utf-8 -*-

#тест чеков с пустыми товарвами checkitem__goods__isnull=True
#в случае внесения чеков с товарами из базы номер 2
import sys, os, django

projecthome = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if projecthome not in sys.path:
    sys.path.append(projecthome)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj.settings")
django.setup()

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

from django.db.models import Min, Max, Sum, Count, Avg, Q, F, Func, Value, IntegerField, FloatField, CharField, Case, When, ExpressionWrapper

from django.db.models.functions import Cast, Coalesce, Trunc, TruncMonth, ExtractYear, ExtractMonth, ExtractWeek, ExtractWeekDay, ExtractDay

from ckeditor.widgets import CKEditorWidget
from dj.views import *
from django.core.mail import send_mail
from node.templatetags.nodetag import *
from node.models import *
from sms.models import *


data=smsqsend.objects.filter(send=False, status=True)

print data.count()

for i in data:
	t=smstemplate.objects.all().order_by('-sort')
	t=t.first() #берем первый шаблон
	m=t.message
	#фио
	m=m.replace('(f)', i.buyer.f)
	m=m.replace('(i)', i.buyer.i)
	m=m.replace('(o)', i.buyer.o)
	m=m.replace('(url)', 'babah24.ru')
	#пол
	if i.buyer.sex:
		if i.buyer.sex == 'male':
			m=m.replace('(mr)', u'Уважаемый')
		if i.buyer.sex == 'female':
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
	databonus=i.buyer.discountcard_set.all().aggregate(s=Sum('bonus'))['s']
	if databonus > float(1):
		bonus = round(float(databonus))
		m=m.replace('(bonus)', '%.0f' % bonus)
	else:
		m=m.replace('(bonus)', '')

	#	
	# #добавляем имя ребенка
	# if 'childid' in request.GET:
		# try:
			# c=child.objects.get(id=request.GET['childid'])
		# except:
			# pass
		# else:
			# m=m.replace('(childname)', c.name)
	# m=m.replace('(childname)', '') #if empty, replace to ''

	i.message=m 
	i.backurl=backhash
	i.save()





