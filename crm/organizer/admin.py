#-*- coding: utf-8 -*-

from django.contrib import admin

# Register your models here.
from .models import *

class organizerAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'stime', 'etime',)

admin.site.register(organizer, organizerAdmin)