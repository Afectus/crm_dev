# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from django.db import models

from django.forms import TextInput, Textarea

from ckeditor.widgets import CKEditorWidget


from worktask.models import *

class UsertaskAdmin(admin.ModelAdmin):
	list_display = ('id', 'status', 'priority', 'user', 'ctime', 'name', 'message', )
admin.site.register(usertask, UsertaskAdmin)


class filetaskAdmin(admin.ModelAdmin):
	list_display = ('id', 'sourcefile', )
admin.site.register(filetask, filetaskAdmin)

class liketaskAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'usertask', 'value')
admin.site.register(liketask, liketaskAdmin)

class commenttaskAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'usertask', 'message')
admin.site.register(commenttask, commenttaskAdmin)


class notificationtaskAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'usertask', )
admin.site.register(notificationtask, notificationtaskAdmin)
