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
from .models import *

import logging
log = logging.getLogger(__name__)



class bizplist_detail(ListView): 
	template_name = 'bizpstep_diagram.html' 
	model = bizpstep

	def dispatch(self, request, *args, **kwargs):
		#get_object_or_denied(self.request.user, 'materialvalue', 'R')
		self.data = get_object_or_404(bizplist, id=self.kwargs['pk'])
		return super(bizplist_detail, self).dispatch(request, *args, **kwargs)
	
	def get_queryset(self):
		data=super(bizplist_detail, self).get_queryset().order_by('sort')
		data=data.filter(process=self.data).exclude(parent__isnull=False)
		return data

	def get_context_data(self, *args, **kwargs):
		context_data = super(bizplist_detail, self).get_context_data(*args, **kwargs)
		context_data.update({'object': self.data,})
		return context_data
		
class bizpstep_detail(ListView): 
	template_name = 'bizpstep_diagram.html' 
	model = bizpstep

	def dispatch(self, request, *args, **kwargs):
		#get_object_or_denied(self.request.user, 'materialvalue', 'R')
		self.data = get_object_or_404(bizpstep, id=self.kwargs['pk'])
		return super(bizpstep_detail, self).dispatch(request, *args, **kwargs)
	
	def get_queryset(self):
		  data=super(bizpstep_detail, self).get_queryset().order_by('sort')
		  data=data.filter(parent=self.data)
		  return data

	def get_context_data(self, *args, **kwargs):
		context_data = super(bizpstep_detail, self).get_context_data(*args, **kwargs)
		context_data.update({'object': self.data,})
		
		#поиск следующего шага
		if self.data.parent is True:
			nextstep=bizpstep.objects.filter(parent=self.data, sort__gt=self.data.sort).order_by('sort').first()
		else:
			nextstep=bizpstep.objects.filter(parent__isnull=True, process=self.data.process, sort__gt=self.data.sort).order_by('sort').first()
		context_data.update({'nextstep': nextstep,})
			
		#
		
		return context_data

