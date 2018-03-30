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


app_name = 'report'
urlpatterns = [
	url(r'^report/list/?$', login_required(report_list.as_view())),
	#список чеков
	url(r'^report/sale/list/?$', login_required(report_sale_list.as_view())),
	#отчет мотивация
	url(r'^report/motivation/?$', login_required(report_motivation.as_view())),
	#отчет продаж
	#url(r'^report/sale/?$', login_required(report_sale.as_view())),
	#url(r'^report/sale/?$', RedirectView.as_view(url='/report/sale/1/')),
	#url(r'^report/sale/(?P<page>\d+)/?$', login_required(report_sale.as_view())),
	#отчет продаж по товарам
	url(r'^report/saletopgoods/?$', login_required(report_sale_topgoods.as_view())),
	#отчет продаж по топ товарам
	url(r'^report/salegoods/?$', RedirectView.as_view(url='/report/salegoods/1/')),
	url(r'^report/salegoods/(?P<page>\d+)/?$', login_required(report_sale_goods.as_view())),
	#отчет сумма период
	url(r'^report/sumperiod/?$', RedirectView.as_view(url='/report/sumperiod/1/')),
	url(r'^report/sumperiod/(?P<page>\d+)/?$', login_required(report_sumperiod.as_view())),
	#ABC Анализ
	url(r'^report/abcgoods/?$', RedirectView.as_view(url='/report/abcgoods/1/')),
	url(r'^report/abcgoods/(?P<page>\d+)/?$', login_required(report_abcgoods.as_view())),
	#отчет счетчик посетителей
	url(r'^report/visitor/?$', RedirectView.as_view(url='/report/visitor/1/')),
	url(r'^report/visitor/(?P<page>\d+)/?$', login_required(report_visitor.as_view())),
	#отчет счетчик посетителей период
	url(r'^report/visitorperiod/?$', RedirectView.as_view(url='/report/visitorperiod/1/')),
	url(r'^report/visitorperiod/(?P<page>\d+)/?$', login_required(report_visitor_period.as_view())),
	#Список покупателей покупок от сумму до суммы xpage
	url(r'^report/buyertop/?$', login_required(report_buyertop.as_view())),
]





