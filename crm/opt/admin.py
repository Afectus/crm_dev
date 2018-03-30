# -*- coding: utf-8 -*-
from django.contrib import admin
from panel.models import *
from django.db import models

from django.forms import TextInput, Textarea

from ckeditor.widgets import CKEditorWidget


from .models import *

class optbuyerAdmin(admin.ModelAdmin):
	list_display = ('id', 'name',)
admin.site.register(optbuyer, optbuyerAdmin)

class optpriceAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'url', 'comment',)
admin.site.register(optprice, optpriceAdmin)

class optpricecartAdmin(admin.ModelAdmin):
	list_display = ('id', 'optprice', 'goods', 'quant', )
admin.site.register(optpricecart, optpricecartAdmin)
