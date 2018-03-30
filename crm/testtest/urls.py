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



app_name = 'testtest'
urlpatterns = [

	url(r'^testtest/testa/list/?$', testa_list.as_view()),
	url(r'^testtest/testa/(?P<pk>\d+)/?$', login_required(testa_detail.as_view()), name='testa_detail'),
	url(r'^testtest/testb/(?P<pk>\d+)/?$', login_required(testb_detail.as_view()), name='testb_detail'),

	#url(r'^api/test/get_post/?$', api_test_get_post),
]





