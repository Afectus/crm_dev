# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models

from django.forms import TextInput, Textarea

from django.contrib.auth.models import User, Group

from ckeditor.widgets import CKEditorWidget

from bitrix.models import *

class ReviewAdmin(admin.ModelAdmin):
	list_display = ('id', 'ctime', 'subj', 'uname', 'phone', 'email', 'order', 'message',)
	
admin.site.register(review, ReviewAdmin)


class buyermessageAdmin(admin.ModelAdmin):
	list_display = ('id', 'buyer', 'ctime', 'message',)
admin.site.register(buyermessage, buyermessageAdmin)

