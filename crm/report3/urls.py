# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.urls import path, re_path
from .views import *





urlpatterns = [
	url(r'^report3/ostatkisklad/list/$', list_ostatkisklad.as_view(), name='list_ostatkisklad'),
	#url(r'^update/paginator(?P<pk>\d+)$', paginatornumm_update.as_view(), name='update_paginator'),
]





