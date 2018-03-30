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

from .mobilon import *


app_name = 'call'
urlpatterns = [
	#http://crm.babah24.ru/mobilon/webhook/call/?callerid={CALLERID}&time={TIME}&innumber={INCOMING_NUMBER}
	url(r'^mobilon/webhook/call/?$', mobilon_webhook_call, name='mobilon_webhook_call'),
	url(r'^mobilon/webhook/callback/?$', mobilon_webhook_callback, name='mobilon_webhook_callback'),
	#
	url(r'^call/traceback/list/?$', login_required(call_traceback_list.as_view()), name='call_traceback_list'),
	url(r'^call/traceback/detail/(?P<pk>\d+)/?$', login_required(call_traceback_detail.as_view()), name='call_traceback_detail'),
	
	
	#url(r'^buyer/adv/(?P<control>off)/(?P<token>\w+)/?$', buyeradv),
	#url(r'^buyer/message/(?P<token>\w+)/?$', buyermessagemake),
	#
	#url(r'^bitrix/review/add/?$', review_create.as_view()),
	#url(r'^bitrix/review/list/?$', bitrixreviewlist),
	#url(r'^bitrix/review/list/?$', bitrixreviewlist.as_view()),
	#api
	#url(r'^bitrix/buyerisauth/(?P<authtoken>\w+)/?$', buyerauthtesttoken.as_view(), name='buyerauthtesttoken'),
]





