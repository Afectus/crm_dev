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
from .api import *
from .api2 import *
from .ordercartlist import *


app_name = 'order'
urlpatterns = [
	url(r'^api/order/add/?$', api_order_add),
	url(r'^api/order/update/?$', api_order_update),
	url(r'^api/order/callback/?$', api_order_callback),
	url(r'^api/order/test/?$', login_required(api_order_test)),
	#
	url(r'^api2/order/update_json/?$', api_order_update_json),
	#
	#
	url(r'^order/add/?$', login_required(order_add.as_view()), name='add'),
	url(r'^order/list/?$', login_required(order_list.as_view()), name='list'),
	url(r'^order/arch/list/?$', login_required(order_arch_list.as_view()), name='arch_list'),
	url(r'^order/detail/(?P<pk>\d+)/?$', login_required(order_detail.as_view()), name='detail'),
	url(r'^order/detail/print/(?P<pk>\d+)/?$', login_required(order_detail_print.as_view()), name='order_detail_print'),
	url(r'^order/event/detail/(?P<pk>\d+)/?$', login_required(order_event_detail.as_view()), name='order_event_detail'),
	url(r'^order/edit/(?P<pk>\d+)/?$', login_required(order_edit.as_view()), name='edit'),
	url(r'^order/status/edit/(?P<pk>\d+)/?$', login_required(order_status_edit.as_view()), name='status_edit'),
	url(r'^order/accept/(?P<pk>\d+)/?$', login_required(order_accept), name='accept'),
	url(r'^order/success/(?P<pk>\d+)/?$', login_required(order_success), name='success'),
	url(r'^order/inway/xls/?$', login_required(order_inway_xls.as_view()), name='inway_xls'),
	#ordercartlist
	url(r'^order/ordercartlist/edit/(?P<pk>\d+)/?$', login_required(ordercartlist_edit.as_view()), name='ordercartlist_edit'),
	url(r'^order/ordercartlist/add/(?P<pk>\d+)/?$', login_required(ordercartlist_add.as_view()), name='ordercartlist_add'),
	url(r'^order/ordercartlist/del/(?P<pk>\d+)/?$', login_required(ordercartlist_del.as_view()), name='ordercartlist_del'),
	
	
]





