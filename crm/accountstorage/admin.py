# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import *

class accountstorageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )

admin.site.register(accountstorage, accountstorageAdmin)