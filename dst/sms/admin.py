# -*- coding: utf-8 -*-
from django.contrib import admin
from sms.models import *


class SmsreportAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'phone', 'time', 'text', 'status',)
	date_hierarchy = 'time'

admin.site.register(smsreport, SmsreportAdmin)


class SmstemplateAdmin(admin.ModelAdmin):
	list_display = ('id', 'status', 'sort', 'name', 'message', )

admin.site.register(smstemplate, SmstemplateAdmin)



class SmsqsendAdmin(admin.ModelAdmin):
	list_display = ('id', 'status', 'send', 'cdate', 'buyer', 'backurl', 'message', 'result', )

admin.site.register(smsqsend, SmsqsendAdmin)



class callreportAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'phone', 'time', 'status',)
	date_hierarchy = 'time'

admin.site.register(callreport, callreportAdmin)