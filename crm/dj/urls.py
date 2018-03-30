# -*- coding: utf-8 -*-

from django.contrib import admin
from django.urls import path

from django.conf.urls import include, url

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

def auth_logout(request):
	auth.logout(request)
	return HttpResponseRedirect("/user/login")
	
	
def getcap(request):
	from django.http import HttpResponse
	import json
	from captcha.models import CaptchaStore
	from captcha.helpers import captcha_image_url
	newcapkey = CaptchaStore.generate_key()
	newcapimg  = captcha_image_url(newcapkey)
	tmp={'res': 1, 'key': newcapkey, 'img': newcapimg,}
	return HttpResponse(json.dumps(tmp), content_type='application/json')
	

class test(TemplateView):
	template_name = 'test.html'
	
class test2(TemplateView):
	template_name = 'test2.html'
	
def my404(request):
	return render(request, '404.html', status=404)
	
def my500(request):
	return render(request, '500.html', status=500)

handler404 = my404
handler500 = my500
	
	

urlpatterns = [
	#include app urls
	#misha
	url(r'^', include('report3.urls')),
	url(r'^', include('softapp.urls')),
	url(r'^', include('deliveryapp.urls')),
	#algol
	url(r'^', include('accountstorage.urls')),
	url(r'^', include('project.urls')),
	url(r'^', include('report2.urls')),
	url(r'^', include('instructions.urls')),
	url(r'^', include('normact.urls')),
	url(r'^', include('telegramtemplate.urls')),
	url(r'^', include('corpmail.urls')),
	url(r'^', include('materialvalue.urls')),
	url(r'^', include('organizer.urls')),
	url(r'^', include('pictgallery.urls')),
	url(r'^', include('useridea2.urls')),
	url(r'^', include('newsfeed.urls')),
	url(r'^', include('docflow.urls')),
	#
	#url(r'^', include('testtest.urls')),
	url(r'^', include('acl.urls')),
	url(r'^', include('notify.urls')),
	url(r'^', include('opt.urls')),
	url(r'^', include('library.urls')),
	url(r'^', include('marketing.urls')),
	url(r'^', include('userauth.urls')),
	url(r'^', include('panel.urls')),
	url(r'^', include('node.urls')),
	url(r'^', include('sms.urls')),
	url(r'^', include('call.urls')),
	url(r'^', include('projects.urls')),
	url(r'^', include('workgraph.urls')),
	url(r'^', include('holiday.urls')),
	url(r'^', include('personal.urls')),
	url(r'^', include('device.urls')),
	url(r'^', include('screen.urls')),
	url(r'^', include('screen1.urls')),
	url(r'^', include('screen2.urls')),
	url(r'^', include('video.urls')),
	url(r'^', include('report.urls')),
	url(r'^', include('mod.urls')),
	url(r'^', include('it.urls')),
	url(r'^', include('workflow.urls')),
	url(r'^', include('pricetag.urls')),
	url(r'^', include('worktask.urls')),
	url(r'^', include('useridea.urls')),
	url(r'^', include('bitrix.urls')),
	url(r'^', include('api1c.urls')),
	url(r'^', include('inventory.urls')),
	url(r'^', include('order.urls')),
	url(r'^', include('kassir.urls')),
	url(r'^', include('log.urls')),
	url(r'^', include('bizprocess.urls')),
	#
	url(r'^', include('testtest.urls')),
	#
	url(r'^test/?$', test.as_view()),
	url(r'^test2/?$', test2.as_view()),
	#
	url(r'^user/logout/?$', auth_logout),
	url(r'^getcap/?$', getcap),
	#
	url(r'^captcha/', include('captcha.urls')),
	path('admin/', admin.site.urls),
	url(r'^i18n/', include('django.conf.urls.i18n')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_title = 'CRM'
admin.site.site_header = 'CRM'


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]


