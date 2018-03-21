# -*- coding: utf-8 -*-
from django.db import models

from PIL import Image
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit, SmartResize, Transpose, Adjust
from django.db.models.signals import post_delete, post_save, pre_save, pre_delete
from django.dispatch import receiver

from dj.views import make_upload_path
from dj.views import id_generator

from django.utils.safestring import mark_safe

from django.utils import timezone

from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User, Group

import re

from node.templatetags.nodetag import *



class base1c(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	status = models.BooleanField(verbose_name='Статус', default=True) 
	name = models.CharField(verbose_name=u'Название', help_text='Название', max_length=200)
	namefull = models.CharField(verbose_name=u'Название полное', help_text='Название полное', max_length=400, blank=True)
	
	def __str__(self):
		return u'%s %s' % (self.id, self.name)

	class Meta:
		ordering=['-id']
		verbose_name = u'База 1с'
		verbose_name_plural = u'База 1с'

		

class pricetype(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	base = models.ForeignKey(base1c, on_delete=models.CASCADE, null=True, blank=True)
	status = models.BooleanField(verbose_name='Статус', default=True) 
	id1c = models.CharField(verbose_name='id 1c', max_length=50, unique=True)
	name = models.CharField(verbose_name=u'Наименование', help_text='Наименование', max_length=200, blank=True)
	namefull = models.CharField(verbose_name=u'Представление',  max_length=500, blank=True)

	def __str__(self):
		return u'%s %s' % (self.id, self.name)

	class Meta:
		ordering=['-id']
		verbose_name = u'Тип цен'
		verbose_name_plural = u'Тип цен'		
	
	
	
class kontragent(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	status = models.BooleanField(verbose_name='Статус', default=True) 
	id1c = models.CharField(verbose_name='id 1c', max_length=50)
	#
	name = models.CharField(verbose_name=u'Наименование', help_text='Наименование', max_length=200, blank=True)
	namefull = models.CharField(verbose_name=u'НаименованиеПолное',  max_length=500, blank=True)
	
	inn = models.CharField(verbose_name=u'ИНН',  max_length=500, blank=True)
	kpp = models.CharField(verbose_name=u'КПП',  max_length=500, blank=True)
	kodpookpo = models.CharField(verbose_name=u'КодПоОКПО',  max_length=500, blank=True)
	urfizlico = models.CharField(verbose_name=u'ЮрФизЛицо',  max_length=500, blank=True)
	bankrek = models.CharField(verbose_name=u'БанковскиеРеквизиты',  max_length=500, blank=True)
	gpskod = models.CharField(verbose_name=u'ГруппаПолучателейСкидкиКод',  max_length=500, blank=True)
	stbank= models.CharField(verbose_name=u'стБанк',  max_length=500, blank=True)
	stbik = models.CharField(verbose_name=u'стБИК',  max_length=500, blank=True)
	stks = models.CharField(verbose_name=u'стКС',  max_length=500, blank=True)
	strs = models.CharField(verbose_name=u'стРС',  max_length=500, blank=True)
	pred = models.CharField(verbose_name=u'Представление',  max_length=500, blank=True)
	comment = models.CharField(verbose_name=u'Комментарий',  max_length=500, blank=True)


	def __str__(self):
		return u'%s %s' % (self.id, self.name)

	class Meta:
		ordering=['-id']
		verbose_name = u'Контрагент'
		verbose_name_plural = u'Контрагенты'	
	
	
	
	
	
	
	
	
class organization(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	status = models.BooleanField(verbose_name='Статус', default=True) 
	id1c = models.CharField(verbose_name='id 1c', max_length=50)
	name = models.CharField(verbose_name=u'Наименование', help_text='Наименование', max_length=200, blank=True)
	namefull = models.CharField(verbose_name=u'НаименованиеПолное',  max_length=500, blank=True)
	nameshort = models.CharField(verbose_name=u'НаименованиеСокращенное',  max_length=500, blank=True)
	inn = models.CharField(verbose_name=u'ИНН',  max_length=500, blank=True)

	def __str__(self):
		return u'%s %s' % (self.id, self.name)

	class Meta:
		ordering=['-id']
		verbose_name = u'Организация'
		verbose_name_plural = u'Организация'	

################################################################
################################################################
##merge models shop and stock to single model shopstock

class shopstock(models.Model): #merge models shop and stock to single model shopstock
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	status = models.BooleanField(verbose_name='Статус', default=True) 
	id1c = models.CharField(verbose_name='id 1c', max_length=50)
	name = models.CharField(verbose_name='Название', max_length=200)
	type = models.CharField(verbose_name='Тип', max_length=200, choices=(('shop', 'Магазин'), ('stock', 'Склад'),), default='shop')
	# #shop
	htmlcolor = models.CharField(verbose_name='Цвет', max_length=50, default='red')
	sort = models.PositiveIntegerField(verbose_name='Сортировка', default=0)
	#расчет мотивации, не имеет отншение к выгрузке
	motivationratio = models.FloatField(verbose_name='Коэффициент мотивация', default=0)
	#stock
	base = models.ForeignKey(base1c, on_delete=models.CASCADE, null=True, blank=True)
	idbitrix = models.CharField(verbose_name='id bitrix', help_text=u'Не забываем добавить новый склад на сайте в Битрикс', max_length=200, blank=True)
	typestock = models.CharField(verbose_name='ТипСклада', max_length=500, blank=True)
	organization = models.ForeignKey(organization, on_delete=models.CASCADE, null=True, blank=True)
	shop = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Магазин', null=True, blank=True)
	desc = models.TextField(verbose_name='Полезная информация', max_length=10000, blank=True)
	#
	
	def __str__(self):
		return u'%s %s %s -> %s' % (self.id, self.id1c, self.get_type_display(), self.name)

	class Meta:
		ordering=['-sort']
		verbose_name = u'Магазин/Склад'
		verbose_name_plural = u'Магазин/Склад'


class shop(models.Model): #merge models shop and stock to single model shopstock
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	status = models.BooleanField(verbose_name='Статус', default=True) 
	id1c = models.CharField(verbose_name='id 1c', max_length=50)
	name = models.CharField(verbose_name=u'Название', help_text='Название магазина', max_length=200)
	htmlcolor = models.CharField(verbose_name='Цвет', max_length=50, default='red')
	sort = models.PositiveIntegerField(verbose_name='Сортировка', default=0)
	#расчет мотивации, не имеет отншение к выгрузке
	motivationratio = models.FloatField(verbose_name='Коэффициент мотивация', default=0)
	
	
	def __str__(self):
		return u'%s %s' % (self.id, self.name)

	class Meta:
		ordering=['-sort']
		verbose_name = u'Магазин'
		verbose_name_plural = u'Магазины'
		

#склады
class stock(models.Model):  #merge models shop and stock to single model shopstock
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	base = models.ForeignKey(base1c, on_delete=models.CASCADE, null=True, blank=True)
	status = models.BooleanField(verbose_name='Статус', default=False) 
	idbitrix = models.CharField(verbose_name='id bitrix', help_text=u'Не забываем добавить новый склад на сайте в Битрикс', max_length=200, blank=True)
	id1c = models.CharField(verbose_name='id 1c', max_length=200)
	name = models.CharField(verbose_name='Название', max_length=200)
	typestock = models.CharField(verbose_name='ТипСклада', max_length=500, blank=True)
	organization = models.ForeignKey(organization, on_delete=models.CASCADE, null=True, blank=True)
	shop = models.ForeignKey(shop, on_delete=models.CASCADE, verbose_name=u'Магазин', null=True, blank=True)
	desc = models.TextField(verbose_name='Полезная информация', max_length=10000, blank=True)
	
	def __str__(self):
		return '%s %s' % (self.id, self.name)

	class Meta:
		ordering=['id']
		verbose_name = u'Склад'
		verbose_name_plural = u'Склады'

#############################################################################
#############################################################################
#############################################################################		
#количество товара на складе
class qinstock(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	stock = models.ForeignKey(stock, on_delete=models.CASCADE, verbose_name='Склад')
	value = models.PositiveIntegerField(verbose_name='Количество', default=0,)
	
	def __str__(self):
		return '%s=%s' % (self.stock.name, self.value)

	class Meta:
		ordering=['id']
		verbose_name = u'Количество на складе'
		verbose_name_plural = u'Количество на складе'		
		

class cashbox(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	status = models.BooleanField(verbose_name='Статус', default=True) 
	id1c = models.CharField(verbose_name='id 1c', max_length=50)
	name = models.CharField(verbose_name=u'Наименование', help_text='Наименование', max_length=200)
	shop = models.ForeignKey(shop, on_delete=models.CASCADE, verbose_name='МагазинКод', null=True, blank=True)
	organization = models.ForeignKey(organization, on_delete=models.CASCADE, null=True, blank=True)
	typecashbox = models.CharField(verbose_name=u'Тип кассы', help_text='Тип кассы', max_length=200, default=u'Контрольно кассовая машина')

	def __str__(self):
		return u'%s %s' % (self.id, self.name)

	class Meta:
		ordering=['-id']
		verbose_name = u'Касса'
		verbose_name_plural = u'Кассы'
		
		

#хозяйственные операции
class hozoperation(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	status = models.BooleanField(verbose_name='Статус', default=True) 
	id1c = models.CharField(verbose_name='id 1c', max_length=200)
	name = models.CharField(verbose_name='Название', max_length=200)
	code = models.CharField(verbose_name='КодХозяйственнойОперации', max_length=500, blank=True)
	pred = models.CharField(verbose_name='Представление', max_length=500, blank=True)
	
	def __str__(self):
		return '%s %s' % (self.id, self.name)

	class Meta:
		ordering=['id']
		verbose_name = u'Хозяйственные операции'
		verbose_name_plural = u'Хозяйственные операции'		
		
	




####################################
#**************ТОВАРЫ**************#
####################################
	
#Сертификаты
def make_upload_cert(instance, filename):
	#print instance._get_FIELD_display
	#print dir(instance.__class__)
	category = instance.__class__.__name__ #имя модели, каталог категория
	fieldname = 'pdf' #имя поля модели, каталог подкатегория
	fileext = re.compile(r'^.*\.(?P<ext>\w+)$').match(filename).group('ext')
	filename = id_generator()
	return u"uploads/%s_%s/%s" % (category, fieldname, '%s.%s' % (filename, fileext))	

class goodscert(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	name = models.CharField(verbose_name='Номер', max_length=200)
	datestart = models.DateField(verbose_name='Дата выдачи', default=timezone.now)
	dateend = models.DateField(verbose_name='Дата окончания', default=timezone.now)
	org = models.TextField(verbose_name='Орган выдачи', max_length=30000)
	pdf = models.FileField(verbose_name=u'Файл сертификата', upload_to=make_upload_cert, max_length=500)
	
	def __str__(self):
		return u'%s %s' % (self.id, self.name)

	class Meta:
		ordering=['-id']
		verbose_name = u'Сертификат'
		verbose_name_plural = u'Сертификаты'
#end_cert	


class tax(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	id1c = models.CharField(verbose_name='id 1c', max_length=50, blank=True)
	idbitrix = models.CharField(verbose_name='id битрикс', max_length=50, blank=True)
	status = models.BooleanField(verbose_name='Статус', default=True)
	parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Родитель', limit_choices_to={'parent__isnull': True, }, blank=True, null=True)
	name = models.CharField(verbose_name=u'Название', help_text='Название товара', max_length=200)
	pict = models.ImageField(verbose_name=u'Картинка', upload_to=make_upload_path, max_length=300, blank=True)
	pict1 = ImageSpecField(source='pict', processors=[ResizeToFill(230, 200)], format='PNG', options={'quality': 75})

	def __str__(self):
		if self.parent:
			return u'%s -> %s' % (self.parent, self.name)
		else:
			return u'%s' % (self.name)

	class Meta:
		ordering=['id']
		verbose_name = u'Категория'
		verbose_name_plural = u'Категории'
	
def delete_tax_pict(sender, **kwargs):
	mf = kwargs.get("instance")
	mf.pict.delete(save=False)
	
post_delete.connect(delete_tax_pict, tax)
	

class goodsmotivationratiosum(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	id1c = models.CharField(verbose_name='id 1c', max_length=50, blank=True)
	name = models.CharField(verbose_name='Название', max_length=300, blank=True) 
	ratio = models.PositiveIntegerField(verbose_name='Категория', default=0)
	sum = models.FloatField(verbose_name='+Сумма', default=0)
	dsum = models.FloatField(verbose_name='-Сумма', default=0)
	percent = models.FloatField(verbose_name='+%', default=0)
	dpercent = models.FloatField(verbose_name='-%', default=0)

	def __str__(self):
		return '%s (%s)' % (self.name, self.ratio)

	class Meta:
		ordering=['id']
		verbose_name = u'Мотивация=сумма (основная)'
		verbose_name_plural = u'Мотивация=сумма (основная)'

		
class goods(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	base = models.ForeignKey(base1c, on_delete=models.CASCADE, null=True, blank=True)
	id1c = models.CharField(verbose_name='id 1c', max_length=200)
	idbitrix = models.CharField(verbose_name='id битрикс', max_length=50, blank=True)
	utime = models.DateTimeField(verbose_name='Время последнего обновления', auto_now=True)
	status = models.BooleanField(verbose_name='Статус', default=True) 
	name = models.CharField(verbose_name=u'Название', help_text='Название товара', max_length=200, null=True, blank=True)
	namefull = models.CharField(verbose_name=u'Название полное', help_text='Название товара полное', max_length=400, null=True, blank=True)
	art = models.CharField(verbose_name=u'Артикул', help_text='Артикул товара', max_length=200, null=True, blank=True)
	desc = models.TextField(verbose_name=u'Описание', help_text=u'Описание товара', max_length=30000, blank=True)
	madein = models.CharField(verbose_name=u'СтранаПроисхождения', max_length=200, blank=True)
	desc = models.TextField(verbose_name=u'Описание', help_text=u'Описание товара', max_length=30000, blank=True)
	datelife = models.DateField(verbose_name='СрокГодности', null=True, blank=True)
	#количество на складе
	qinstock = models.ManyToManyField(qinstock, verbose_name='Количество на складе', blank=True)
	#цена
	price = models.FloatField(verbose_name='Цена', default=0)
	startprice = models.FloatField(verbose_name='Закупочная Цена', default=0)
	manualstartprice = models.FloatField(verbose_name='Оптовая Цена (Забитая вручную)', default=0)
	#
	catalogshow = models.BooleanField(verbose_name='Отображать в каталоге', default=False)
	showondemo = models.BooleanField(verbose_name='Показывать в демо', default=False)
	touchscreen = models.BooleanField(verbose_name='Отображать на тачскринах', default=False)
	video = models.CharField(verbose_name=u'Видео', max_length=400, blank=True)
	videomp4 = models.CharField(verbose_name=u'Видео MP4', max_length=400, blank=True)
	#videomp42 = models.CharField(verbose_name=u'Видео MP4 (версия 2)', max_length=400, blank=True)
	#
	tax = models.ManyToManyField(tax, verbose_name='Категория', blank=True)
	#propertiesvalue = models.ManyToManyField(propertiesvalue, verbose_name='Свойства', blank=True)
	#Основные свойства из битрикс
	bname = models.CharField(verbose_name=u'Битрикс Название', help_text='Название товара в битриксе', max_length=200, blank=True)
	pricenameprefix = models.CharField(verbose_name=u'Название префикс для ценника', max_length=200, blank=True)
	pricename = models.CharField(verbose_name=u'Название для ценника', max_length=200, blank=True)
	#набор или нет
	nabor = models.BooleanField(verbose_name='Набор', default=False)
	naborparent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Входит в товар (набор)', limit_choices_to={'idbitrix__isnull': False, 'status': True, 'nabor': True,}, blank=True, null=True)
	#
	pict = models.ImageField(verbose_name=u'Картинка', upload_to=make_upload_path, max_length=500, blank=True)
	pict20 = ImageSpecField(source='pict', processors=[ResizeToFit(20, 20)], format='PNG', options={'quality': 95})
	pict40 = ImageSpecField(source='pict', processors=[ResizeToFit(40, 40)], format='PNG', options={'quality': 95})
	pict60 = ImageSpecField(source='pict', processors=[ResizeToFit(60, 60)], format='PNG', options={'quality': 95})
	pict80 = ImageSpecField(source='pict', processors=[ResizeToFit(80, 80)], format='PNG', options={'quality': 95})
	pict120 = ImageSpecField(source='pict', processors=[ResizeToFit(120, 120)], format='PNG', options={'quality': 95})
	pict160 = ImageSpecField(source='pict', processors=[ResizeToFit(160, 160)], format='PNG', options={'quality': 95})
	pict180 = ImageSpecField(source='pict', processors=[ResizeToFit(180, 180)], format='PNG', options={'quality': 95})
	pict200 = ImageSpecField(source='pict', processors=[ResizeToFit(200, 200)], format='PNG', options={'quality': 95})
	pict500 = ImageSpecField(source='pict', processors=[ResizeToFit(500, 500)], format='PNG', options={'quality': 95})
	pict640 = ImageSpecField(source='pict', processors=[ResizeToFit(640, 640)], format='PNG', options={'quality': 95})
	#dev
	pictdevlist = ImageSpecField(source='pict', processors=[ResizeToFill(180, 180)], format='PNG', options={'quality': 95})
	#qrcode
	qrcode = models.ImageField(verbose_name=u'QRCode', upload_to=u"uploads/qrcode/", max_length=500, blank=True)
	qrcode40 = ImageSpecField(source='qrcode', processors=[ResizeToFit(40, 40)], format='PNG', options={'quality': 95})
	qrcode100 = ImageSpecField(source='qrcode', processors=[ResizeToFit(100, 100)], format='PNG', options={'quality': 95})
	qrcode500 = ImageSpecField(source='qrcode', processors=[ResizeToFit(500, 500)], format='PNG', options={'quality': 95})

	#свойства для сортировки
	propa = models.PositiveIntegerField(verbose_name=u'Количество разрывов', default=0)
	propb = models.PositiveIntegerField(verbose_name=u'Продолжительность', default=0)
	#propc = models.FloatField(verbose_name=u'Калибр изделия', default=0)

	goodscert = models.ForeignKey(goodscert, on_delete=models.CASCADE, verbose_name='Сертификат', null=True, blank=True)
	
	#количество показов видео на планшетах и тачскринах
	showvideocount = models.PositiveIntegerField(verbose_name='Количество показов видео', default=0)
	
	motivationinpoints1 = models.ForeignKey(goodsmotivationratiosum, on_delete=models.CASCADE, related_name='motivationinpoints1', verbose_name='Мотивация в баллах', default=1)
	
	def __str__(self):
		return u'%s %s %s %s %s (%s)' % (self.id, self.art, self.id1c, self.idbitrix, self.name, self.base.name)
		#return u'%s' % (self.id)

	class Meta:
		ordering=['-id']
		verbose_name = u'Товар'
		verbose_name_plural = u'Товары'

			
def delete_goods_pict(sender, **kwargs):
	mf = kwargs.get("instance")
	mf.pict.delete(save=False)
	mf.qrcode.delete(save=False)
	
post_delete.connect(delete_goods_pict, goods)



#количество товара на складе
class goodsinstock(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	goods = models.ForeignKey(goods, on_delete=models.CASCADE, verbose_name='Товар')
	stock = models.ForeignKey(stock, on_delete=models.CASCADE, verbose_name='Склад')
	value = models.PositiveIntegerField(verbose_name='Количество', default=0,)
	
	def __str__(self):
		return '%s=%s' % (self.stock.name, self.value)

	class Meta:
		ordering=['id']
		verbose_name = u'Количество на складе (goodsinstock)'
		verbose_name_plural = u'Количество на складе (goodsinstock)'	


#conversation
class relgoods(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	a = models.ForeignKey(goods, on_delete=models.CASCADE, related_name='a', verbose_name='Товар A')
	b = models.ForeignKey(goods, on_delete=models.CASCADE, related_name='b', verbose_name='Товар B')

	def __str__(self):
		return u'%s' % (self.id)

	class Meta:
		ordering=['-id']
		verbose_name = u'conversation'
		verbose_name_plural = u'conversation'	


class pricegoods(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	goods = models.ForeignKey(goods, on_delete=models.CASCADE, verbose_name='Товар')
	price = models.FloatField(verbose_name='Цена', default=0)
	unit = models.CharField(verbose_name='ЕдиницаИзмерения', max_length=200, blank=True)
	pricetype = models.ForeignKey(pricetype, on_delete=models.CASCADE, verbose_name='ТипЦенКод')

	def __str__(self):
		return u'%s' % (self.id)

	class Meta:
		ordering=['-id']
		verbose_name = u'Цена (Товар)'
		verbose_name_plural = u'Цена (Товар)'	





class baseunit(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	status = models.BooleanField(verbose_name='Статус', default=True)
	id1c = models.CharField(verbose_name='id 1c', max_length=50, unique=True)
	value = models.CharField(verbose_name='Значение', max_length=200)
	goods = models.ForeignKey(goods, on_delete=models.CASCADE, verbose_name='Товар')
	factor = models.PositiveIntegerField(verbose_name='Коэффициент', default=1)
	

	def __str__(self):
		return u'%s %s %s' % (self.id, self.status, self.id1c)

	class Meta:
		ordering=['-id']
		verbose_name = u'Единицы измерения'
		verbose_name_plural = u'Единица измерения'
		
		

class properties(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	status = models.BooleanField(verbose_name='Статус', default=False) 
	idbitrix = models.CharField(verbose_name='id битрикс', max_length=50)
	code = models.CharField(verbose_name=u'Код свойства', max_length=200, blank=True)
	name = models.CharField(verbose_name=u'Название свойства', max_length=200)
	baseunit = models.CharField(verbose_name='Единица измерения', max_length=80, choices=((u'шт', u'шт'), (u'м', u'м'), (u'сек', u'сек'), (u' "', u' "')), blank=True)
	multiple = models.BooleanField(verbose_name='Множественное', default=False)

	def __str__(self):
		return u'%s %s %s' % (self.id, self.status, self.name)

	class Meta:
		ordering=['-id']
		verbose_name = u'Свойство'
		verbose_name_plural = u'Свойства'
		

# class propfilter(models.Manager):
    # def get_queryset(self):
        # return super(propfilter, self).get_queryset().filter(properties__status=True)
	
		
class propertiesvalue(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	goods = models.ForeignKey(goods, on_delete=models.CASCADE, verbose_name='Товар')
	properties = models.ForeignKey(properties, on_delete=models.CASCADE, verbose_name='Свойство')
	value = models.CharField(verbose_name=u'Значение свойства', max_length=200)
	#manager
	#pfilter = propfilter()
	
	def __str__(self):
		return u'%s %s' % (self.id, self.value)

	class Meta:
		ordering=['-id']
		verbose_name = u'Значение свойства'
		verbose_name_plural = u'Значение свойств'

#Анкеты
def make_upload_anketa(instance, filename):
	#print instance._get_FIELD_display
	#print dir(instance.__class__)
	category = instance.__class__.__name__ #имя модели, каталог категория
	fieldname = 'anketa' #имя поля модели, каталог подкатегория
	fileext = re.compile(r'^.*\.(?P<ext>\w+)$').match(filename).group('ext')
	filename = id_generator()
	return u"uploads/%s_%s/%s" % (category, fieldname, '%s.%s' % (filename, fileext))	


class buyer(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	status = models.BooleanField(verbose_name='Статус', default=True) 
	id1c = models.CharField(verbose_name='id 1c', max_length=50, unique=True)
	f = models.CharField(verbose_name=u'Фамилия', max_length=200, blank=True)
	i = models.CharField(verbose_name=u'Имя', max_length=200, blank=True)
	o = models.CharField(verbose_name=u'Отчество', max_length=200, blank=True)
	bday = models.DateField(verbose_name='Дата Рождения', blank=True, null=True,)
	sex = models.CharField(verbose_name='Пол', max_length=80, choices=(('male', u'Мужской'), ('female', u'Женский')), default='male')
	phone = models.CharField(verbose_name=u'Телефон', max_length=20, blank=True)
	#денормализация + индексы
	bdayindex = models.CharField(verbose_name='Дата Рождения индекс', max_length=20, blank=True, db_index=True)
	bonus = models.FloatField(verbose_name='РазмерБонусаОстаток', default=0) #УДАЛИТЬ
	
	#согласие на рассылку
	adv = models.BooleanField(verbose_name='Согласие на рассылку', default=False)
	anketa = models.FileField(verbose_name='Анкета', upload_to=make_upload_anketa, max_length=500, null=True, blank=True)
	
	#auth
	authsmstime = models.DateTimeField(verbose_name='Время последней отправки смс', auto_now=True)
	authcode = models.CharField(verbose_name=u'Проверочный код', max_length=100, blank=True)
	authtoken = models.CharField(verbose_name=u'Авторизационный токен', max_length=100, blank=True)
	
	#log 1с
	ctime = models.DateTimeField(verbose_name='Время создания', auto_now_add=True, null=True)
	lastmodtime = models.DateTimeField(verbose_name='Время модификации', auto_now=True, null=True)
	creator = models.CharField(verbose_name='Ответственный код', max_length=100, blank=True)
	lastmod = models.CharField(verbose_name='Последний редактор код', max_length=100, blank=True)

	
	
	@property
	def gethidephone(self):
		return hidephone(self.phone)
	
	
	def __str__(self):
		return u'%s %s %s %s %s' % (self.id, self.id1c, self.f, self.i, self.o)

	class Meta:
		ordering=['-id']
		verbose_name = u'Покупатель'
		verbose_name_plural = u'Покупатели'
	
@receiver(post_save, sender = buyer)
def buyerbdayindexsave(instance, **kwargs):
	try:
		buyer.objects.filter(id=instance.id).update(bdayindex=instance.bday.strftime("%d%m"))
	except:
		buyer.objects.filter(id=instance.id).update(bdayindex='none')
##################


#Дисконтные карты
class discountcard1(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	status = models.BooleanField(verbose_name='Статус', default=True) 
	id1c = models.CharField(verbose_name='id 1c', max_length=50)
	name = models.CharField(verbose_name='Имя', max_length=200)
	buyer = models.ForeignKey(buyer, on_delete=models.CASCADE, verbose_name='Родитель')
	bonus = models.FloatField(verbose_name='РазмерБонусаОстаток', default=0)

	def __str__(self):
		return u'%s %s %s' % (self.id, self.id1c, self.name)

	class Meta:
		ordering=['-buyer']
		verbose_name = u'Дисконтная карта 1'
		verbose_name_plural = u'Дисконтные карты 1'




#Дисконтные карты
class discountcard(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	status = models.BooleanField(verbose_name='Статус', default=True) 
	id1c = models.CharField(verbose_name='id 1c', max_length=50)
	name = models.CharField(verbose_name='Имя', max_length=200, unique=True)
	buyer = models.ForeignKey(buyer, on_delete=models.CASCADE, verbose_name='Родитель')
	bonus = models.FloatField(verbose_name='РазмерБонусаОстаток', default=0)

	def __str__(self):
		return u'%s %s %s' % (self.id, self.id1c, self.name)

	class Meta:
		ordering=['-buyer']
		verbose_name = u'Дисконтная карта'
		verbose_name_plural = u'Дисконтные карты'


#############
class child(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	buyer = models.ForeignKey(buyer, on_delete=models.CASCADE, verbose_name='Родитель')
	status = models.BooleanField(verbose_name='Статус', default=True) 
	id1c = models.CharField(verbose_name='id 1c', max_length=50, blank=True)
	name = models.CharField(verbose_name=u'Имя', max_length=200)
	bday = models.DateField(verbose_name=u'Дата Рождения', null=True, blank=True)
	#female = models.BooleanField(verbose_name='Женский пол', default=False)
	sex = models.CharField(verbose_name='Пол', max_length=80, choices=(('male', u'Мужской'), ('female', u'Женский')), default='male')
	#денормализация + индексы
	bdayindex = models.CharField(verbose_name=u'Дата Рождения индекс', max_length=20, blank=True)

	def __str__(self):
		return u'%s %s %s %s' % (self.id, self.id1c, self.name, self.bday)

	class Meta:
		ordering=['-buyer']
		verbose_name = u'Ребенок'
		verbose_name_plural = u'Дети'


@receiver(post_save, sender = child)
def childbdayindexsave(instance, **kwargs):
	try:
		child.objects.filter(id=instance.id).update(bdayindex=instance.bday.strftime("%d%m"))
	except:
		child.objects.filter(id=instance.id).update(bdayindex='none')

###########



#Событие клиента, напоминания о событиях
beventtypechoice=[('event', 'Событие'), ('m', 'Мать'), ('f', 'Отец'), ('b', 'Брат'), ('s', 'Сестра'), ('1c', '1с - День рождения БР')]
class buyerevent(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	#id1c = models.CharField(verbose_name='id 1c', max_length=50, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Менеджер', blank=True, null=True)
	ctime = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
	buyer = models.ForeignKey(buyer, on_delete=models.CASCADE, verbose_name='Покупатель')
	stime = models.DateField(verbose_name='Дата/Время', blank=True, null=True)
	type = models.CharField(verbose_name='Тип', max_length=200, choices=beventtypechoice, default='event')
	
	name = models.CharField(verbose_name=u'Название', max_length=500)
	comment = models.TextField(verbose_name='Комментарий', max_length=30000)
	#денормализация + индексы
	stimeindex = models.CharField(verbose_name='Дата индекс', max_length=20,  blank=True)
	
	def __str__(self):
		return '%s %s' % (self.id, self.name)

	class Meta:
		ordering=['id']
		verbose_name = u'События клиента'
		verbose_name_plural = u'События клиента'

@receiver(post_save, sender = buyerevent)
def buyereventstimeindexsave(instance, **kwargs):
	try:
		buyerevent.objects.filter(id=instance.id).update(stimeindex=instance.stime.strftime("%d%m"))
	except:
		buyerevent.objects.filter(id=instance.id).update(stimeindex='none')
###################3
	

	
	
#Событие клиента по новому из форм 1c
buyerrelchoice=[
	('son', 'Сын'),
	('d', 'Дочь'),
	('f', 'Отец'),
	('m', 'Мать'),
	('sis', 'Сестра'),
	('b', 'Брат'),
	('other', 'Близкий Родственник'),
	]


class buyerrel(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	id1c = models.CharField(verbose_name='id 1c', max_length=50)
	ctime = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
	buyer = models.ForeignKey(buyer, on_delete=models.CASCADE, verbose_name='Покупатель')
	type = models.CharField(verbose_name='Степень родства', max_length=200, choices=buyerrelchoice)
	#f = models.CharField(verbose_name='Фамилия', max_length=200)
	i = models.CharField(verbose_name='Имя', max_length=200, blank=True)
	o = models.CharField(verbose_name='Отчество', max_length=200, blank=True)
	bday = models.DateField(verbose_name='Дата Рождения', null=True, blank=True)
	#денормализация + индексы
	bdayindex = models.CharField(verbose_name='Дата Рождения индекс', max_length=20, blank=True, db_index=True)
	
	#log 1с
	ctime = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
	lastmodtime = models.DateTimeField(verbose_name='Время модификации', auto_now=True)
	creator = models.CharField(verbose_name='Ответственный код', max_length=100, blank=True)
	lastmod = models.CharField(verbose_name='Последний редактор код', max_length=100, blank=True)

	def __str__(self):
		return '%s %s' % (self.id, self.id1c)

	class Meta:
		ordering=['id']
		verbose_name = u'Покупатель родственники'
		verbose_name_plural = u'Покупатель родственники'

@receiver(post_save, sender = buyerrel)
def defbuyerrelbdayindexsave(instance, **kwargs):
	try:
		buyerrel.objects.filter(id=instance.id).update(bdayindex=instance.bday.strftime("%d%m"))
	except:
		buyerrel.objects.filter(id=instance.id).update(bdayindex='none')
###################3
	
	
	

#barcode
class barcodelist(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	#id1c = models.CharField(verbose_name='id 1c', max_length=50, blank=True)
	goods = models.ForeignKey(goods, on_delete=models.CASCADE, verbose_name='Номенклатура', null=True, blank=True)
	discountcard = models.ForeignKey(discountcard, on_delete=models.CASCADE, verbose_name='Дисконтная карта', null=True, blank=True)
	barcode = models.CharField(verbose_name='Штрихкод', max_length=200, blank=True)
	unit = models.CharField(verbose_name='ЕдиницаИзмерения', max_length=400, blank=True)
	typebar = models.CharField(verbose_name='ТипШтрихкода', max_length=200, blank=True)
	typebarcode = models.CharField(verbose_name='ТипШтрихкодаКод', max_length=200, blank=True)
	typewho = models.CharField(verbose_name='ТипВладельца', max_length=200, blank=True)
	
	def __str__(self):
		return u'%s %s %s' % (self.id, self.barcode, self.unit,)

	class Meta:
		ordering=['-id']
		verbose_name = u'Штрих код'
		verbose_name_plural = u'Штрих код'
#end_barcode
	
	
	
		
#CHECK СКИДКИ
class discounts(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	status = models.BooleanField(verbose_name='Статус', default=True) 
	id1c = models.CharField(verbose_name='id 1c', max_length=50, blank=True)
	name = models.CharField(verbose_name=u'Название', help_text='Название скидки', max_length=500)
	
	def __str__(self):
		return u'%s' % (self.name)

	class Meta:
		ordering=['-id']
		verbose_name = u'Скидки'
		verbose_name_plural = u'Скидки'





operationchoice = (('sale', 'Продажа'), ('return', 'Возврат'),)

def make_upload_check(instance, filename):
	category = instance.__class__.__name__ #имя модели, каталог категория
	#filename = id_generator()
	return u"uploads/%s/%s" % (category, '%s.csv' % filename)		


class check(models.Model):
	lock = models.BooleanField(verbose_name='Замок', default=False)
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	uuid = models.CharField(verbose_name='uuid', max_length=300, blank=True)
	id1c = models.CharField(verbose_name='id 1c', max_length=300, blank=True)
	nckkm = models.CharField(verbose_name='Номер Чека ККМ', max_length=300, blank=True)
	ctime = models.DateTimeField(db_index=True, verbose_name='Время создания чека', auto_now_add=True)
	time = models.DateTimeField(db_index=True, verbose_name='Дата/Время', default=timezone.now)
	timeindex = models.CharField(verbose_name='Дата индекс', max_length=20, blank=True, db_index=True)
	shop = models.ForeignKey(shop, on_delete=models.CASCADE, verbose_name='Магазин', null=True, blank=True)
	cashbox = models.ForeignKey(cashbox, on_delete=models.CASCADE, verbose_name='Касса', null=True, blank=True)
	seller = models.CharField(verbose_name='Продавец', max_length=100, blank=True)
	#seller = models.ForeignKey(seller, verbose_name='Продавец', null=True, blank=True)
	buyer = models.ForeignKey(buyer, on_delete=models.CASCADE, verbose_name='Покупатель', null=True, blank=True)
	bonuswho = models.CharField(verbose_name='Владелец дисконтной карты код', max_length=100, blank=True)
	discountcard = models.CharField(verbose_name='Дисконтная карта', max_length=100, blank=True)
	otvetstven = models.CharField(verbose_name='Ответственный', max_length=100, blank=True)
	operation = models.CharField(verbose_name='Вид операции', max_length=80, choices=operationchoice, default='sale')
	status = models.CharField(verbose_name='Статус', max_length=100, blank=True)
	smena_kkm = models.CharField(verbose_name='Смена ККМ', max_length=100, blank=True)
	checkreturn = models.CharField(verbose_name='Возврат чека', max_length=100, blank=True) #номер чека который возвращается новым текущим чеком
	accept = models.BooleanField(verbose_name='Проведен', default=False)
	
	#оплата
	nal = models.FloatField(verbose_name='Оплата наличные', default=0)
	beznal = models.FloatField(verbose_name='Оплата без наличные', default=0)
	bonuspay = models.FloatField(verbose_name='Оплата бонусы', default=0)
	paygiftcert = models.FloatField(verbose_name='Оплата подарочным сертификатом', default=0)
	#bonuspay нужно убрать в будущем, при рефакторинге
	bonusadd = models.FloatField(verbose_name='Начисление бонусов', default=0)
	
	#оплата по новому
	paym1 = models.FloatField(verbose_name='Оплата наличные', default=0)
	paym2 = models.FloatField(verbose_name='Оплата без наличные', default=0)
	paym3 = models.FloatField(verbose_name='Оплата бонусными баллами', default=0)
	paym4 = models.FloatField(verbose_name='Оплата подарочным сертификатом', default=0)
	
	#лог
	#sourcefile = models.FileField(upload_to=make_upload_check, max_length=500, null=True, blank=True)
	fname = models.CharField(verbose_name='Н. Файла', max_length=200, blank=True)
	sourcejson = models.TextField(verbose_name='json из 1с', max_length=30000, blank=True)
	process = models.CharField(verbose_name='Процесс', max_length=80, choices=(('test', 'Тестовый чек'), ('invalid', 'Не валидный'), ('valid', 'Валидный'), ('copy', 'Копия') ), default='valid')
	methodadd = models.CharField(verbose_name='Откуда загружен', max_length=80, choices=(('csv', 'CSV'), ('jsonapi', 'JSON from API'), ('jsonfile', 'JSON from FILE'),), default='jsonapi')

	def __str__(self):
		return u'%s' % (self.id)

	class Meta:
		ordering=['-id']
		verbose_name = u'Чек'
		verbose_name_plural = u'Чеки'
		

@receiver(post_save, sender = check)
def timeindexsave(instance, **kwargs):
	try:
		check.objects.filter(id=instance.id).update(timeindex=instance.time.strftime("%d%m"))
	except:
		check.objects.filter(id=instance.id).update(timeindex='none')
##################
		

#позиция в чеке
class checkitem(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	fcheck = models.ForeignKey(check, on_delete=models.CASCADE, verbose_name='Чек', null=True, blank=True)
	goods = models.ForeignKey(goods, on_delete=models.CASCADE, db_index=True, verbose_name='Товар', null=True, blank=True)
	col = models.FloatField(verbose_name='Количество', default=0,)
	unit = models.ForeignKey(baseunit, on_delete=models.CASCADE, null=True, blank=True)
	price = models.FloatField(verbose_name='Цена', default=0)
	sum = models.FloatField(verbose_name='Сумма', default=0)
	totaldiscount = models.FloatField(verbose_name='totaldiscount', default=0)
	operation = models.CharField(verbose_name='Вид операции', max_length=80, choices=operationchoice, default='sale')
	
	
	def __str__(self):
		return u'%s' % (self.id)

	class Meta:
		ordering=['-id']
		verbose_name = u'Чек: позиция'
		verbose_name_plural = u'Чек: позиция'

		

#скидки в чеке
class checkd(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	checkitem = models.ForeignKey(checkitem, on_delete=models.CASCADE, verbose_name='Чек')
	discounts = models.ForeignKey(discounts, on_delete=models.CASCADE, verbose_name='Скидка', null=True, blank=True)
	discount = models.FloatField(verbose_name='Скидка', default=0)
	descdiscount = models.CharField(verbose_name='Описание скидки', max_length=300, blank=True)

	def __str__(self):
		return u'%s' % (self.id)

	class Meta:
		ordering=['-id']
		verbose_name = u'Чек: скидка'
		verbose_name_plural = u'Чек: скидка'




########ОПЕРАЦИИ ПЕРЕМЕЩЕНИЯ ТОВАРОВ, ОСТАТКИ, СКЛАДЫ########	
class movegoods(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	#status = models.BooleanField(verbose_name='Статус', default=True) 
	id1c = models.CharField(verbose_name='id 1c', max_length=50, blank=True)
	ctime = models.DateTimeField(verbose_name='Дата', auto_now_add=True)
	#
	atime = models.DateTimeField(verbose_name='Дата', null=True, blank=True)
	kontragent = models.ForeignKey(kontragent, on_delete=models.CASCADE, verbose_name='КонтрагентКод', null=True, blank=True)
	hozoperation = models.ForeignKey(hozoperation, on_delete=models.CASCADE, verbose_name='ХозяйственнаяОперацияКод', null=True, blank=True)
	fstock = models.ForeignKey(stock, related_name='fstock', on_delete=models.CASCADE, verbose_name='СкладКод', null=True, blank=True)
	#
	stockfrom = models.ForeignKey(stock, related_name='stockfrom', on_delete=models.CASCADE, verbose_name='СкладОтправительКод', null=True, blank=True)
	stockto = models.ForeignKey(stock, related_name='stockto', on_delete=models.CASCADE, verbose_name='СкладПолучательКод', null=True, blank=True)
	#
	unit = models.ForeignKey(baseunit, on_delete=models.CASCADE, verbose_name='ЕдиницаИзмерения', null=True, blank=True)
	fshop = models.ForeignKey(shop, related_name='fshop', on_delete=models.CASCADE, verbose_name='МагазинКод', null=True, blank=True)
	shopfrom = models.ForeignKey(shop, related_name='shopfrom', on_delete=models.CASCADE, verbose_name='МагазинОтправительКод', null=True, blank=True)
	shopto = models.ForeignKey(shop, related_name='shopto', on_delete=models.CASCADE, verbose_name='СкладПолучательКод', null=True, blank=True)
	goods = models.ForeignKey(goods, on_delete=models.CASCADE, verbose_name='НоменклатураКод')
	#
	fcheck = models.ForeignKey(check, on_delete=models.CASCADE, verbose_name='ЧекККМНомер', null=True, blank=True)
	#
	col = models.PositiveIntegerField(verbose_name='Количество', default=0)
	price = models.FloatField(verbose_name='Цена', default=0, blank=True)
	sum = models.FloatField(verbose_name='Сумма', default=0, blank=True)
	who = models.CharField(verbose_name=u'ОтветственныйКод', max_length=500, blank=True)
	comment = models.CharField(verbose_name=u'Комментарий', max_length=1000, blank=True)	
	carried = models.BooleanField(verbose_name=u'Проведен', default=False)

	def __str__(self):
		return '%s' % (self.id)

	class Meta:
		ordering=['id']
		verbose_name = u'Движение товара'
		verbose_name_plural = u'Движение товара'				
########КОНЕЦ ОПЕРАЦИИ ПЕРЕМЕЩЕНИЯ ТОВАРОВ, ОСТАТКИ, СКЛАДЫ########			

	
