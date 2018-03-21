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


now = datetime.datetime.now()
start=now.replace(day=1)

#checkitem.objects.filter(fcheck__shop__id=6, fcheck__time__month=now.month, fcheck__time__year=now.year).aggregate(s=Sum('sum'))


#checkitem.objects.filter(fcheck__shop__id=6, fcheck__time__date__gte=s).aggregate(s=Sum('sum'))


#берем магазин
s=shop.objects.get(id=6)




data=checkitem.objects.filter(fcheck__shop=s)
#data=data.filter(fcheck__time__date__gte=start)
data=data.filter(fcheck__time__month=now.month, fcheck__time__year=now.year)


data=data.annotate(s=Sum('price')*Count('col'))

data=data.annotate(s=F('price')*F('col'))

data=data.annotate(d=Sum('checkd__discount'))

data=data.annotate(d=Case(When(checkd__discount__isnull=True, then=0), default=Sum('checkd__discount')))


#применять с делением на ноль
#data=data.annotate(d2=Case(When(totaldiscount=0, then=0), default=(F('s')/100)*F('totaldiscount')))

data=data.annotate(d2=(F('s')/100)*F('totaldiscount'))


data=data.annotate(r=F('s')-F('d')-F('d2'))

for i in data:
	print '%s | %s*%s=%s | (%s*100)/%s=%s | %s-%s-%s=%s (%s)' % (
		i.fcheck.id, 
		i.col, i.price, i.s, 
		i.s, i.totaldiscount, i.d2, 
		i.s, i.d, i.d2, i.r, i.sum
		)






