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



app_name = 'opt'
urlpatterns = [
	#optbuyer
	url(r'^opt/buyer/list/?$', login_required(optbuyer_list.as_view()), name='optbuyer_list'),
	url(r'^opt/buyer/add/?$', login_required(optbuyer_add.as_view()), name='optbuyer_add'),
	url(r'^opt/buyer/edit/(?P<pk>\d+)/?$', login_required(optbuyer_edit.as_view()), name='optbuyer_edit'),
	url(r'^opt/buyer/del/(?P<pk>\d+)/?$', login_required(optbuyer_del.as_view()), name='optbuyer_del'),
	#optprice_list
	url(r'^opt/price/list/?$', login_required(optprice_list.as_view()), name='optprice_list'),
	url(r'^opt/price/detail/(?P<pk>\d+)/?$', login_required(optprice_detail.as_view()), name='optprice_detail'),
	url(r'^opt/price/add/?$', login_required(optprice_add.as_view()), name='optprice_add'),
	url(r'^opt/price/edit/(?P<pk>\d+)/?$', login_required(optprice_edit.as_view()), name='optprice_edit'),
	url(r'^opt/price/del/(?P<pk>\d+)/?$', login_required(optprice_del.as_view()), name='optprice_del'),
	url(r'^opt/price/contract/(?P<pk>\d+)/?$', login_required(optprice_contract.as_view()), name='optprice_contract'),
	#
	url(r'^major/price/(?P<url>\w+)/?$', majorprice.as_view(), name='majorprice'),
	#
	url(r'^major/cart/add/?$', majorcartadd, name='majorcartadd'),
	url(r'^major/cart/(?P<url>\w+)/?$', majorcart.as_view(), name='majorcart'),
	url(r'^major/cartprint/(?P<url>\w+)/?$', majorcartprint.as_view(), name='majorcartprint'),
	url(r'^major/cart/del/(?P<url>\w+)/(?P<pk>\d+)/?$', majorcartdel, name='majorcartdel'),
	url(r'^major/cart/clear/(?P<url>\w+)/?$', majorcartclear, name='majorcartclear'),
	url(r'^major/order/(?P<url>\w+)/?$', majororder.as_view(), name='majororder'),
	url(r'^major/success/(?P<url>\w+)/?$', majorsuccess.as_view(), name='majorsuccess'),
	url(r'^major/contract/(?P<url>\w+)/?$', majorcontract.as_view(), name='majorcontract'),
]





