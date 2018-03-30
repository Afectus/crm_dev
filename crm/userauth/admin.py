# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models

from django.forms import TextInput, Textarea

from ckeditor.widgets import CKEditorWidget


from .models import *


class Userloginblockdb(admin.ModelAdmin):
	list_display = ('id', 'user', 'ip', 'starttime', 'blocktime',)
admin.site.register(userloginblockdb, Userloginblockdb)

