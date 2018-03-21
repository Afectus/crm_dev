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
from .buyer import *
from .goods import *
from .goods_json import *
from .api import *



class saveonclose(TemplateView):
	template_name = '_saveonclose.html'

app_name = 'panel'
urlpatterns = [
	url(r'^$', login_required(home.as_view())),
	#api
	url(r'^api/goods/video/edit/?$', api_goods_video_edit, name='api_goods_video_edit'),
	
	#################МОТИВАЦИЯ
	url(r'^motivation/report/list/table/?$', login_required(motivation_report_list_table.as_view())),
	url(r'^motivation/report/list/json/?$', login_required(motivation_report_list_json)),
	#
	url(r'^goodsmotivationratiosum/list/?$', login_required(goodsmotivationratiosum_list.as_view()), name='goodsmotivationratiosum_list'),
	url(r'^goodsmotivationratiosum/edit/(?P<pk>\d+)/?$', login_required(goodsmotivationratiosum_edit.as_view()), name='goodsmotivationratiosum_edit'),
	url(r'^shop/list/?$', login_required(shop_list.as_view()), name='shop_list'),
	url(r'^shop/edit/(?P<pk>\d+)/?$', login_required(shop_edit.as_view()), name='shop_edit'),
	################################
	
	
	#
	url(r'^user/restore/?$', user_restore.as_view()),
	url(r'^user/profile/?$', login_required(own_user_profile_edit.as_view())),
	url(r'^user/password/?$', login_required(user_password.as_view())),
	#
	url(r'^form/saveonclose/?$', login_required(saveonclose.as_view()), name='saveonclose'),
	
	#goods_list_public
	url(r'^goods/list/public/?$', login_required(goods_list_public.as_view()), name='goods_list_public'),
	
	#goods_list_light
	url(r'^goods/list/light/?$', login_required(goods_list_light.as_view()), name='goods_list_light'),
	url(r'^goods/edit/light/(?P<pk>\d+)/?$', login_required(goods_edit_light.as_view()), name='goods_edit_light'),
	
	#goods_list
	url(r'^goods/list/?$', RedirectView.as_view(url='/goods/list/1/')),
	url(r'^goods/list/(?P<page>\d+)/?$', login_required(goods_list.as_view()), name='goods_list'),
	url(r'^goods/detail/(?P<pk>\d+)/?$', login_required(goods_detail.as_view()), name='goods_detail'),
	url(r'^goods/edit/(?P<pk>\d+)/?$', login_required(goods_edit.as_view()), name='goods_edit'),
	
	#buyer_list
	url(r'^buyer/detail/(?P<pk>\d+)/?$', login_required(buyer_detail.as_view()), name='buyer_detail'),
	url(r'^buyer/list/?$', login_required(buyer_list.as_view()), name='buyer_list'),
	url(r'^buyer/list/json/$', login_required(buyer_list.as_view())),
	url(r'^buyer/list/(?P<name>\d+).json$', login_required(buyer_list.as_view())),
	url(r'^buyer/edit/(?P<pk>\d+)/?$', login_required(buyer_edit.as_view())),
	#url(r'^buyer/list.json$', login_required(buyer_list_json.as_view())),
	#events
	url(r'^event/call/list/?$', login_required(event_call_list.as_view())),
	url(r'^event/add/call/(?P<pk>\d+)/?$', login_required(event_call_add.as_view())),
	url(r'^event/edit/call/(?P<pk>\d+)/?$', login_required(event_call_edit.as_view())),
	#review
	url(r'^review/list/?$', login_required(panel_review_list.as_view())),
	url(r'^review/edit/(?P<pk>\d+)/?$', login_required(panel_review_edit.as_view())),

	#child_list
	url(r'^child/list/?$', RedirectView.as_view(url='/child/list/1/')),
	url(r'^child/list/(?P<page>\d+)/?$', login_required(panel_child_list.as_view())),
	url(r'^childbook/list/?$', login_required(childbook_list.as_view())),
	#url(r'^childbook/edit/(?P<pk>\d+)/?$', login_required(childbook_edit.as_view())),
	url(r'^childbook/del/(?P<pk>\d+)/?$', login_required(childbook_del.as_view())),
	url(r'^childbook/add/(?P<pk>\d+)/?$', login_required(childbook_add)),
	url(r'^childbook/clear/?$', login_required(childbook_clear)),
	url(r'^childbook/text/?$', login_required(childbook_text.as_view())),
	
	#discounts
	url(r'^discount/list/?$', login_required(discount_list.as_view())),
	url(r'^discount/add/?$', login_required(discount_add.as_view())),
	url(r'^discount/edit/(?P<pk>\d+)/?$', login_required(discount_edit.as_view())),
	
	#goodscert
	url(r'^goodscert/list/?$', login_required(goodscert_list.as_view()), name='goodscert_list'),
	url(r'^goodscert/add/?$', login_required(goodscert_add.as_view()), name='goodscert_add'),
	url(r'^goodscert/edit/(?P<pk>\d+)/?$', login_required(goodscert_edit.as_view()), name='goodscert_edit'),
	
	url(r'^goodscert/goods/?$', login_required(goodscert_goods.as_view()), name='goodscert_goods'),
	
	
	#план продаж магазина
	url(r'^panel/saleplanshop/list/?$', login_required(saleplanshop_list.as_view())),
	url(r'^panel/saleplanshop/add/?$', login_required(saleplanshop_add.as_view())),
	url(r'^panel/saleplanshop/edit/(?P<pk>\d+)/?$', login_required(saleplanshop_edit.as_view())),
	
	#goodfix
	url(r'^panel/goodfix/add/?$', login_required(panel_goodfix_add.as_view())),
	url(r'^panel/goodfix/list/?$', login_required(panel_goodfix_list.as_view())),
	url(r'^panel/goodfix/edit/(?P<pk>\d+)/?$', login_required(panel_goodfix_edit.as_view())),
	
	#buyerevent
	url(r'^buyerevent/list/?$', RedirectView.as_view(url='/buyerevent/list/1/')),
	url(r'^buyerevent/list/(?P<page>\d+)/?$', login_required(buyerevent_list.as_view())),
	url(r'^buyerevent/edit/(?P<pk>\d+)/?$', login_required(buyerevent_edit.as_view())),
	url(r'^buyerevent/add/(?P<pk>\d+)/?$', login_required(buyerevent_add.as_view())),

	url(r'^makecall/(?P<pk>\d+)/?$',  login_required(makecall)), #звонить покупателю
	url(r'^owncallreport/list/?$', login_required(owncallreport_list.as_view())),
	
	#sms
	url(r'^sendsms/?$', login_required(sendsms.as_view())),
	url(r'^sendsms2b/(?P<pk>\d+)/?$', login_required(sendsms2b.as_view())),
	url(r'^ownsmsreport/list/?$', login_required(ownsmsreport_list.as_view())),
	url(r'^smstemplate/list/?$', login_required(smstemplate_list.as_view())),
	url(r'^smstemplate/edit/(?P<pk>\d+)/?$', login_required(smstemplate_edit.as_view())),
	url(r'^smsqsend/list/?$', login_required(smsqsend_list.as_view()), name='smsqsend_list'),
	url(r'^smsqsend/edit/(?P<pk>\d+)/?$', login_required(smsqsend_edit.as_view()), name='smsqsend_edit'),
	url(r'^smsqsend/detail/(?P<pk>\d+)/?$', login_required(smsqsend_detail.as_view())),
	url(r'^smsqsend/del/(?P<pk>\d+)/?$', login_required(smsqsend_del.as_view())),
	url(r'^smsqsend/add/(?P<pk>\d+)/?$', login_required(smsqsend_add)),
	url(r'^smsqsend/clear/?$', login_required(smsqsend_clear)),
	url(r'^backurl/(?P<backurl>\w+)/?$', checkbackurl),
	#
	url(r'^buyer/getphone/(?P<pk>\d+)/?$', login_required(getphone)),
	#imagebase
	url(r'^imagebase/del/(?P<pk>\d+)/?$', login_required(imagebase_del), name='imagebase_del'),
]





