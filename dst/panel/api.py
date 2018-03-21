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
from panel.form import *
from panel.models import *
from log.models import *
from acl.views import get_object_or_denied


import logging
log = logging.getLogger(__name__)



@csrf_exempt
def api_goods_video_edit(request):
	tmp={'res': 0, 'data': u'error',}
	if request.method == 'POST':
		tmp={'res': 0, 'data': u'request method is POST',}
	if 'crc' in request.GET and 'id' in request.GET:
		crc = makeapitoken(request.GET['id'])
		log.info(crc.lower(), request.GET['crc'].lower())
		if crc.lower() == request.GET['crc'].lower():
			data=json.loads(request.body)
			for i in data:
				try:
					g=goods.objects.get(id=i['id'])
				except:
					pass
				else:
					g.videomp4=i['name']
					g.save()
			tmp={'res': 1, 'data': u'api_goods_video_edit OK',}
		else:
			tmp={'res': 0, 'data': u'crc error',}
	return HttpResponse(json.dumps(tmp), content_type='application/json')


