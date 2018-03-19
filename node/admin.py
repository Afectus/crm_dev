# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models

from django.forms import TextInput, Textarea

from django.contrib.auth.models import User, Group

from ckeditor.widgets import CKEditorWidget

from node.models import *


class base1cAdmin(admin.ModelAdmin):
	list_display = ('id', 'status', 'name')
	
admin.site.register(base1c, base1cAdmin)

class TaxAdmin(admin.ModelAdmin):
	list_display = ('id', 'id1c', 'idbitrix', 'status', 'name', 'parent')
	
admin.site.register(tax, TaxAdmin)


class StockAdmin(admin.ModelAdmin):
	list_display = ('id', 'status', 'name', 'id1c', 'idbitrix', 'base',)
	
admin.site.register(stock, StockAdmin)

class shopstockAdmin(admin.ModelAdmin):
	list_display = ('id', 'type', 'status', 'name', 'id1c', 'idbitrix', 'base',)
	list_filter = ('type', )
	
admin.site.register(shopstock, shopstockAdmin)


class QinstockAdmin(admin.ModelAdmin):
	list_display = ('id', 'stock', 'value', )
	list_filter = ('stock', )

admin.site.register(qinstock, QinstockAdmin)

class goodsinstockAdmin(admin.ModelAdmin):
	list_display = ('id', 'stock', 'goods', 'value', )
	list_filter = ('stock', )

admin.site.register(goodsinstock, goodsinstockAdmin)




class QinstockInline(admin.StackedInline):
    model = goods.qinstock.through


class GoodsAdmin(admin.ModelAdmin):
	#inlines = (QinstockInline,)
	list_display = ('id', 'mypict', 'myqrcode', 'id1c', 'idbitrix', 'art', 'name', 'utime', 'status', 'video', 'naborparent', 'bname', 'price', 'myqinstock', 'showondemo', 'touchscreen', 'video')
	
	search_fields = ['id', 'id1c', 'idbitrix', 'name', 'bname', 'art', 'video',]
	list_filter = ('showondemo', 'nabor', 'base')
	
	save_on_top = True
	
	def myqinstock(self, obj):
		tmp=''
		for i in obj.qinstock.all():
			tmp=tmp+'%s = %s</br>\n' % (i.stock.name, i.value)
		return tmp
	myqinstock.short_description  = u'Количество на складе'
	myqinstock.allow_tags = True
	
	def mypict(self, obj):
		try:
			return '<img src="%s" />' % obj.pict40.url
		except:
			return 'image'
	mypict.short_description  = u'Картинка'
	mypict.allow_tags = True
	
	def myqrcode(self, obj):
		try:
			return '<a href="%s" target="_blank"><img src="%s" /></a>' % (obj.qrcode500.url, obj.qrcode40.url)
		except:
			return 'qrcode'
	myqrcode.short_description  = u'QRCode'
	myqrcode.allow_tags = True
	
admin.site.register(goods, GoodsAdmin)

class CashboxAdmin(admin.ModelAdmin):
	list_display = ('id', 'id1c', 'status', 'name', 'typecashbox', )
	
	search_fields = ['id', 'id1c', 'name',]
	#list_filter = ('id1c', 'name', )
	
admin.site.register(cashbox, CashboxAdmin)

class ShopAdmin(admin.ModelAdmin):
	list_display = ('id', 'id1c', 'sort', 'status', 'name', 'htmlcolor', 'motivationratio')
	
	search_fields = ['id', 'id1c', 'name',]
	list_filter = ('id1c', 'name', )
	
admin.site.register(shop, ShopAdmin)



class BuyerAdmin(admin.ModelAdmin):
	list_display = ('id', 'id1c', 'myphone', 'f', 'i', 'o', 'sex', 'bday', 'bdayindex', 'ctime', 'lastmodtime', 'creator', 'lastmod',)
	search_fields = ['id', 'id1c', 'phone', 'f', 'i', 'o', ]
	list_filter = ('sex', 'bday', )
	
	'''
	actions = None

	def get_readonly_fields(self, request, obj=None):
		return self.fields or [f.name for f in self.model._meta.fields]

	def has_add_permission(self, request):
		return False

    # Allow viewing objects but not actually changing them
	def has_change_permission(self, request, obj=None):
		if request.method not in ('GET', 'HEAD'):
			return False
		return super(BuyerAdmin, self).has_change_permission(request, obj)

	def has_delete_permission(self, request, obj=None):
		return False
	'''
	def myphone(self, obj):
		a=obj.phone
		left=len(a)-2
		right=len(a)
		filler='*'*left
		res='%s%s' % (filler, a[left:right])
		return res
	myphone.short_description  = u'Телефон'
	myphone.allow_tags = False
	
	
	# def myeventcall(self, obj):
		# tmp='<a href="/event/add/call/%s">Создать событие</a></br>\n</br>\n' % (obj.id)
		# for i in obj.eventcall_set.all():
			# tmp=tmp+'<a href="/admin/node/eventcall/%s/change/">%s</a></br>\n' % (i.id, i.ctime.strftime("%d.%m.%Y %H:%M"))
		# return tmp
	# myeventcall.short_description  = u'События'
	# myeventcall.allow_tags = True

admin.site.register(buyer, BuyerAdmin)


class ChildAdmin(admin.ModelAdmin):
	list_display = ('id', 'id1c', 'buyer', 'name', 'bday', 'sex', )
	search_fields = ['id', 'id1c', 'name', 'buyer__id1c', ]
admin.site.register(child, ChildAdmin)


class buyerrelAdmin(admin.ModelAdmin):
	list_display = ('id', 'id1c', 'type', 'i', 'o', )
	search_fields = ['id', 'id1c', 'i', 'o', ]
admin.site.register(buyerrel, buyerrelAdmin)


class PAdmin(admin.ModelAdmin):
	list_display = ('id', 'idbitrix', 'status', 'code', 'name', 'baseunit', 'multiple', )
admin.site.register(properties, PAdmin)

class PvAdmin(admin.ModelAdmin):
	list_display = ('id', 'goods', 'properties', 'value', )
admin.site.register(propertiesvalue, PvAdmin)






class CheckAdmin(admin.ModelAdmin):
	list_display = ('id', 'id1c', 'nckkm', 'ctime', 'time', 'process', 'methodadd', 'status', 'operation', 'seller', 'buyer', 'nal', 'beznal', 'bonuspay', 'bonusadd', 'discountcard',)
	
	search_fields = ['id', 'id1c', 'nckkm', 'seller', ]
	list_filter = ('process', 'methodadd', 'shop', 'cashbox',)
	
admin.site.register(check, CheckAdmin)



class CheckitemAdmin(admin.ModelAdmin):
	list_display = ('id', 'fcheck', 'goods', 'col', 'price', 'sum', )
	
	search_fields = ['id', 'fcheck__id', 'fcheck__nckkm',]

	
admin.site.register(checkitem, CheckitemAdmin)


class CheckdAdmin(admin.ModelAdmin):
	list_display = ('id', 'checkitem', 'discount', 'descdiscount', )
	list_filter = ('discounts',)
	search_fields = ['id', 'checkitem__fcheck__id', 'checkitem__fcheck__nckkm',]
admin.site.register(checkd, CheckdAdmin)



class DiscountAdmin(admin.ModelAdmin):
	list_display = ('id', 'id1c', 'status', 'name', )
	search_fields = ['id', 'id1c', 'name',]
admin.site.register(discounts, DiscountAdmin)



class buyereventAdmin(admin.ModelAdmin):
	list_display = ('id', 'buyer', 'stime', 'name', 'comment', )
	list_filter = ('type', )
admin.site.register(buyerevent, buyereventAdmin)


class organizationAdmin(admin.ModelAdmin):
	list_display = ('id', 'id1c', 'status', 'name', )
admin.site.register(organization, organizationAdmin)

class kontragentAdmin(admin.ModelAdmin):
	list_display = ('id', 'id1c', 'status', 'name', )
admin.site.register(kontragent, kontragentAdmin)

class hozoperationAdmin(admin.ModelAdmin):
	list_display = ('id', 'id1c', 'name', 'code', )
admin.site.register(hozoperation, hozoperationAdmin)


class movegoodsAdmin(admin.ModelAdmin):
	list_display = ('id', 'id1c', 'ctime', 'hozoperation')
admin.site.register(movegoods, movegoodsAdmin)



class barcodelistAdmin(admin.ModelAdmin):
	list_display = ('id', 'goods', 'discountcard', 'barcode', 'unit', 'typebar', 'typebarcode', 'typewho',)
	search_fields = ['id', 'barcode', ]
admin.site.register(barcodelist, barcodelistAdmin)


class goodscertAdmin(admin.ModelAdmin):
	list_display = ('id', 'name',)
admin.site.register(goodscert, goodscertAdmin)

class discountcard1Admin(admin.ModelAdmin):
	list_display = ('id', 'id1c', 'name', 'buyer', 'bonus')
	search_fields = ['id', 'id1c', 'name', 'buyer__id1c', 'buyer__phone', 'buyer__f', 'buyer__i', 'buyer__o']
admin.site.register(discountcard1, discountcard1Admin)



class discountcardAdmin(admin.ModelAdmin):
	list_display = ('id', 'id1c', 'name', 'buyer', 'bonus')
	search_fields = ['id', 'id1c', 'name', 'buyer__id1c', 'buyer__phone', 'buyer__f', 'buyer__i', 'buyer__o']
admin.site.register(discountcard, discountcardAdmin)

class baseunitdAdmin(admin.ModelAdmin):
	list_display = ('id', 'id1c', 'status', 'value', 'goods')
	search_fields = ['id', 'id1c', 'goods__id1c']
	list_filter = ('value', )
admin.site.register(baseunit, baseunitdAdmin)


class pricetypeAdmin(admin.ModelAdmin):
	list_display = ('id', 'id1c', 'name', 'base', )
	
admin.site.register(pricetype, pricetypeAdmin)



class pricegoodsAdmin(admin.ModelAdmin):
	list_display = ('id', 'price', 'goods')
	
admin.site.register(pricegoods, pricegoodsAdmin)


class relgoodsAdmin(admin.ModelAdmin):
	list_display = ('id', 'a', 'b')
admin.site.register(relgoods, relgoodsAdmin)

class goodsmotivationratiosumAdmin(admin.ModelAdmin):
	list_display = ('id', 'id1c', 'name', 'ratio', 'sum', 'dsum',)
admin.site.register(goodsmotivationratiosum, goodsmotivationratiosumAdmin)
