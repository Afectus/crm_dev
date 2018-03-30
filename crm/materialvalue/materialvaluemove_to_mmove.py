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
from django.db.models.functions import Coalesce
from django.db.models.functions import Cast, Trunc, TruncMonth, ExtractYear, ExtractMonth, ExtractWeek, ExtractWeekDay, ExtractDay
from ckeditor.widgets import CKEditorWidget
from dj.views import *
from django.core.mail import send_mail
from node.templatetags.nodetag import *
from node.models import *

from materialvalue.models import *


data = materialvaluemove.objects.all()
	
	
# for i in data:
	# print(i.materialvalue.id)
	# #print(i.stock.id1c)
	
	# #
	# tmpmove = None
	
	# if i.shop != None:
		# print(i.shop.id1c)
		# tmpmove = shopstock.objects.get(type='shop', id1c=i.shop.id1c)

	# if i.stock != None:
		# print(i.stock.id1c)
		# tmpmove = shopstock.objects.get(type='stock', id1c=i.stock.id1c)
	
	# if i.materialvaluegmove != None:
		# print(i.materialvaluegmove.id)
		
		
	# a=mvmove(materialvalue=i.materialvalue, shopstock=tmpmove)
	# a.materialvaluegmove = i.materialvaluegmove
	# a.note = i.note
	# a.mdate = i.mdate
	
	# a.save()

	
data = materialvaluemove.objects.filter(materialvalue__id=114)
for i in data:
	print(i.mdate)
