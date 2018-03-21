from django.conf.urls import include, url
from django.contrib import admin

# from django.conf import settings
# from django.conf.urls.static import static

from django.contrib import auth
# from django.shortcuts import HttpResponseRedirect
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

# from django.views.generic.base import TemplateView
from django.views.generic import RedirectView

# from django.shortcuts import render_to_response, render

from .views import *


app_name = 'report2'
urlpatterns = [
    url(r'^report/smssale/?$', login_required(report2_smssale.as_view()), name='sms_sale'),
	url(r'^report/points/?$', login_required(report_points.as_view()), name='report_points'),
	url(r'^report/smssaleafter/?$', login_required(report2_smssale_after.as_view()), name='sms_sale_after'),
]