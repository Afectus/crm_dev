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

app_name = 'project'
urlpatterns = [
	url(r'^project/add/?$', login_required(project_add.as_view()), name='project_add'),
	url(r'^project/list/?$', login_required(project_list.as_view()), name='project_list'),
	url(r'^project/edit/(?P<pk>\d+)/?$', login_required(project_edit.as_view()), name='project_edit'),
	url(r'^project/detail/(?P<pk>\d+)/?$', login_required(project_detail.as_view()), name='project_detail'),
	url(r'^project/pict/add/(?P<pk>\d+)/?$', login_required(project_pict_add.as_view()), name='project_pict_add'),
	url(r'^project/file/add/(?P<pk>\d+)/?$', login_required(project_file_add.as_view()), name='project_file_add'),
	url(r'^project/pict/del/(?P<pk>\d+)/?$', login_required(project_pict_del.as_view()), name='project_pict_del'),
	url(r'^project/file/del/(?P<pk>\d+)/?$', login_required(project_file_del.as_view()), name='project_file_del'),
	#
	url(r'^projectstep/add/(?P<pk>\d+)/?$', login_required(projectstep_add.as_view()), name='projectstep_add'),
	url(r'^projectstep/edit/(?P<pk>\d+)/?$', login_required(projectstep_edit.as_view()), name='projectstep_edit'),
	url(r'^projectstep/detail/(?P<pk>\d+)/?$', login_required(projectstep_detail.as_view()), name='projectstep_detail'),
	url(r'^projectstep/success/(?P<pk>\d+)/?$', login_required(projectstep_success.as_view()), name='projectstep_success'),
	url(r'^projectstep/pict/add/(?P<pk>\d+)/?$', login_required(projectstep_pict_add.as_view()), name='projectstep_pict_add'),
	url(r'^projectstep/file/add/(?P<pk>\d+)/?$', login_required(projectstep_file_add.as_view()), name='projectstep_file_add'),
	url(r'^projectstep/pict/del/(?P<pk>\d+)/?$', login_required(projectstep_pict_del.as_view()), name='projectstep_pict_del'),
	url(r'^projectstep/file/del/(?P<pk>\d+)/?$', login_required(projectstep_file_del.as_view()), name='projectstep_file_del'),
	url(r'^projectstepcomment/edit/(?P<pk>\d+)/?$', login_required(projectstepcomment_edit.as_view()), name='projectstepcomment_edit'),
	url(r'^projectstepcomment/del/(?P<pk>\d+)/?$', login_required(projectstepcomment_del.as_view()), name='projectstepcomment_del'),
	url(r'^projectstepcomment/pict/add/(?P<pk>\d+)/?$', login_required(projectstepcomment_pict_add.as_view()), name='projectstepcomment_pict_add'),
	url(r'^projectstepcomment/file/add/(?P<pk>\d+)/?$', login_required(projectstepcomment_file_add.as_view()), name='projectstepcomment_file_add'),
	url(r'^projectstepcomment/pict/del/(?P<pk>\d+)/?$', login_required(projectstepcomment_pict_del.as_view()), name='projectstepcomment_pict_del'),
	url(r'^projectstepcomment/file/del/(?P<pk>\d+)/?$', login_required(projectstepcomment_file_del.as_view()), name='projectstepcomment_file_del'),
	#
	# url(r'^projectcomment/add/(?P<pk>\d+)/?$', login_required(projectcomment_add.as_view()), name='projectcomment_add'),
	url(r'^projectcomment/edit/(?P<pk>\d+)/?$', login_required(projectcomment_edit.as_view()), name='projectcomment_edit'),
	url(r'^projectcomment/del/(?P<pk>\d+)/?$', login_required(projectcomment_del.as_view()), name='projectcomment_del'),
	url(r'^projectcomment/pict/add/(?P<pk>\d+)/?$', login_required(projectcomment_pict_add.as_view()), name='projectcomment_pict_add'),
	url(r'^projectcomment/file/add/(?P<pk>\d+)/?$', login_required(projectcomment_file_add.as_view()), name='projectcomment_file_add'),
	url(r'^projectcomment/pict/del/(?P<pk>\d+)/?$', login_required(projectcomment_pict_del.as_view()), name='projectcomment_pict_del'),
	url(r'^projectcomment/file/del/(?P<pk>\d+)/?$', login_required(projectcomment_file_del.as_view()), name='projectcomment_file_del'),
]
