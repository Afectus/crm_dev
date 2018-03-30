from django.contrib import admin

from .models import *

class softsAdmin(admin.ModelAdmin):
	list_display = ('id', )
admin.site.register(softs, softsAdmin)
