# -*- coding: utf-8 -*-
from django.contrib import admin
from panel.models import *
from django.db import models

from django.forms import TextInput, Textarea

from ckeditor.widgets import CKEditorWidget

from .models import *

class invlistAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'cdate', 'status', 'user', 'message', )
admin.site.register(invlist, invlistAdmin)


class invitemAdmin(admin.ModelAdmin):
	list_display = ('id', 'ctime', 'invlist', 'goods', 'barcode', 'lifedate', 'message', )
admin.site.register(invitem, invitemAdmin)


