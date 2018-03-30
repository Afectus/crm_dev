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



app_name = 'inventory'
urlpatterns = [
	#
	url(r'^inv/list/all/?$', login_required(invlist_list.as_view()), name='invlist_list'),
	url(r'^inv/list/add/?$', login_required(invlist_add.as_view()), name='invlist_add'),
	url(r'^inv/list/edit/(?P<pk>\d+)?$', login_required(invlist_edit.as_view()), name='invlist_edit'),
	#
	url(r'^inv/list/(?P<pk>\d+)/?$', login_required(invitem_process.as_view()), name='invitem_process'),
	url(r'^inv/item/add/(?P<pk>\d+)/(?P<barcode>\d+)/(?P<col>\d+)/?$', login_required(invitem_add), name='invitem_add'),
	url(r'^inv/item/del/(?P<pk>\d+)/?$', login_required(invitem_del.as_view()), name='invitem_del'),
	url(r'^inv/item/edit/(?P<pk>\d+)/?$', login_required(invitem_edit.as_view()), name='invitem_edit'),
	#url(r'^inv/item/edit/(?P<pk>\d+)/?$', login_required(invitem_edit.as_view()), name='invitem_list'),
	url(r'^inv/item/csv/(?P<pk>\d+)/?$', login_required(invitem_csv), name='invitem_csv'),
]





