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
from it.models import *


import logging
log = logging.getLogger(__name__)


@method_decorator(permission_required('it.add_usermanual'), name='dispatch')
class usermanual_list(ListView):
	template_name = "usermanual_list.html"
	model = usermanual
	#paginate_by = 10
	
	def dispatch(self, request, *args, **kwargs):
		return super(usermanual_list, self).dispatch(request, *args, **kwargs)
		
@method_decorator(permission_required('it.add_usermanual'), name='dispatch')
class usermanual_detail(DetailView):
	model = usermanual
	template_name = 'usermanual_detail.html'
	
	
jsonbody="""{
	"salt": 370868,
	"crc": "c35c91ac207f1eb240d0e9371e97b85a",
	"res": true,
	"id1c": "ДМИПК006364",
	"list": []
}"""	
	
class Form_it_json_send(forms.Form):
	url = forms.CharField(label='Url', help_text='Адрес', widget=forms.TextInput(attrs={'class': 'form-control','autocomplete': 'on'}), max_length=500, required=True,)
	jsonbody = forms.CharField(widget=forms.Textarea(attrs={'cols': '40', 'rows': '10',}), label='JSON', max_length=10000, required=True)	
	
#method_decorator(permission_required('sms.add_smsreport'), name='dispatch')
class it_json_send(FormView):
	template_name = 'it_json_send.html'
	success_url = '/it/json/send/?send=true'
	form_class = Form_it_json_send

	def dispatch(self, request, *args, **kwargs):
		return super(it_json_send, self).dispatch(request, *args, **kwargs)

	#def get_success_url(self):
	#	return '/it_json_send/?send=true'
	
	def get_initial(self):
		return {
			'url': 'http://crm.babah24.ru/api/1c/check/add/?salt=&crc=92C2931D23D23148D051F21134E73807',
			'jsonbody': jsonbody,
			}

	def get_context_data(self, **kwargs):
		context = super(it_json_send, self).get_context_data(**kwargs)
		#context['nickname'] = self.data.name
		return context
		
	def form_valid(self, form):
		#cd = form.cleaned_data
		return super(it_json_send, self).form_valid(form)	
	
	
	
