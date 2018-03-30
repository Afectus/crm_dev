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


app_name = 'screen'
urlpatterns = [
	url(r'^screen/?$', screenhome.as_view()),
	url(r'^screen/list/(?P<pk>\d+)/?$', screenlist.as_view()),
	url(r'^screen/list/(?P<pk>\d+)/sort\.(?P<sort>name)/?$', screenlist.as_view()),
	url(r'^screen/list/(?P<pk>\d+)/sort\.(?P<sort>price)/?$', screenlist.as_view()),
	url(r'^screen/list/(?P<pk>\d+)/sort\.(?P<sort>a)/?$', screenlist.as_view()),#количестов зарядов
	url(r'^screen/list/(?P<pk>\d+)/sort\.(?P<sort>b)/?$', screenlist.as_view()),#продолжительность
	#поиск
	url(r'^screen/listsearch/?$', screenlistsearch.as_view()),
	#
	url(r'^screen/ajax/showvideocount/(?P<pk>\d+)/?$', screenshowvideocount),
]





