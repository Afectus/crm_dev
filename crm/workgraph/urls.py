# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import auth
from django.shortcuts import HttpResponseRedirect
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from django.views.generic.base import TemplateView
from django.views.generic import RedirectView

from django.shortcuts import render_to_response, render

from .views import *


app_name = 'workgraph'
urlpatterns = [
	url(r'^workgraph/list/?$', login_required(workgraph_list.as_view()), name='list'),
	url(r'^workgraph/add/?$', login_required(workgraph_add.as_view()), name='add'),
	url(r'^workgraph/edit/(?P<pk>\d+)/?$', login_required(workgraph_edit.as_view()), name='edit'),
]





