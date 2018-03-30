# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models

from django.forms import TextInput, Textarea

from django.contrib.auth.models import User, Group

from ckeditor.widgets import CKEditorWidget

from .models import *


class projectsAdmin(admin.ModelAdmin):
	list_display = ('id', 'name',)
	
admin.site.register(projects, projectsAdmin)

