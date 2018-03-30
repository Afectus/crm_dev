# Register your models here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from django.db import models

from django.forms import TextInput, Textarea

#from ckeditor.widgets import CKEditorWidget

from .models import *

class newsfeedAdmin(admin.ModelAdmin):
	list_display = ('id', 'name')

admin.site.register(news, newsfeedAdmin)

class newspictureAdmin(admin.ModelAdmin):
	list_display = ('id', 'desc')

admin.site.register(newspicture, newspictureAdmin)
