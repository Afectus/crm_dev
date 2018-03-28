from django.urls import path, re_path
from django.contrib.auth.decorators import login_required

from .views import *
from .panel import *

urlpatterns = [
	# views
	re_path('^softapp/softs/list/?$', login_required(softs_list.as_view()), name='softs_list'),
	re_path('^softapp/softs/(?P<pk>\d+)/?$', login_required(softs_detail.as_view()), name='softs_detail'),
	# panel
	re_path('^panel/softs/list/?$', login_required(panel_softs_list.as_view()), name='panel_softs_list'),
	re_path('^panel/softs/add/?$', login_required(panel_softs_add.as_view()), name='panel_softs_add'),
	re_path('^panel/softs/del/(?P<pk>\d+)/?$', login_required(panel_softs_del.as_view()), name='panel_softs_del'),
	re_path('^panel/softs/edit/(?P<pk>\d+)/?$', login_required(panel_softs_edit.as_view()), name='panel_softs_edit'),
]
