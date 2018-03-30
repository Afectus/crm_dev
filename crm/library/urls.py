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



app_name = 'library'
urlpatterns = [
	url(r'^library/book/add/?$', login_required(library_book_add.as_view()), name='library_book_add'),
	url(r'^library/book/list/?$', login_required(library_book_list.as_view()), name='library_book_list'),
	url(r'^library/book/edit/(?P<pk>\d+)/?$', login_required(library_book_edit.as_view()), name='library_book_edit'),
	url(r'^library/book/detail/(?P<pk>\d+)/?$', login_required(library_book_detail.as_view()), name='library_book_detail'),
	url(r'^library/book/like/(?P<pk>\d+)/(?P<value>[1-5])/?$', login_required(library_book_like), name='library_book_like'),
	url(r'^library/download/(?P<pk>\d+)/?$', login_required(download_book), name='download_book'),
	url(r'^library/download/list/?$', login_required(library_download_list.as_view()), name='library_download_list'),
]





