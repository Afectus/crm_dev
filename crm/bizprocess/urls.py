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
from .diagram import *


app_name = 'bizprocess'
urlpatterns = [
	#diagram
	url(r'^bizprocess/bizplist/detail/(?P<pk>\d+)/?$', login_required(bizplist_detail.as_view()), name='bizplist_detail'),
	url(r'^bizprocess/bizpstep/detail/(?P<pk>\d+)/?$', login_required(bizpstep_detail.as_view()), name='bizpstep_detail'),
	#
	#bizplist
	url(r'^bizprocess/bizplist/list/?$', login_required(bizplist_list.as_view()), name='bizplist_list'),
	url(r'^bizprocess/bizplist/add/?$', login_required(bizplist_add.as_view()), name='bizplist_add'),
	url(r'^bizprocess/bizplist/edit/(?P<pk>\d+)/?$', login_required(bizplist_edit.as_view()), name='bizplist_edit'),
	url(r'^bizprocess/bizplist/table/detail/(?P<pk>\d+)/?$', login_required(bizplist_table_detail.as_view()), name='bizplist_table_detail'),
	#bizpstep
	url(r'^bizprocess/bizpstep/add/process/(?P<pk>\d+)/?$', login_required(bizpstep_add_parent.as_view()), name='bizpstep_add_parent'),
	url(r'^bizprocess/bizpstep/add/step/(?P<pk>\d+)/?$', login_required(bizpstep_add_child.as_view()), name='bizpstep_add_child'),
	url(r'^bizprocess/bizpstep/edit/(?P<pk>\d+)/parent/?$', login_required(bizpstep_edit_parent.as_view()), name='bizpstep_edit_parent'),
	url(r'^bizprocess/bizpstep/edit/(?P<pk>\d+)/child/?$', login_required(bizpstep_edit_child.as_view()), name='bizpstep_edit_child'),
	url(r'^bizprocess/bizpstep/table/detail/(?P<pk>\d+)/?$', login_required(bizpstep_table_detail.as_view()), name='bizpstep_table_detail'),
	url(r'^bizprocess/bizpstep/del/(?P<pk>\d+)/?$', login_required(bizpstep_del.as_view()), name='bizpstep_del'),
	url(r'^bizprocess/bizpstep/del/(?P<pk>\d+)/parent/?$', login_required(bizpstep_del_parent.as_view()), name='bizpstep_del_parent'),
	url(r'^bizprocess/bizpstep/del/(?P<pk>\d+)/child/?$', login_required(bizpstep_del_child.as_view()), name='bizpstep_del_child'),
	
	
	

]





