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



app_name = 'kassir'
urlpatterns = [
	url(r'^kassir/menu/?$', login_required(kassir_menu.as_view()), name='kassir_menu'),
	#buyer_list
	url(r'^kassir/buyer/list/?$', RedirectView.as_view(url='/kassir/buyer/list/1/'), name='kassir_buyer_list_redirect'),
	url(r'^kassir/buyer/list/(?P<page>\d+)/?$', login_required(kassir_buyer_list.as_view()), name='kassir_buyer_list'),
	#url(r'^kassir/buyer/detail/(?P<pk>\d+)/?$', login_required(kassir_buyer_detail.as_view()), name='kassir_buyer_detail'),
	url(r'^kassir/buyer/edit/(?P<pk>\d+)/?$', login_required(kassir_buyer_edit.as_view()), name='kassir_buyer_edit'),
	#
	
	url(r'^kassir/visitorlog/list/?$', login_required(kassirvisitorlog_list.as_view()), name='kassirvisitorlog_list'),
	url(r'^kassir/visitorlog/add/?$', login_required(kassirvisitorlog_add.as_view()), name='kassirvisitorlog_add'),
]





