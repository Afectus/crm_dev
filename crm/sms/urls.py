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

app_name = 'sms'
urlpatterns = [
	url(r'^api/sms/send/?$', apismssend, name='apismssend'),
	#url(r'^buyer/adv/(?P<control>on)/(?P<token>\w+)/?$', buyeradv),
	#url(r'^buyer/adv/(?P<control>off)/(?P<token>\w+)/?$', buyeradv),
	#url(r'^buyer/message/(?P<token>\w+)/?$', buyermessagemake),
	#
	#url(r'^bitrix/review/add/?$', review_create.as_view()),
	#url(r'^bitrix/review/list/?$', bitrixreviewlist),
	#url(r'^bitrix/review/list/?$', bitrixreviewlist.as_view()),
	#api
	#url(r'^bitrix/buyerisauth/(?P<authtoken>\w+)/?$', buyerauthtesttoken.as_view(), name='buyerauthtesttoken'),
]





