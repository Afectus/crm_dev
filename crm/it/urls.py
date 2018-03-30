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


app_name = 'it'
urlpatterns = [
	url(r'^usermanual/list/?$', login_required(usermanual_list.as_view()), name='usermanual_list'),
	url(r'^usermanual/detail/(?P<pk>\d+)/?$', login_required(usermanual_detail.as_view()), name='usermanual_detail'),
	#test tool
	url(r'^it/json/send/?$', login_required(it_json_send.as_view()), name='it_json_send'),
	
]





