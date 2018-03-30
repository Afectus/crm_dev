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
# from normact.views import *


app_name = 'normact'
urlpatterns = [
    url(r'^normact/add/?$', login_required(normact_add.as_view()), name='normact_add'),
    url(r'^normact/list/?$', login_required(normact_list.as_view()), name='normact_list'),
    url(r'^normact/list/(?P<pk>\w+)/?$', login_required(normact_list.as_view()), name='normact_list'),
    url(r'^normact/edit/(?P<pk>\d+)/?$', login_required(normact_edit.as_view()), name='normact_edit'),
    url(r'^normact/del/(?P<pk>\d+)/?$', login_required(normact_del.as_view()), name='normact_del'), 
]
