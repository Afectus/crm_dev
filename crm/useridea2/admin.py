# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from django.db import models

from django.forms import TextInput, Textarea

from ckeditor.widgets import CKEditorWidget


from useridea2.models import *

class UserideasectionAdmin(admin.ModelAdmin):
	list_display = ('id', 'name' )

admin.site.register(ideasection, UserideasectionAdmin)

class Useridea2Admin(admin.ModelAdmin):
	list_display = ('id', 'name' )

admin.site.register(useridea, Useridea2Admin)

class commentidea2Admin(admin.ModelAdmin):
	list_display = ('id', 'user', 'useridea', 'message')

admin.site.register(commentidea, commentidea2Admin)

class fileidea2Admin(admin.ModelAdmin):
	list_display = ('id', 'sourcefile', )
admin.site.register(file, fileidea2Admin)

class pictidea2Admin(admin.ModelAdmin):
	list_display = ('id', 'pict', )
admin.site.register(picture, pictidea2Admin)

class likeidea2Admin(admin.ModelAdmin):
	list_display = ('id', 'user', 'useridea', 'value')
admin.site.register(likeidea, likeidea2Admin)



