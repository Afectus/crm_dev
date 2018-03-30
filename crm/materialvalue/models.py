#-*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from PIL import Image
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit, ResizeToFill, SmartResize, Transpose, Adjust
import string
import random
import re
from dj.views import *
from django.utils import timezone
from panel.models import profileuser
from node.models import shop, stock, shopstock

MLIST = (
	('inuse', 'Активен'),
	('decommissioned', 'Списан'),
	('notwork', 'Неисправен'),
)


CATEGORY = (
	('a', 'Печати и штампы'),
	('b', 'Кассовая техника'),
	('c', 'Мебель'),
	('d', 'Огнетушители'),
	('e', 'Бытовые принадлежности'),
	('f', 'Компьютеры и комплектующие'),
	('g', 'Мультимедия'),
	('h', 'Инструменты'),
	#('h', 'Инструменты'),
)


MOVETYPES = (
	('relocation', 'Перемещение'),
	('writeoff', 'Списание'),
)


def make_upload_mvfile(instance, filename):
	category = instance.__class__.__name__ #имя модели, каталог категория
	fileext = re.compile(r'^.*\.(?P<ext>\w+)$').match(filename).group('ext')
	filename = id_generator()
	return u"uploads/%s/%s" % (category, '%s.%s' % (filename, fileext))

class mvcontainer(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	name = models.CharField(verbose_name='Название контейнера', max_length=255)
	shopstock = models.ForeignKey(shopstock, verbose_name='Склад', on_delete=models.CASCADE, null=True, blank=True) 
	
	def __str__(self):
		return '%s %s (%s)' % (self.id, self.name, self.shopstock)

class mvcell(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	name = models.CharField(verbose_name='Название ячейки', max_length=255)
	container = models.ForeignKey(mvcontainer, on_delete=models.CASCADE)

	def __str__(self):
		return u'%s %s -> %s' % (self.id, self.container, self.name)

class materialvalue(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	category = models.CharField(verbose_name='Категория', max_length=300, choices=CATEGORY, default='e')
	barcode = models.CharField(verbose_name='Штрих-код', max_length=13, default='1111111111111')
	name = models.CharField(verbose_name='Название', max_length=255)
	model = models.CharField(verbose_name='Модель', max_length=255, blank=True)
	serial = models.CharField(verbose_name='Серийный номер', max_length=255, blank=True)
	pictdesc = models.ImageField(verbose_name='Фото наклейки/шильдика/штрихкода', upload_to=make_upload_path, max_length=500, blank=True, null=True)
	pictdesc200 = ImageSpecField(source='pictdesc', processors=[ResizeToFit(200, 200)], format='PNG', options={'quality': 95})
	photo = models.ImageField(verbose_name='Фото объекта', upload_to=make_upload_path, max_length=500, blank=True, null=True)
	photo200 = ImageSpecField(source='photo', processors=[ResizeToFit(200, 200)], format='PNG', options={'quality': 75})
	photo100 = ImageSpecField(source='photo', processors=[ResizeToFit(100, 100)], format='PNG', options={'quality': 75})
	photo500 = ImageSpecField(source='photo', processors=[ResizeToFit(500, 500)], format='PNG', options={'quality': 75})
	photo800 = ImageSpecField(source='photo', processors=[ResizeToFit(800, 800)], format='PNG', options={'quality': 75})
	status = models.CharField(verbose_name='Статус', max_length=30, choices=MLIST, default='inuse')
	amount = models.IntegerField(verbose_name='Количество', default=1)
	assessed_value = models.FloatField(verbose_name='Оценочная стоимость', default=0, blank=True, null=True)
	parent = models.ForeignKey('self', verbose_name='Связать с ценностью', on_delete=models.SET_NULL, null=True, blank=True)
	
	desc = models.TextField(verbose_name='Описание', max_length=10000, blank=True)

	def __str__(self):
		return u'%s %s' % (self.id, self.name)

	class Meta:
		ordering=['-id']
		verbose_name = u'Материальные ценности'
		verbose_name_plural = u'Материальные ценности'

class mvfile(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	sourcefile = models.FileField(verbose_name='Файл', upload_to=make_upload_mvfile, max_length=500)
	desc = models.CharField(verbose_name='Описание файла', max_length=255, blank=True)
	materialvalue = models.ForeignKey(materialvalue, on_delete=models.CASCADE)

	def __str__(self):
		return '%s %s' % (self.id, self.desc)

	class Meta:
		ordering = ['id']
		verbose_name = u'Файл материальной ценности'
		verbose_name_plural = u'Файлы материальной ценности'


class additionalphoto(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	materialvalue = models.ForeignKey(materialvalue, on_delete=models.CASCADE)
	photo = models.ImageField(verbose_name=u'Фотография',upload_to=make_upload_path, max_length=500)
	photo50 = ImageSpecField(source='photo', processors=[ResizeToFit(50, 50)], format='PNG', options={'quality': 95})

	class Meta:
		ordering = ['id']
		verbose_name = u'Дополнительные фотографии'
		verbose_name_plural = u'Дополнительные фотографии'


class materialvaluegmove(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	name = models.CharField(verbose_name='Название документа', max_length=255, default='Нет')
	cdate = models.DateField(verbose_name='Дата', auto_now_add=True)
	gmtype = models.CharField(verbose_name='Тип перемещения', max_length=30, choices=MOVETYPES, default='relocation')

	def __str__(self):
		return u'%s %s' % (self.id, self.name)

	class Meta:
		ordering=['id']
		verbose_name = u'Движение материальных ценностей по документу'
		verbose_name_plural = u'Движения материальных ценностей по документу'

###### старая таблица перемещений #######

class materialvaluemove(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	materialvaluegmove = models.ForeignKey(materialvaluegmove, on_delete=models.CASCADE, null=True, blank=True)
	materialvalue = models.ForeignKey(materialvalue, on_delete=models.CASCADE)
	mdate = models.DateField(verbose_name='Дата', default=timezone.now)
	# typelocation = models.CharField(verbose_name='Тип месторасположения', max_length=30, choices=LLIST, default='stock')
	# location = models.CharField(verbose_name='Местоположение', max_length=500, default='')
	note = models.CharField(verbose_name='Примечание', max_length=500, blank=True)
	stock = models.ForeignKey(stock, on_delete=models.CASCADE, verbose_name='Склад', null=True, blank=True) 
	shop = models.ForeignKey(shop, on_delete=models.CASCADE, verbose_name='Магазин', null=True, blank=True) 
	# parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Родитель', null=True, blank=True, limit_choices_to={'': True},) 

	def __str__(self):
		return u'%s %s' % (self.id, self.note)

	class Meta:
		ordering=['id']
		verbose_name = u'Движение материальных ценностей'
		verbose_name_plural = u'Движения материальных ценностей'

#### новая таблица перемещений

class mvmove(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	materialvaluegmove = models.ForeignKey(materialvaluegmove, on_delete=models.CASCADE, null=True, blank=True)
	materialvalue = models.ForeignKey(materialvalue, on_delete=models.CASCADE)
	mdate = models.DateField(verbose_name='Дата', default=timezone.now)
	note = models.CharField(verbose_name='Примечание', max_length=500, blank=True)
	shopstock = models.ForeignKey(shopstock, on_delete=models.CASCADE, verbose_name='Местонахождение')
	mvcell = models.ForeignKey(mvcell, on_delete=models.CASCADE, verbose_name='Конейнер->Ячейка', null=True, blank=True)

	def __str__(self):
		return u'%s %s' % (self.id, self.note)

	class Meta:
		ordering=['id']
		verbose_name = u'Движение материальных ценностей new'
		verbose_name_plural = u'Движения материальных ценностей new'

##############################
