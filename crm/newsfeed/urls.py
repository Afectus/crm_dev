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



app_name = 'newsfeed'
urlpatterns = [
	#news
	url(r'^newsfeed/news/add/?$', login_required(news_add.as_view()), name='news_add'),
	url(r'^newsfeed/news/list/?$', login_required(news_list.as_view()), name='news_list'),
	url(r'^newsfeed/news/edit/(?P<pk>\d+)/?$', login_required(news_edit.as_view()), name='news_edit'),
	url(r'^newsfeed/news/detail/(?P<pk>\d+)/?$', login_required(news_detail.as_view()), name='news_detail'),
	url(r'^newsfeed/news/del/(?P<pk>\d+)/?$', login_required(news_del.as_view()), name='news_del'),
	#picture's and file's operations
	url(r'^newsfeed/news/pict/add/(?P<pk>\d+)/?$', login_required(news_pict_add.as_view()), name='news_pict_add'),
	url(r'^newsfeed/news/pict/del/(?P<pk>\d+)/?$', login_required(news_pict_del.as_view()), name='news_pict_del'),
	#comments
]





