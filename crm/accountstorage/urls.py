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

app_name = 'accountstorage'
urlpatterns = [
	url(r'^accountstorage/add/?$', login_required(accountstorage_add.as_view()), name='accountstorage_add'),
	url(r'^accountstorage/list/?$', login_required(accountstorage_list.as_view()), name='accountstorage_list'),
	url(r'^accountstorage/edit/(?P<pk>\d+)/?$', login_required(accountstorage_edit.as_view()), name='accountstorage_edit'),
	url(r'^accountstorage/detail/(?P<pk>\d+)/?$', login_required(accountstorage_detail.as_view()), name='accountstorage_detail'),
]
