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

from order.models import *
from workgraph.models import *

#reset all priority
resetdata=ordermanager.objects.filter(shift=True).update(sort=0)

#
today = datetime.date.today()
if today.isoweekday() == 6 or today.isoweekday() == 7:
	om=ordermanager.objects.filter(shift=True, schedule=today.isoweekday())
	print(today.isoweekday(), today)
	for i in om:
		data=workgraph.objects.filter(Q(user__user=i.user), Q(sdate=today) | Q(edate=today))
		if data.exists():
			print(i.user, data.first().sdate, data.first().edate)
			i.sort=20
			i.save()


print("=============================")
print("who will work on the day off?")
print("=============================")
data=ordermanager.objects.filter(schedule=6).order_by('-sort')[:3]
for i in data:
	print(i.user, i.schedule, i.sort)
	
data=ordermanager.objects.filter(schedule=7).order_by('-sort')[:3]
for i in data:
	print(i.user, i.schedule, i.sort)

