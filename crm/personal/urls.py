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


app_name = 'personal'
urlpatterns = [
	#
	url(r'^personal/list/?$', login_required(personal_list.as_view()), name='personal_list'),
	url(r'^personal/detail/(?P<pk>\d+)/?$', login_required(personal_detail.as_view()), name='personal_detail'),
	#
	#personal data
	url(r'^personaldata/edit/(?P<pk>\d+)/?$', login_required(personaldata_edit.as_view()), name='personaldata_edit'),
	#personal
	url(r'^personal/edit/(?P<pk>\d+)/?$', login_required(personal_edit.as_view())),
	
	url(r'^personal/add/child/(?P<pk>\d+)/?$', login_required(personal_add_child.as_view())),
	url(r'^personal/remove/child/(?P<pk>\d+)/?$', login_required(personal_remove_child.as_view())),
	url(r'^personal/edit/child/(?P<pk>\d+)/?$', login_required(personal_edit_child.as_view())),
	url(r'^personal/signature/(?P<pk>\d+)/?$', login_required(personal_signature.as_view())),
	url(r'^personal/add/feat/(?P<pk>\d+)/?$', login_required(personal_add_feat.as_view())),
	url(r'^personal/remove/feat/(?P<pk>\d+)/?$', login_required(personal_remove_feat.as_view())),
	url(r'^personal/edit/feat/(?P<pk>\d+)/?$', login_required(personal_edit_feat.as_view())),
	url(r'^personal/detail/feat/(?P<pk>\d+)/?$', login_required(personal_detail_feat.as_view()), name='detail_feat'),
	url(r'^personal/add/feat/image/(?P<pk>\d+)/?$', login_required(personal_add_feat_image.as_view()), name='personal_add_feat_image'),
	
	
	#personalanketa
	url(r'^personalanketa/list/?$', login_required(personalanketa_list.as_view()), name='personalanketa_list'),
	url(r'^personalanketa/add/?$', login_required(personalanketa_add.as_view()), name='personalanketa_add'),
	url(r'^personalanketa/add/(?P<pk>\d+)/?$', login_required(personalanketa_add.as_view()), name='personalanketa_add'),
	url(r'^personalanketa/edit/(?P<pk>\d+)/?$', login_required(personalanketa_edit.as_view()), name='personalanketa_edit'),
	url(r'^personalanketa/detail/(?P<pk>\d+)/?$', login_required(personalanketa_detail.as_view()), name='personalanketa_detail'),
	
]





