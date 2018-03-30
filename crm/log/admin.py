# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models

from django.forms import TextInput, Textarea

from django.contrib.auth.models import User, Group

from ckeditor.widgets import CKEditorWidget

from log.models import *


class CommonlogAdmin(admin.ModelAdmin):
	list_display = ('id', 'ctime', 'name', 'desc',)
	search_fields = ['id', 'name',]
	list_filter = ('name',)
	save_on_top = True
admin.site.register(commonlog, CommonlogAdmin)

class kassirlogAdmin(admin.ModelAdmin):
	list_display = ('id', 'ctime', 'name', 'desc', 'user')
	search_fields = ['id', 'name', 'desc']
	list_filter = ('name', 'user', )
	save_on_top = True
admin.site.register(kassirlog, kassirlogAdmin)


class MailresAdmin(admin.ModelAdmin):
	list_display = ('id', 'status', 'ctime', 'email', 'action', 'result')
admin.site.register(mailres, MailresAdmin)