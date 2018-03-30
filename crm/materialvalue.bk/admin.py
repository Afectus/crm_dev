# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import *

class materialvalueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(materialvalue, materialvalueAdmin)

class materialvaluemoveAdmin(admin.ModelAdmin):
    list_display = ('id', 'note')

admin.site.register(materialvaluemove, materialvaluemoveAdmin)

class materialvaluegmoveAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(materialvaluegmove, materialvaluegmoveAdmin)