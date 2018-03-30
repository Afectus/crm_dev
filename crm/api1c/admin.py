# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models

from django.forms import TextInput, Textarea

from django.contrib.auth.models import User, Group

from ckeditor.widgets import CKEditorWidget

from .models import *

class uploadzipAdmin(admin.ModelAdmin):
	list_display = ('id', 'name',)
admin.site.register(uploadzip, uploadzipAdmin)

class logexchangeAdmin(admin.ModelAdmin):
	list_display = ('id', 'success', 'ftime', 'ctime', 'exectime', 'procedureexchange', 'target', 'fname',  'sourcefile')
	list_filter = ('success', 'procedureexchange', )
	
	def exectime(self, obj):
		return '%s:%s %s:%s' % (obj.startexectime.hour, obj.startexectime.minute, obj.endexectime.hour, obj.endexectime.minute)
	exectime.short_description  = u'Время'
	exectime.allow_tags = True
	
	
admin.site.register(logexchange, logexchangeAdmin)

class procedureexchangeAdmin(admin.ModelAdmin):
	list_display = ('id', 'status', 'start', 'name', 'code', 'sort', 'comment', 'fname', 'parent', 'mono', 'cron',)
admin.site.register(procedureexchange, procedureexchangeAdmin)


