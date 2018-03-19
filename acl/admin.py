# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models

from django.forms import TextInput, Textarea

from ckeditor.widgets import CKEditorWidget

from .models import *
from panel.models import *


class aclobjectAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'objectid',)
admin.site.register(aclobject, aclobjectAdmin)


class acluAdmin(admin.ModelAdmin):
	list_display = ('id', 'status', 'aclobject', 'user', 'type', 'ctime', 'etime',)
	list_filter = ('status', 'aclobject', 'type')
admin.site.register(aclu, acluAdmin)

class aclgAdmin(admin.ModelAdmin):
	list_display = ('id', 'status', 'aclobject', 'group', 'type', 'ctime', 'etime',)
	list_filter = ('status', 'aclobject', 'type')
admin.site.register(aclg, aclgAdmin)