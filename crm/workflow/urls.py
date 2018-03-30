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


app_name = 'workflow'
urlpatterns = [
	url(r'^printtask/list/?$', login_required(printtask_list.as_view()), name='printtask_list'),
	url(r'^printtask/edit/(?P<pk>\d+)/?$', login_required(printtask_edit.as_view()), name='printtask_edit'),
	url(r'^printtask/detail/(?P<pk>\d+)/?$', login_required(printtask_detail.as_view()), name='printtask_detail'),
	url(r'^printtask/del/(?P<pk>\d+)/?$', login_required(printtask_del.as_view()), name='printtask_del'),
	url(r'^printtask/add/(?P<pk>\d+)/(?P<copies>\d+)/(?P<barcode>\d+)/?$', login_required(printtask_add), name='printtask_add'),
	url(r'^printtask/clear/?$', login_required(printtask_clear)),
	url(r'^price2image/add/(?P<pk>\d+)/?$', price2image_add),
	url(r'^printtask/copies/(?P<copies>\d+)/?$', login_required(printtask_copies)),
	url(r'^printtask/stock/(?P<id>\d+)/?$', login_required(printtask_stock)),
	#
	url(r'^printtask/printbarcodetext/?$', login_required(printbarcodetext.as_view())),
	url(r'^printtask/printtext/?$', login_required(printtext.as_view())),
	#поставщики
	url(r'^distributor/list/?$', login_required(distributor_list.as_view())),
	url(r'^distributor/list/(?P<pk>\d+)/?$', login_required(distributor_list.as_view())),
	url(r'^distributor/add/?$', login_required(distributor_add.as_view()), name='distributor_add'),
	url(r'^distributor/edit/(?P<pk>\d+)/?$', login_required(distributor_edit.as_view())),
	url(r'^distributormenu/edit/(?P<pk>\d+)/?$', login_required(distributormenu_edit.as_view()), name='distributormenu_edit'),
]





