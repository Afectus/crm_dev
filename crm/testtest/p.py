#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, django

projecthome = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if projecthome not in sys.path:
    sys.path.append(projecthome)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj.settings")
django.setup()



import time
import requests
import datetime
from django.utils import timezone
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile

from testtest.models import *
from dj.views import *

#for i in goods.objects.filter(propertiesvalue__properties__code='KOL_RAZ'):
#    for ii in i.propertiesvalue_set.all():
#	print ii.properties.code,'=',ii.value

from django.db.models import Sum, Count, Q, F, IntegerField
from django.db.models.functions import Cast

from django.db.models import DateTimeField

from django.db.models.functions import Trunc, TruncMonth, ExtractMonth, ExtractYear, ExtractMonth, ExtractWeek, ExtractWeekDay, ExtractDay

a=datetime.date(2017, 1, 1)
b=datetime.date(2017, 5, 30)

data=check.objects.filter(time__range=(a, b)).annotate(month=TruncMonth('time')).values('month').annotate(s=Sum('nal')).order_by()

#print data


#data = check.objects.filter(time__range=(a, b)).annotate(month=TruncMonth('time')).values('month').annotate(c=Count('id'))

#data = check.objects.filter(time__range=(a, b)).annotate(start_day=TruncMonth('time', 'month')).values('start_day').annotate(experiments=Count('id'))

#data = test1.objects.annotate(month=TruncMonth('cdate')).values('month').annotate(c=Count('id'))


#for i in test1.objects.all(): print i.id, i.name, i.cdate

#data = test1.objects.annotate(month=TruncMonth('cdate')).values('month', 'name').annotate(c=Count('id')).order_by()


data=check.objects.annotate(month=TruncMonth('time')).values('month', 'shop').annotate(s=Sum('nal')).order_by('-month')

data=check.objects.annotate(week=ExtractWeek('time'), year=ExtractYear('time')).values('week', 'year', 'shop').annotate(s=Sum('nal')).order_by('-week')




data=check.objects.annotate(year=ExtractYear('time'), month=ExtractMonth('time'), week=ExtractWeek('time'), day=ExtractDay('time'), weekday=ExtractWeekDay('time')).values('year', 'month', 'week', 'day', 'shop').annotate(s=Sum('nal')).order_by()

data=checkitem.objects.annotate(year=ExtractYear('fcheck__time'), month=ExtractMonth('fcheck__time'), week=ExtractWeek('fcheck__time')).values('year', 'month', 'week', 'fcheck__shop').annotate(s=Sum('sum')).order_by('week', 'year')


for i in data:
    print i
	
	

