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



app_name = 'worktask'
urlpatterns = [
	url(r'^worktask/add/freetask/?$', login_required(create_freetask.as_view())),
	url(r'^worktask/add/usertask/?$', login_required(create_usertask.as_view())),
	url(r'^worktask/add/file/(?P<pk>\d+)/?$', login_required(create_filetask.as_view())),
	url(r'^worktask/del/file/(?P<pk>\d+)/?$', login_required(remove_filetask.as_view())),
	url(r'^worktask/list/?$', login_required(task_list.as_view())),
	url(r'^worktask/edit/(?P<pk>\d+)/?$', login_required(task_edit.as_view())),
	url(r'^worktask/admin/edit/(?P<pk>\d+)/?$', login_required(admin_task_edit.as_view()), name='admin_task_edit'),
	url(r'^worktask/detail/(?P<pk>\d+)/?$', login_required(task_detail.as_view())),
	url(r'^worktask/like/task/(?P<pk>\d+)/(?P<value>[1-5])/?$', login_required(add_liketask)),
	url(r'^worktask/take/task/(?P<pk>\d+)/?$', login_required(take_task)),
	url(r'^worktask/read/task/(?P<pk>\d+)/?$', login_required(read_task)),
]





