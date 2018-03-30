from django.urls import path, re_path
from django.contrib.auth.decorators import login_required

from .views import *

urlpatterns = [
	# views
	re_path('^deliveryapp/dellist/list/?$', login_required(dellist_list.as_view()), name='dellist_list'),
	re_path('^deliveryapp/dellist/my-list/?$', login_required(dellist_mylist.as_view()), name='dellist_mylist'),
	re_path('^deliveryapp/dellist/add/?$', login_required(dellist_add.as_view()), name='dellist_add'),
	re_path('^deliveryapp/dellist/(?P<pk>\d+)/?$', login_required(dellist_detail.as_view()), name='dellist_detail'),
	re_path('^deliveryapp/dellist/edit/(?P<pk>\d+)/?$', login_required(dellist_edit.as_view()), name='dellist_edit'),
	re_path('^deliveryapp/dellist/accept/(?P<pk>\d+)/?$', login_required(dellist_accept), name='dellist_accept'),
	re_path('^deliveryapp/dellist/success/(?P<pk>\d+)/?$', login_required(dellist_success), name='dellist_success'),
]
