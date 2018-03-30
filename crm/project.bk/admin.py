# Register your models here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from django.db import models

from django.forms import TextInput, Textarea

#from ckeditor.widgets import CKEditorWidget

from .models import *

class projectAdmin(admin.ModelAdmin):
    list_display = ('id', )

admin.site.register(project, projectAdmin)

class projectcommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'value')

admin.site.register(projectcomment, projectcommentAdmin)

class projectstepAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'edate', 'desc')

admin.site.register(projectstep, projectstepAdmin)

class projectpictAdmin(admin.ModelAdmin):
    list_display = ('id', 'pict')

admin.site.register(projectpict, projectpictAdmin)

class projectfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'sourcefile')

admin.site.register(projectfile, projectfileAdmin)