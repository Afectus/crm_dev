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
# from instructions.views import *


app_name = 'telegramtemplate'
urlpatterns = [
    # url(r'^telegramtemplate/add/?$', login_required(telegramtemplate_add.as_view()), name='telegramtemplate_add'),
    url(r'^telegramtemplate/list/?$', login_required(telegramtemplate_list.as_view()), name='telegramtemplate_list'),
    url(r'^telegramtemplate/edit/(?P<pk>\d+)/?$', login_required(telegramtemplate_edit.as_view()), name='telegramtemplate_edit'),
]
