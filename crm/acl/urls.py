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



app_name = 'acl'
urlpatterns = [
	url(r'^acl/perm/list/?$', login_required(acl_perm_list.as_view()), name='acl_perm_list'),
	#aclu
	url(r'^acl/aclu/edit/(?P<pk>\d+)/?$', login_required(acl_aclu_edit.as_view()), name='acl_aclu_edit'),
	url(r'^acl/aclu/add/(?P<pk>\d+)/?$', login_required(acl_aclu_add.as_view()), name='acl_aclu_add'),
	url(r'^acl/aclu/del/(?P<pk>\d+)/?$', login_required(acl_aclu_del.as_view()), name='acl_aclu_del'),
	#aclg
	url(r'^acl/aclg/edit/(?P<pk>\d+)/?$', login_required(acl_aclg_edit.as_view()), name='acl_aclg_edit'),
	url(r'^acl/aclg/add/(?P<pk>\d+)/?$', login_required(acl_aclg_add.as_view()), name='acl_aclg_add'),
	url(r'^acl/aclg/del/(?P<pk>\d+)/?$', login_required(acl_aclg_del.as_view()), name='acl_aclg_del'),
	
]





