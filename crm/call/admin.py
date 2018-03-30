# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *


class callreportlogAdmin(admin.ModelAdmin):
	list_display = ('id', 'ctime', 'route', 'phone', 'phone8', 'incoming_number', 'info',)
	#date_hierarchy = 'time'

admin.site.register(callreportlog, callreportlogAdmin)


# class SmstemplateAdmin(admin.ModelAdmin):
	# list_display = ('id', 'status', 'sort', 'name', 'message', )

# admin.site.register(smstemplate, SmstemplateAdmin)



# class SmsqsendAdmin(admin.ModelAdmin):
	# list_display = ('id', 'status', 'cdate', 'buyer', 'backurl', 'message', 'result', )

# admin.site.register(smsqsend, SmsqsendAdmin)



# class callreportAdmin(admin.ModelAdmin):
	# list_display = ('id', 'user', 'phone', 'time', 'status',)
	# date_hierarchy = 'time'

# admin.site.register(callreport, callreportAdmin)