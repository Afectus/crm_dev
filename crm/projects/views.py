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
from panel.form import *
from .models import *


import logging
log = logging.getLogger(__name__)


	
@method_decorator(permission_required('projects.add_projects'), name='dispatch')
class projects_list(ListView):
	template_name = 'projects_list.html'
	model = projects
	paginate_by = 20
	
@method_decorator(permission_required('projects.add_projects'), name='dispatch')
class projects_add(CreateView):
	model = projects
	template_name = 'projects_add.html'
	success_url = '/projects/list'
	fields = ['status', 'sdate', 'edate', 'executor', 'name', 'message',]

@method_decorator(permission_required('projects.add_projects'), name='dispatch')
class projects_edit(UpdateView):
	model = projects
	template_name = 'projects_edit.html'
	success_url = '/projects/list'
	fields = ['status', 'sdate', 'edate', 'executor', 'name', 'message',]
	
	def dispatch(self, request, *args, **kwargs):
		get_object_or_404(self.model, id=self.kwargs['pk'])
		return super(projects_edit, self).dispatch(request, *args, **kwargs)


	
	
	
	
	
	
	
	
	
	
