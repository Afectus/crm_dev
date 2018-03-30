# -*- coding: utf-8 -*-
from __future__ import unicode_literals
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

from django.urls import reverse

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


from django.db.models import Max, Sum, Count
from django.db.models import Q, F

from ckeditor.widgets import CKEditorWidget

from dj.views import *


from django.core.mail import send_mail


from node.templatetags.nodetag import *

from node.models import *
from .form import *
from .models import *


import logging
log = logging.getLogger(__name__)

	
def userlogin(request):
	if request.method == 'GET':
		user = request.user
		if not user.is_authenticated:
			next = request.GET.get('next', '/')
			form_login = Form_login(initial={'next': next})
			return render(request, "login.html", {'form_login': form_login,})
		else:
			return HttpResponseRedirect("/")
	if request.method == 'POST':
		#проверка на блокировку пользователя
		errors=False
		blockmsg=False
		timeblock=datetime.datetime.now() - datetime.timedelta(seconds=60)
		ublock=userloginblockdb.objects.filter(ip=request.META['REMOTE_ADDR'], starttime__gt=timeblock)
		if ublock.exists() and ublock.count() > 3:
			blockmsg=True
			errors=u'Вы слишком часто пытаетесь войти, подождите минуту и попробуйте снова.'
		###########
		form_login = Form_login(request.POST)
		if form_login.is_valid() and blockmsg==False:
			cd = form_login.cleaned_data
			user = auth.authenticate(username=cd['username'].lower(), password=cd['password'])
			if user is not None:
				if user.is_active:
					auth.login(request, user)
					return HttpResponseRedirect(cd['next'])
				if not user.is_active:
					errors=u'Пользователь не подтвержден'
			else:
				ublock=userloginblockdb(user='%s::%s' % (cd['username'], cd['password']), ip=request.META['REMOTE_ADDR'], blocktime=3) #если неправильный логин пароль то добавляем блокировку
				ublock.save()
				errors=u'Проверьте правильность введенных данных'

		return render(request, "login.html", {'form_login': form_login, 'errors': errors, })
		
		

