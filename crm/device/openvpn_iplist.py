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

from device.models import *


#/etc/openvpn/ccd

#валидный список ip для сетей windows
iplist = [
#[  1,  2], [  5,  6], [  9, 10], #сервисные 
[ 13, 14], [ 17, 18],
[ 21, 22], [ 25, 26], [ 29, 30], [ 33, 34], [ 37, 38],
[ 41, 42], [ 45, 46], [ 49, 50], [ 53, 54], [ 57, 58],
[ 61, 62], [ 65, 66], [ 69, 70], [ 73, 74], [ 77, 78],
[ 81, 82], [ 85, 86], [ 89, 90], [ 93, 94], [ 97, 98],
#[101,102], #мой
[105,106], [109,110], [113,114], [117,118],
[121,122], [125,126], [129,130], [133,134], [137,138],
[141,142], [145,146], [149,150], [153,154], [157,158],
[161,162], [165,166], [169,170], [173,174], [177,178],
[181,182], [185,186], [189,190], [193,194], [197,198],
[201,202], [205,206], [209,210], [213,214], [217,218],
[221,222], [225,226], [229,230], [233,234], [237,238],
[241,242], [245,246], [249,250], [253,254],
]


#print iplist

#for i in iplist:
#	print i[0], i[1]
	

data=device.objects.filter(status=True)

for i in data:
	vpnip=iplist.pop(0)
	print i.mac, vpnip[0], vpnip[1]
	i.vpnip='10.8.0.%s' % (vpnip[0])
	i.save()
	os.system('touch /etc/openvpn/ccd/%s' % (i.mac))
	os.system('echo "ifconfig-push 10.8.0.%s 10.8.0.%s" > /etc/openvpn/ccd/%s' % (vpnip[0], vpnip[1], i.mac))
	
	
