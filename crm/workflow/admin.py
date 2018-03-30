# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models

from django.forms import TextInput, Textarea

from django.contrib.auth.models import User, Group

from ckeditor.widgets import CKEditorWidget

from workflow.models import *


class printtaskAdmin(admin.ModelAdmin):
	list_display = ('id', 'status', 'goods', 'copies', )
	
admin.site.register(printtask, printtaskAdmin)

class distributormenuAdmin(admin.ModelAdmin):
	list_display = ('id', 'name',)
	
admin.site.register(distributormenu, distributormenuAdmin)

class distributorAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'distributormenu',)
	
admin.site.register(distributor, distributorAdmin)