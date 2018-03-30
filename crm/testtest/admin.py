# -*- coding: utf-8 -*-
from django.contrib import admin

from django.db import models

from django.forms import TextInput, Textarea

from ckeditor.widgets import CKEditorWidget

from .models import *


class testaAdmin(admin.ModelAdmin):
	list_display = ('id', 'name',)
admin.site.register(testa, testaAdmin)

class testbAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'parent', 'sort',)
admin.site.register(testb, testbAdmin)