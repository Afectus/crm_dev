# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from django.db import models

from django.forms import TextInput, Textarea

from ckeditor.widgets import CKEditorWidget


from .models import *

class librarybookAdmin(admin.ModelAdmin):
	list_display = ('id', 'ctime', 'user', 'name', 'desc', )
admin.site.register(librarybook, librarybookAdmin)


class librarybooklikeAdmin(admin.ModelAdmin):
	list_display = ('id', 'librarybook', 'user', )
admin.site.register(librarybooklike, librarybooklikeAdmin)

class librarybookcommentAdmin(admin.ModelAdmin):
	list_display = ('id', 'ctime', 'librarybook', 'user', 'message')
admin.site.register(librarybookcomment, librarybookcommentAdmin)

class librarybookdownloadAdmin(admin.ModelAdmin):
	list_display = ('id', 'ctime', 'librarybook', 'user')
admin.site.register(librarybookdownload, librarybookdownloadAdmin)
