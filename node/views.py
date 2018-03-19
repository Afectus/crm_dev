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
from acl.models import *
from log.models import *
from acl.views import get_object_or_denied


import logging
log = logging.getLogger(__name__)



#@method_decorator(permission_required('node.add_check'), name='dispatch')
class check_detail(DetailView):
	model = check
	template_name = 'check_detail.html'
	
	def dispatch(self, request, *args, **kwargs):
		#self.data = get_object_or_404(self.model, id=self.kwargs['pk'])
		get_object_or_denied(self.request.user, 'check', 'R') #проверяем права
		return super(check_detail, self).dispatch(request, *args, **kwargs)
	
	# def get_object(self, queryset=None):
		# return self.data

	def get_context_data(self, **kwargs):
		context = super(check_detail, self).get_context_data(**kwargs)
		#context['servername'] = self.data.name
		return context
