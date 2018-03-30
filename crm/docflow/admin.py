# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import *

class docflow_category_Admin(admin.ModelAdmin):
	list_display = ('id', 'name')

admin.site.register(docflow_category, docflow_category_Admin)

class docflowfileAdmin(admin.ModelAdmin):
	list_display = ('id', 'name')

admin.site.register(docflowfile, docflowfileAdmin)

class cash_payment_voucherAdmin(admin.ModelAdmin):
	list_display = ('id', 'name')

admin.site.register(cash_payment_voucher, cash_payment_voucherAdmin)

# class kontragentmenuAdmin(admin.ModelAdmin):
# 	list_display = ('id', 'name',)
	
# admin.site.register(kontragentmenu, kontragentmenuAdmin)

# class kontragentAdmin(admin.ModelAdmin):
# 	list_display = ('id', 'name', 'kontragentmenu',)
	
# admin.site.register(kontragent, kontragentAdmin)