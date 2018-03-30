# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models

from django.forms import TextInput, Textarea

from django.contrib.auth.models import User, Group

from ckeditor.widgets import CKEditorWidget

from it.models import *

class techinfoAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'desc', 'pict', 'techfile', )
	search_fields = ['name', 'desc',]
	save_on_top = True
	'''
	def myurl(self, obj):
		tmp=''
		tmp=tmp+'%s=%s</br>' % ('starturl', obj.starturl)
		tmp=tmp+'%s=%s</br>' % ('catalogserverurl', obj.catalogserverurl)
		return tmp
	myurl.short_description  = u'Настройки'
	myurl.allow_tags = True
	'''
	
admin.site.register(techinfo, techinfoAdmin)


class usermanualAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'desc', )
	search_fields = ['name', 'desc',]
	save_on_top = True
	
admin.site.register(usermanual, usermanualAdmin)

