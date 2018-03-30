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


app_name = 'screen2'
urlpatterns = [
	url(r'^screen2/?$', screenhome2.as_view(), name='screenhome2'),
	url(r'^screen2/list/?$', screenlist2.as_view(), name='screenlist2'),
	url(r'^screen2/list/(?P<pk>\d+)/?$', screenlist2.as_view(), name='screenlist2'),
	url(r'^screen2/list/(?P<pk>\d+)/sort\.(?P<sort>name)/?$', screenlist2.as_view(), name='screenlist2'),
	url(r'^screen2/list/(?P<pk>\d+)/sort\.(?P<sort>price)/?$', screenlist2.as_view(), name='screenlist2'),
	url(r'^screen2/list/(?P<pk>\d+)/sort\.(?P<sort>a)/?$', screenlist2.as_view(), name='screenlist2'),#количестов зарядов
	url(r'^screen2/list/(?P<pk>\d+)/sort\.(?P<sort>b)/?$', screenlist2.as_view(), name='screenlist2'),#продолжительность
	#
	url(r'^screen2/ajax/showvideocount/(?P<pk>\d+)/?$', screenshowvideocount2),
]





