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

app_name = 'organizer'
urlpatterns = [
	#
	url(r'^organizer/calendar/?$', login_required(organazier_calendar.as_view()), name='organazier_calendar'),
	
	#api
	url(r'^organizer/api/drop/?$', login_required(organizer_api_drop), name='organizer_api_drop'),
	url(r'^organizer/api/eventdrop/?$', login_required(organizer_api_eventdrop), name='organizer_api_eventdrop'),
	url(r'^organizer/api/eventresize/?$', login_required(organizer_api_eventresize), name='organizer_api_eventresize'),
	url(r'^organizer/api/eventdel/?$', login_required(organizer_api_eventdel), name='organizer_api_eventdel'),
	
	#
	url(r'^organizer/add/?$', login_required(organizer_add.as_view()), name='organizer_add'),
	url(r'^organizer/list/?$', login_required(organizer_list.as_view()), name='organizer_list'),
	url(r'^organizer/edit/(?P<pk>\d+)/?$', login_required(organizer_edit.as_view()), name='organizer_edit'),
	url(r'^organizer/del/(?P<pk>\d+)/?$', login_required(organizer_del.as_view()), name='organizer_del'),

]





