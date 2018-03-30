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
from useridea2.views import *


app_name = 'useridea2'
urlpatterns = [
	#ideasection
	url(r'^useridea2/ideasection/add/?$', login_required(ideasection_add.as_view()), name='ideasection_add'),
	url(r'^useridea2/ideasection/list/?$', login_required(ideasection_list.as_view()), name='ideasection_list'),
	url(r'^useridea2/ideasection/edit/(?P<pk>\d+)/?$', login_required(ideasection_edit.as_view()), name='ideasection_edit'),
	url(r'^useridea2/ideasection/del/(?P<pk>\d+)/?$', login_required(ideasection_del.as_view()), name='ideasection_del'),
	#useridea 
	url(r'^useridea2/idea/add/?$', login_required(useridea_add.as_view()), name='useridea_add'),
	url(r'^useridea2/idea/detail/(?P<pk>\d+)/?$', login_required(useridea_detail.as_view()), name='useridea_detail'),
	url(r'^useridea2/idea/edit/(?P<pk>\d+)/?$', login_required(useridea_edit.as_view()), name='useridea_edit'),
	url(r'^useridea2/idea/changestatus/(?P<pk>\d+)/?$', login_required(useridea_change_status.as_view()), name='useridea_change_status'),
	#picture's and file's operations
	url(r'^useridea2/idea/pict/add/(?P<pk>\d+)/?$', login_required(useridea_pict_add.as_view()), name='useridea_pict_add'),
	url(r'^useridea2/idea/file/add/(?P<pk>\d+)/?$', login_required(useridea_file_add.as_view()), name='useridea_file_add'),
	url(r'^useridea2/idea/pict/del/(?P<pk>\d+)/?$', login_required(useridea_pict_del.as_view()), name='useridea_pict_del'),
	url(r'^useridea2/idea/file/del/(?P<pk>\d+)/?$', login_required(useridea_file_del.as_view()), name='useridea_file_del'),
	#comments
	url(r'^useridea2/commentidea/edit/(?P<pk>\d+)/?$', login_required(commentidea_edit.as_view()), name='commentidea_edit'),
	url(r'^useridea2/commentidea/del/(?P<pk>\d+)/?$', login_required(commentidea_del.as_view()), name='commentidea_del'),
	url(r'^useridea2/commentidea/pict/add/(?P<pk>\d+)/?$', login_required(commentidea_pict_add.as_view()), name='commentidea_pict_add'),
	url(r'^useridea2/commentidea/file/add/(?P<pk>\d+)/?$', login_required(commentidea_file_add.as_view()), name='commentidea_file_add'),
	url(r'^useridea2/commentidea/pict/del/(?P<pk>\d+)/?$', login_required(commentidea_pict_del.as_view()), name='commentidea_pict_del'),
	url(r'^useridea2/commentidea/file/del/(?P<pk>\d+)/?$', login_required(commentidea_file_del.as_view()), name='commentidea_file_del'),
	#like
	url(r'^useridea2/idea/like/(?P<pk>\d+)/(?P<value>[1-5])/?$', login_required(likeidea_add), name='useridea_estimate'),
]





