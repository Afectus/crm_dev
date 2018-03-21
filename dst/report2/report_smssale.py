#!/usr/bin/python
# -*- coding: utf-8 -*-

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
from django.db.models.functions import Cast, Trunc, TruncMonth, ExtractYear, ExtractMonth, ExtractWeek, ExtractWeekDay, ExtractDay
from ckeditor.widgets import CKEditorWidget
from dj.views import *
from django.core.mail import send_mail
from node.templatetags.nodetag import *
from node.models import *
from sms.models import *



#s=datetime.date(1987, 01, 01)
#e=datetime.date(1987, 01, 10)
####################################################################################
#data=buyer.objects.all()
#data=data.filter(bday__range=(s, e))



# shopratio = 100

# s=shop.objects.get(id=6) #доммер

# data=goods.objects.filter(checkitem__fcheck__shop=s, checkitem__operation='sale')

# data=data.annotate(countsale=Sum('checkitem__col'))
# data=data.annotate(sumpoints=Cast(F('countsale')*F('motivationinpoints'),FloatField()))
# data=data.annotate(ratio=Cast(F('sumpoints')*Value(shopratio),FloatField()))

# for i in data:
	# print '|', i.id, i.name, '|', i.countsale, '|', i.motivationinpoints, '|', i.sumpoints, '|', i.ratio
	
	
# total = data.aggregate(total=Sum('ratio'))
# print total
	
	
data=smsqsend.objects.all()

#data=data.annotate(ccheck=Count('buyer__check'))

data=data[:100]

for i in data:
	print i.cdate, i.buyer
	for c in i.buyer.check_set.filter():
		print c
	
	
	
	
	
	

