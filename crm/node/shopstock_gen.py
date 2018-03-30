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
from django.db.models import Min, Max, Sum, Count, Avg
from django.db.models import Q, F, Func, Value, IntegerField, FloatField, CharField, Case, When
from django.db.models.functions import Coalesce
from django.db.models.functions import Cast, Trunc, TruncMonth, ExtractYear, ExtractMonth, ExtractWeek, ExtractWeekDay, ExtractDay
from ckeditor.widgets import CKEditorWidget
from dj.views import *
from django.core.mail import send_mail
from node.templatetags.nodetag import *
from node.models import *


for i in shop.objects.all():
	print(i)
	try:
		newshop=shopstock.objects.get(id1c=i.id1c, type='shop')
	except:
		newshop=shopstock(status=i.status, id1c=i.id1c, name=i.name, type='shop')
	
	newshop.status=i.status
	newshop.id1c=i.id1c
	newshop.name=i.name
	newshop.type='shop'
	#
	newshop.htmlcolor=i.htmlcolor
	newshop.sort=i.sort
	newshop.motivationratio=i.motivationratio
	newshop.save()
		
		
for i in stock.objects.all():
	print(i)
	try:
		newstock=shopstock.objects.get(id1c=i.id1c, type='stock')
	except:
		newstock=shopstock(status=i.status, id1c=i.id1c, name=i.name, type='stock')
	

	newstock.status=i.status
	newstock.id1c=i.id1c
	newstock.name=i.name
	newstock.type='stock'
	#
	newstock.base=i.base
	newstock.idbitrix=i.idbitrix
	newstock.typestock=i.typestock
	newstock.organization=i.organization
	#
	try:
		s=shopstock.objects.get(id1c=i.shop.id1c, type='shop')
	except:
		pass
	else:
		newstock.shop=s
	#
	newstock.desc=i.desc
	newstock.save()
		
		
		
		
		
		
		
		




