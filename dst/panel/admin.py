# -*- coding: utf-8 -*-
from django.contrib import admin
from panel.models import *
from django.db import models

from django.forms import TextInput, Textarea

from ckeditor.widgets import CKEditorWidget

class panelmenuAdmin(admin.ModelAdmin):
	list_display = ('id', 'myname', 'url', 'icon', 'parent', 'sort')
	
	def myname(self, obj):
		return '%s - %s' % (obj.name, obj.parent)
	
admin.site.register(panelmenu, panelmenuAdmin)

class ProfileUserAdmin(admin.ModelAdmin):
	list_display = ('id', 'role', 'user', 'phone', 'telegram',)
	list_filter = ('role', )
admin.site.register(profileuser, ProfileUserAdmin)


class childbookAdmin(admin.ModelAdmin):
	list_display = ('id', 'ctime', 'child',)
admin.site.register(childbook, childbookAdmin)


class goodfixAdmin(admin.ModelAdmin):
	list_display = ('id',)
admin.site.register(goodfix, goodfixAdmin)



class saleplanshopAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'value', 'ctime', 'sdate', 'edate',)
admin.site.register(saleplanshop, saleplanshopAdmin)

class EventcallAdmin(admin.ModelAdmin):
	list_display = ('id', 'comment')
	
admin.site.register(eventcall, EventcallAdmin)

class imagebaseAdmin(admin.ModelAdmin):
	list_display = ('id', 'ctime', 'title', 'pict', )
admin.site.register(imagebase, imagebaseAdmin)
