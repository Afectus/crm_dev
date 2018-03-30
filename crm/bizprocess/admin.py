# -*- coding: utf-8 -*-
from django.contrib import admin

from django.db import models

from django.forms import TextInput, Textarea

from ckeditor.widgets import CKEditorWidget

from .models import *


class bizplistAdmin(admin.ModelAdmin):
	list_display = ('id', 'name',)
admin.site.register(bizplist, bizplistAdmin)

class bizpstepAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'parent', 'sort',)
admin.site.register(bizpstep, bizpstepAdmin)