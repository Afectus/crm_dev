# Register your models here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from django.db import models

from django.forms import TextInput, Textarea

#from ckeditor.widgets import CKEditorWidget

from .models import *

class instructionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'file')

admin.site.register(instructions, instructionsAdmin)