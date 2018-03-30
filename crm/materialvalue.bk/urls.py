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
# from materialvalue.views import *


app_name = 'materialvalue'
urlpatterns = [
	url(r'^materialvalue/add/?$', login_required(materialvalue_add.as_view()), name='materialvalue_add'),
	url(r'^materialvalue/list/?$', login_required(materialvalue_list.as_view()), name='materialvalue_list'),
	url(r'^materialvalue/list/print/?$', login_required(materialvalue_list_print.as_view()), name='materialvalue_list_print'),
	url(r'^materialvalue/detail/(?P<pk>\d+)/?$', login_required(materialvalue_detail.as_view()), name='materialvalue_detail'),
	url(r'^materialvalue/detail/print/(?P<pk>\d+)/?$', login_required(materialvalue_detail_print.as_view()), name='materialvalue_detail_print'),
	url(r'^materialvalue/edit/(?P<pk>\d+)/?$', login_required(materialvalue_edit.as_view()), name='materialvalue_edit'),
	url(r'^materialvalue/del/(?P<pk>\d+)/?$', login_required(materialvalue_del.as_view()), name='materialvalue_del'), 
	### additional photo
	url(r'^materialvalue/addphoto/(?P<pk>\d+)/?$', login_required(materialvalue_addphoto.as_view()), name='materialvalue_addphoto'),
	url(r'^materialvalue/addmorephoto/(?P<pk>\d+)/?$', login_required(materialvalue_addmorephoto.as_view()), name='materialvalue_addmorephoto'),
	### movement
	# url(r'^materialvaluemove/add/(?P<pk>\d+)/?$', login_required(materialvaluemove_add.as_view()), name='materialvaluemove_add'),
	url(r'^materialvaluemove/toshop/(?P<pk>\d+)/?$', login_required(materialvaluemove_toshop.as_view()), name='materialvaluemove_toshop'),
	url(r'^materialvaluemove/tostock/(?P<pk>\d+)/?$', login_required(materialvaluemove_tostock.as_view()), name='materialvaluemove_tostock'),
	# url(r'^materialvaluemove/list/(?P<pk>\d+)/?$', login_required(materialvaluemove_list.as_view()), name='materialvaluemove_list'),
	# url(r'^materialvaluemove/edit/(?P<pk>\d+)/?$', login_required(materialvaluemove_edit.as_view()), name='materialvaluemove_edit'),
	# url(r'^materialvaluemove/del/(?P<pk>\d+)/?$', login_required(materialvaluemove_del.as_view()), name='materialvaluemove_del'), 
	# url(r'^materialvalue/addphoto/(?P<pk>\d+)/?$', login_required(materialvalue_addphoto.as_view()), name='materialvalue_addphoto'),
	#групповое перемещение
	url(r'^materialvalue/gmove/shop/?$', login_required(materialvalue_gmove_shop.as_view()), name='materialvalue_gmove_shop'),
	url(r'^materialvalue/gmove/stock/?$', login_required(materialvalue_gmove_stock.as_view()), name='materialvalue_gmove_stock'),
	#
	url(r'^materialvalue/gmove/list/?$', login_required(materialvalue_gmove_list.as_view()), name='materialvalue_gmove_list'),
	url(r'^materialvalue/gmove/detail/(?P<pk>\d+)/?$', login_required(materialvalue_gmove_detail.as_view()), name='materialvalue_gmove_detail'),
	url(r'^materialvalue/gmove/detail/print/(?P<pk>\d+)/?$', login_required(materialvalue_gmove_detail_print.as_view()), name='materialvalue_gmove_detail_print'),
	
]
