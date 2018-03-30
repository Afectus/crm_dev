
# Register your models here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from django.db import models

from django.forms import TextInput, Textarea

#from ckeditor.widgets import CKEditorWidget

from .models import *

class pictgalleryAdmin(admin.ModelAdmin):
    list_display = ('id', 'desc', 'pict')

admin.site.register(pictgallery, pictgalleryAdmin)