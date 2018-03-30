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


app_name = 'device'
urlpatterns = [
	url(r'^dev/?$', devhome.as_view()),
	url(r'^dev/list/(?P<pk>\d+)/?$', devlist.as_view()),
	url(r'^dev/list/(?P<pk>\d+)/sort\.(?P<sort>name)/?$', devlist.as_view()),
	url(r'^dev/list/(?P<pk>\d+)/sort\.(?P<sort>price)/?$', devlist.as_view()),
	url(r'^dev/list/(?P<pk>\d+)/sort\.(?P<sort>a)/?$', devlist.as_view()),#количестов зарядов
	url(r'^dev/list/(?P<pk>\d+)/sort\.(?P<sort>b)/?$', devlist.as_view()),#продолжительность
	#поиск
	url(r'^dev/listsearch/?$', devlistsearch.as_view()),
	#
	url(r'^dev/test/?$', devtest.as_view()),
	#
	url(r'^dev/p/(?P<pk>\d+)/?$', devp.as_view()),
	url(r'^dev/novideo/?$', devnovideo.as_view()),
	url(r'^dev/control/list/?$', login_required(devcontrollist.as_view())),
	url(r'^dev/control/reboot/(?P<pk>\d+)/?$', login_required(devreboot)),
	#device api json
	url(r'^dev/get/(?P<mac>\w+)/?$', devget),
	url(r'^dev/setip/(?P<mac>\w+)/?$', devsetip),
	url(r'^dev/null/(?P<mac>\w+)/?$', devnull),
	url(r'^dev/ping/(?P<mac>\w+)/?$', devping),
	url(r'^dev/ossystem/(?P<mac>\w+)/?$', dev_os_system),
	url(r'^dev/demolist/?$', devdemolist),
	url(r'^dev/medialist/?$', devmedialist),
	url(r'^dev/countdebug/?$', login_required(devcountdebug.as_view())),
	url(r'^dev/setcountvisitor/(?P<mac>\w+)/?$', devsetcountvisitor),
	url(r'^dev/sendvideo/(?P<mac>\w+)/?$', devsendvideo),
	url(r'^dev/ajax/showvideocount/(?P<pk>\d+)/?$', devshowvideocount),
	#dev kondor
	url(r'^dev/kondor/(?P<salt>\w+)/(?P<crc>\w+)/?$', devkondor),
	##############################
]





