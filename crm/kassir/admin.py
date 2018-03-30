# -*- coding: utf-8 -*-
from django.contrib import admin

from django.db import models

from django.forms import TextInput, Textarea

from ckeditor.widgets import CKEditorWidget

from .models import *




class kassirvisitorlogAdmin(admin.ModelAdmin):
	list_display = ('id', )
admin.site.register(kassirvisitorlog, kassirvisitorlogAdmin)
