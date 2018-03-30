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



app_name = 'marketing'
urlpatterns = [
	url(r'^marketing/report/list/?$', login_required(marketing_report_list.as_view())),
	
	url(r'^marketing/report/add/?$', login_required(marketing_report_add.as_view()), name='marketing_report_add'),
	
	url(r'^marketing/report/edit/(?P<pk>\d+)/?$', login_required(marketing_report_edit.as_view()), name='marketing_report_edit'),
	
	url(r'^marketing/report/detail/(?P<pk>\d+)/?$', login_required(marketing_report_detail.as_view()), name='marketing_report_detail'),
	
	url(r'^marketing/report/item/add/(?P<pk>\d+)/?$', login_required(marketing_report_item_add.as_view()), name='marketing_report_item_add'),
	
	url(r'^marketing/report/item/del/(?P<pk>\d+)/?$', login_required(marketing_report_item_del.as_view()), name='marketing_report_item_del'),
	
	url(r'^marketing/report/item/edit/(?P<pk>\d+)/?$', login_required(marketing_report_item_edit.as_view()), name='marketing_report_item_edit'),
	
]





