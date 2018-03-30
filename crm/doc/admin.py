# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models

from django.forms import TextInput, Textarea

from django.contrib.auth.models import User, Group

from ckeditor.widgets import CKEditorWidget

from node.models import *

class docAdmin(admin.ModelAdmin):
	list_display = ('id', 'name',)
	list_filter = ('name', )
	search_fields = ['id', 'name',]
	save_on_top = True
	
	def mypict(self, obj):
		try:
			return '<img src="%s" />' % obj.pict1.url
		except:
			return 'image'
	mypict.short_description  = u'Картинка'
	mypict.allow_tags = True

	
admin.site.register(doc, docAdmin)





