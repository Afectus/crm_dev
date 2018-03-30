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


app_name = 'log'
urlpatterns = [
	url(r'^log/list/?$', login_required(log_list.as_view()), name='log_list'),
	#url(r'^report/sale/?$', login_required(report_sale.as_view())),
	url(r'^log/kassir/?$', RedirectView.as_view(url='/log/kassir/1/')),
	url(r'^log/kassir/(?P<page>\d+)/?$', login_required(log_kassir.as_view()), name='log_kassir'),
]





