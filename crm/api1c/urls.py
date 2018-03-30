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
from .api import *

app_name = 'api1c'
urlpatterns = [
	#url(r'^api1c/addc/?$', api1c_addc, name='api1c_addc'),#создает чек из 1с POST запросом http://crm.babah24.ru/api1c/addc/
	
	url(r'^api1c/get/cert/?$', api1c_getcert, name='api1c_getcert'),
	url(r'^api1c/get/cert/json/?$', api1c_getcert_json, name='api1c_getcert_json'),
	#
	url(r'^api/1c/check/add/?$', api_1c_check_add, name='api_1c_check_add'),
	#1c form in IE 5.0
	url(r'^form/1c/getcard/?$', form_1c_getcard.as_view(), name='form_1c_getcard'),
	url(r'^form/1c/makecard/?$', form_1c_makecard.as_view(), name='form_1c_makecard'),
	url(r'^form/1c/detailcard/(?P<pk>\d+)/?$', form_1c_detailcard.as_view(), name='form_1c_detailcard'),
	url(r'^form/1c/editcard/(?P<pk>\d+)/?$', form_1c_editcard.as_view(), name='form_1c_editcard'),
	url(r'^form/1c/relcard/(?P<pk>\d+)/?$', form_1c_relcard.as_view(), name='form_1c_relcard'),
	url(r'^form/1c/export/(?P<pk>\d+)/?$', form_1c_export.as_view(), name='form_1c_export'),
	url(r'^form/1c/relcard/edit/(?P<pk>\d+)/?$', form_1c_relcard_edit.as_view(), name='form_1c_relcard_edit'),
	#getcurtime
	url(r'^api/1c/getcurtime/?$', api_1c_getcurtime, name='api_1c_getcurtime'),
]





