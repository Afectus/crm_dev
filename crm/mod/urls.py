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


app_name = 'mod'
urlpatterns = [
	#module
	url(r'^mod/ballgen/?$', ballgen.as_view()),
	url(r'^mod/ballgetconf/(?P<name>\w+)/?$', ballgetconf),
	url(r'^mod/ballgenconf/?$', ballgenconf),
	#mod
	url(r'^go/?$', go),
	url(r'^do/?$', go),
	url(r'^qr/(\d+)/?$',qr), #back url qr code
	url(r'^templatemail/?$', templatemail.as_view(), name='modtemplatemail'),
]





