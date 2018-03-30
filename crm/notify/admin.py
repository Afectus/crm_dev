# -*- coding: utf-8 -*-
from django.contrib import admin

from django.db import models

from django.forms import TextInput, Textarea

from ckeditor.widgets import CKEditorWidget

from .models import *

class notifyqueueAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'ctime', 'during', 'handler', 'value',)
	list_filter = ('during',)
	save_as = True
admin.site.register(notifyqueue, notifyqueueAdmin)


class notifyhandlerAdmin(admin.ModelAdmin):
	list_display = ('id', 'status', 'name', )
	save_as = True
admin.site.register(notifyhandler, notifyhandlerAdmin)

class notifyuserkeyAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'handler', 'value', )
	save_as = True
admin.site.register(notifyuserkey, notifyuserkeyAdmin)

