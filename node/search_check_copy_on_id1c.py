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

from django import forms
from django.core.exceptions import ValidationError
from django.contrib import auth
from django.contrib.auth.models import User, Group
import json
from django.core import serializers
from django.http import QueryDict
import datetime, time
from django.db.models import Min, Max, Sum, Count, Avg
from django.db.models import Q, F, Func, Value, IntegerField, FloatField, CharField, Case, When
from django.db.models.functions import Coalesce
from django.db.models.functions import Cast, Trunc, TruncMonth, ExtractYear, ExtractMonth, ExtractWeek, ExtractWeekDay, ExtractDay
from ckeditor.widgets import CKEditorWidget
from dj.views import *
from node.models import *


#поиск дублей чеков по id1c

now = datetime.datetime.now()
start=now.replace(day=1)

#берем магазин
s=shop.objects.get(id=6)

data=check.objects.all()

data=data.exclude(process='copy') #исключаем уже определенные копии

#data=data.filter(shop=s)
#data=data.filter(fcheck__time__date__gte=start)
#data=data.filter(time__month=now.month, time__year=now.year)


for i in data:
	r=data.filter(id1c=i.id1c).exclude(id=i.id)
	if r.exists():
		print i.id1c
		for rr in r:
			print rr.id1c
	



