# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from django.db import models

from django.forms import TextInput, Textarea

from ckeditor.widgets import CKEditorWidget


from useridea.models import *

class UserideaAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'ctime', 'name', 'message', )
admin.site.register(useridea, UserideaAdmin)


class fileideaAdmin(admin.ModelAdmin):
	list_display = ('id', 'sourcefile', )
admin.site.register(fileidea, fileideaAdmin)

class likeideaAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'useridea', 'value')
admin.site.register(likeidea, likeideaAdmin)

class commentideaAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'useridea', 'message')
admin.site.register(commentidea, commentideaAdmin)

