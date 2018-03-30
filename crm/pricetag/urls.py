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


app_name = 'pricetag'
urlpatterns = [
	#admin
	url(r'^pricetag/pricequeue/print/list/?$', login_required(pricequeue_print_list.as_view()), name='pricequeue_print_list'),
	url(r'^pricetag/pricequeue/print/edit/(?P<pk>\d+)/?$', login_required(pricequeue_print_edit.as_view()), name='pricequeue_print_edit'),
	url(r'^pricetag/pricequeue/print/del/(?P<pk>\d+)/?$', login_required(pricequeue_print_del.as_view()), name='pricequeue_print_del'),
	#
	url(r'^pricetag/pricequeue/list/?$', login_required(pricequeue_list.as_view()), name='pricequeue_list'),
	url(r'^pricetag/pricequeue/del/(?P<pk>\d+)/?$', login_required(pricequeue_del.as_view()), name='pricequeue_del'),
	url(r'^pricetag/pricequeue/add/(?P<pk>\d+)/?$', login_required(pricequeue_add), name='pricequeue_add'),
	url(r'^pricetag/pricequeue/clear/?$', login_required(pricequeue_clear), name='pricequeue_clear'),
	url(r'^pricetag/pricequeue/price2image/add/(?P<pk>\d+)/?$', pricequeue_price2image_add, name='pricequeue_price2image_add'),
]





