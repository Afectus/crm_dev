# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models

from django.forms import TextInput, Textarea

from ckeditor.widgets import CKEditorWidget


from mod.models import *




class ballconfitemAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'bid', 'x', 'y', 'radius', 'color', 'colortext', 'background')
	
	list_filter = ('name', )
admin.site.register(ballconfitem, ballconfitemAdmin)

class goreportAdmin(admin.ModelAdmin):
	list_display = ('id', 'time', 'ua', 'ip',)

admin.site.register(goreport, goreportAdmin)

class qrcodereportAdmin(admin.ModelAdmin):
	list_display = ('id', 'time', 'mycomment', 'ua', 'ip',)
	
	def mycomment(self, obj):
		return '<a href="%s" target="_blank">%s</a>' % (obj.comment, obj.comment)
	mycomment.short_description  = u'Комментарий'
	mycomment.allow_tags = True

admin.site.register(qrcodereport, qrcodereportAdmin)
