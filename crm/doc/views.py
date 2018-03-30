# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.shortcuts import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponsePermanentRedirect

from django.core.exceptions import PermissionDenied

from django import forms
from django.contrib.auth.models import User, Group

import json
from django.core import serializers

from django.http import QueryDict

from django.views.generic import DetailView, ListView, DeleteView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.base import TemplateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required


import datetime, time

from django.db.models import Sum, Count
from django.db.models import Q


@permission_required('node.add_buyer')
def getphone(request, pk):
	if request.method == 'GET':
		b=get_object_or_404(buyer, id=pk)
		res={'res': 1, 'phone': b.phone}
		return HttpResponse(json.dumps(res), content_type='application/json')

	res={'res': 0, 'data': u'Ошибка',}
	return HttpResponse(json.dumps(res), content_type='application/json')
		

	
	