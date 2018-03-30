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
# from pictgallery.views import *


app_name = 'pictgallery'
urlpatterns = [
    url(r'^pictgallery/add/?$', login_required(pictgallery_add.as_view()), name='pictgallery_add'),
    url(r'^pictgallery/list/?$', login_required(pictgallery_list.as_view()), name='pictgallery_list'),
    url(r'^pictgallery/edit/(?P<pk>\d+)/?$', login_required(pictgallery_edit.as_view()), name='pictgallery_edit'),
    url(r'^pictgallery/del/(?P<pk>\d+)/?$', login_required(pictgallery_del.as_view()), name='pictgallery_del'),
	# url(r'^projectcomment/file/del/(?P<pk>\d+)/?$', login_required(projectcomment_file_del.as_view()), name='projectcomment_file_del'),
]
