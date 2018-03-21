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
# from corpmail.views import *


app_name = 'corpmail'
urlpatterns = [
    url(r'^corpmail/add/?$', login_required(corpmail_add.as_view()), name='corpmail_add'),
    url(r'^corpmail/detail/(?P<pk>\d+)/?$', login_required(corpmail_detail.as_view()), name='corpmail_detail'),
    url(r'^corpmail/detailsent/(?P<pk>\d+)/?$', login_required(corpmail_detailsent.as_view()), name='corpmail_detailsent'),
    # url(r'^corpmail/reply/(?P<pk>\d+)/?$', login_required(corpmail_reply.as_view()), name='corpmail_reply'),
	url(r'^corpmail/inbox/?$', login_required(corpmail_inbox.as_view()), name='corpmail_inbox'),
	url(r'^corpmail/sent/?$', login_required(corpmail_sent.as_view()), name='corpmail_sent'),
    # url(r'^corpmail/edit/(?P<pk>\d+)/?$', login_required(corpmail_edit.as_view()), name='corpmail_edit'),
    url(r'^corpmail/toarchive/(?P<pk>\d+)/?$', login_required(corpmail_toarchive.as_view()), name='corpmail_toarchive'),
	# url(r'^projectcomment/file/del/(?P<pk>\d+)/?$', login_required(projectcomment_file_del.as_view()), name='projectcomment_file_del'),
]
