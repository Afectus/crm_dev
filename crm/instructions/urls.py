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
# from instructions.views import *


app_name = 'instructions'
urlpatterns = [
	url(r'^instructions/detail/(?P<pk>\d+)/?$', login_required(instructions_detail.as_view()), name='instructions_detail'),
	url(r'^instructions/detail/print/(?P<pk>\d+)/?$', login_required(instructions_detail_print.as_view()), name='instructions_detail_print'),
	url(r'^instructions/add/?$', login_required(instructions_add.as_view()), name='instructions_add'),
	url(r'^instructions/list/?$', login_required(instructions_list.as_view()), name='instructions_list'),
	url(r'^instructions/edit/(?P<pk>\d+)/?$', login_required(instructions_edit.as_view()), name='instructions_edit'),
	url(r'^instructions/del/(?P<pk>\d+)/?$', login_required(instructions_del.as_view()), name='instructions_del'),
	# url(r'^projectcomment/file/del/(?P<pk>\d+)/?$', login_required(projectcomment_file_del.as_view()), name='projectcomment_file_del'),
]
