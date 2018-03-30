# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models

from django.forms import TextInput, Textarea

from ckeditor.widgets import CKEditorWidget


from personal.models import *


class personalchildAdmin(admin.ModelAdmin):
	list_display = ('id', 'profileuser', 'name', 'bday',)
admin.site.register(personalchild, personalchildAdmin)



class personalfeatAdmin(admin.ModelAdmin):
	list_display = ('id', 'profileuser', 'ctime', 'name', )
admin.site.register(personalfeat, personalfeatAdmin)


class personalanketaAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', )
admin.site.register(personalanketa, personalanketaAdmin)


