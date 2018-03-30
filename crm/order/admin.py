# -*- coding: utf-8 -*-
from django.contrib import admin
from order.models import *
from django.db import models

from django.forms import TextInput, Textarea

from ckeditor.widgets import CKEditorWidget


class OrderAdmin(admin.ModelAdmin):
	list_display = ('id', 'bitrixorderid', 'ctime', 'phone', 'uname', 'city', 'status', )
	search_fields = ['id', 'bitrixorderid', 'uname', 'phone', ]
	list_filter = ('status',)
	
	save_as = True
	
admin.site.register(order, OrderAdmin)


class ordercartlistAdmin(admin.ModelAdmin):
	list_display = ('id', 'order', 'ctime', 'goods', 'goods', 'name', 'col', )
	#search_fields = ['id', 'bitrixorderid', 'uname', 'phone', ]
	#list_filter = ('status',)
	
	save_as = True
	
admin.site.register(ordercartlist, ordercartlistAdmin)






class ordereventAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'order', 'ctime', 'event', 'comment', 'info')
	#list_filter = ('status',)
	save_as = True
	
admin.site.register(orderevent, ordereventAdmin)


class ordermanagerAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'handler', 'schedule', 'sort', 'shift',)
	#list_filter = ('status',)
	save_as = True
	
admin.site.register(ordermanager, ordermanagerAdmin)




