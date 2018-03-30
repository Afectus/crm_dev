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


data=device.objects.filter(status=True)

for i in data:
	#i.os_system='ls'
	
	#i.os_system='apt-get install -y openvpn wget'
	#i.os_system='wget http://babah.ru/vpn/client.conf -O /etc/openvpn/client.conf'
	#i.os_system='wget http://babah.ru/vpn/%s.crt -O /etc/openvpn/client.crt' % (i.mac)
	#i.os_system='wget http://babah.ru/vpn/%s.key -O /etc/openvpn/client.key' % (i.mac)
	#i.os_system='wget http://babah.ru/vpn/ca.crt -O /etc/openvpn/ca.crt'
	#i.os_system='systemctl enable openvpn@client'
	#i.os_system='systemctl start openvpn@client'
	i.os_system='shutdown -r now'
	i.save()
	
	
	
	
