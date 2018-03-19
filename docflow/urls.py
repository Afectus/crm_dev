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
# from docflow_category.views import *


app_name = 'docflow'
urlpatterns = [
	url(r'^docflow/category/add/?$', login_required(docflow_category_add.as_view()), name='docflow_category_add'),
	url(r'^docflow/category/list/?$', login_required(docflow_category_list.as_view()), name='docflow_category_list'),
	url(r'^docflow/category/edit/(?P<pk>\d+)/?$', login_required(docflow_category_edit.as_view()), name='docflow_category_edit'),
	url(r'^docflow/category/del/(?P<pk>\d+)/?$', login_required(docflow_category_del.as_view()), name='docflow_category_del'),
	url(r'^docflow/voucher/user/add/?$', login_required(cash_payment_voucher_add.as_view()), name='cash_payment_voucher_add'),
	url(r'^docflow/voucher/kontragent/add/?$', login_required(cash_payment_voucher_kontragent_add.as_view()), name='cash_payment_voucher_kontragent_add'),
	url(r'^docflow/voucher/list/?$', login_required(cash_payment_voucher_list.as_view()), name='cash_payment_voucher_list'),
	url(r'^docflow/voucher/admin/list/?$', login_required(cash_payment_voucher_admin_list.as_view()), name='cash_payment_voucher_admin_list'),
	url(r'^docflow/voucher/edit/(?P<pk>\d+)/?$', login_required(cash_payment_voucher_edit.as_view()), name='cash_payment_voucher_edit'),
	url(r'^docflow/voucher/status/(?P<pk>\d+)/?$', login_required(cash_payment_voucher_change_status.as_view()), name='cash_payment_voucher_change_status'),
	url(r'^docflow/voucher/del/(?P<pk>\d+)/?$', login_required(cash_payment_voucher_del.as_view()), name='cash_payment_voucher_del'),
	url(r'^docflow/file/del/(?P<pk>\d+)/?$', login_required(docflowfile_del.as_view()), name='docflowfile_del'),
	url(r'^docflow/file/add/(?P<pk>\d+)/?$', login_required(docflowfile_add.as_view()), name='docflowfile_add'),
	# # url(r'^projectcomment/file/del/(?P<pk>\d+)/?$', login_required(projectcomment_file_del.as_view()), name='projectcomment_file_del'),
	#контрагенты
	# url(r'^kontragent/list/?$', login_required(kontragent_list.as_view())),
	# url(r'^kontragent/list/(?P<pk>\d+)/?$', login_required(kontragent_list.as_view())),
	# url(r'^kontragent/add/?$', login_required(kontragent_add.as_view()), name='kontragent_add'),
	# url(r'^kontragent/edit/(?P<pk>\d+)/?$', login_required(kontragent_edit.as_view())),
	# url(r'^kontragentmenu/edit/(?P<pk>\d+)/?$', login_required(kontragentmenu_edit.as_view()), name='kontragentmenu_edit'),
]
