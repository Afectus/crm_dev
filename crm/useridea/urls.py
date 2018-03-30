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



app_name = 'useridea'
urlpatterns = [
	#useridea
	url(r'^useridea/add/?$', login_required(create_useridea.as_view())),
	url(r'^useridea/add/file/(?P<pk>\d+)/?$', login_required(create_fileidea.as_view())),
	url(r'^useridea/del/file/(?P<pk>\d+)/?$', login_required(remove_fileidea.as_view())),
	url(r'^useridea/list/?$', login_required(useridea_list.as_view())),
	url(r'^useridea/edit/(?P<pk>\d+)/?$', login_required(useridea_edit.as_view())),
	url(r'^useridea/detail/(?P<pk>\d+)/?$', login_required(useridea_detail.as_view())),
	url(r'^useridea/like/(?P<pk>\d+)/(?P<value>[1-5])/?$', login_required(add_likeidea)),
]





