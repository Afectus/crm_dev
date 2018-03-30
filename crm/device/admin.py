# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models

from django.forms import TextInput, Textarea

from django.contrib.auth.models import User, Group

from ckeditor.widgets import CKEditorWidget

from device.models import *

class DeviceAdmin(admin.ModelAdmin):
	list_display = ('id', 'shopset', 'name', 'status', 'os_system', 'mac', 'ip', 'vpnip', 'pingsave', 'pingsetip', 'pingcron', )
	
	def myurl(self, obj):
		tmp=''
		tmp=tmp+'%s=%s</br>' % ('starturl', obj.starturl)
		tmp=tmp+'%s=%s</br>' % ('catalogserverurl', obj.catalogserverurl)
		return tmp
	myurl.short_description  = u'Настройки'
	myurl.allow_tags = True
	
admin.site.register(device, DeviceAdmin)


class playlistAdmin(admin.ModelAdmin):
	list_display = ('id', 'status', 'name', 'url',)
	
admin.site.register(playlist, playlistAdmin)
	

class shopsetAdmin(admin.ModelAdmin):
	list_display = ('id', 'shop', )
	
admin.site.register(shopset, shopsetAdmin)


class mediaAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'format', 'file', 'audio', 'promo', 'instruction', 'advertising')
	
admin.site.register(media, mediaAdmin)



class countvisitorAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'event', 'shop', 'ctime', 'counttime', 'minface', 'maxface', 'mineye', 'maxeye', 'video', 'zip', )
	list_filter = ('shop', 'event', )
	#date_hierarchy = 'ctime'
	
admin.site.register(countvisitor, countvisitorAdmin)

