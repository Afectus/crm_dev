from django.contrib import admin
from .models import *

class tsAdmin(admin.ModelAdmin):
	list_display = ('id', )
admin.site.register(ts, tsAdmin)

class dellistAdmin(admin.ModelAdmin):
	list_display = ('id', )
admin.site.register(dellist, dellistAdmin)

class deleventAdmin(admin.ModelAdmin):
	list_display = ('id', )
admin.site.register(delevent, deleventAdmin)