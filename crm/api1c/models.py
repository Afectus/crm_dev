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

class uploadzip(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	name = models.CharField(verbose_name='Архив', max_length=300, blank=True)

	def __str__(self):
		return u'%s' % (self.id)

	class Meta:
		ordering=['-id']
		verbose_name = u'Архив'
		verbose_name_plural = u'Архив'
		

class procedureexchange(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Зависимость', null=True, blank=True)
	cron = models.BooleanField(verbose_name='cron', default=False)
	cron2 = models.BooleanField(verbose_name='cron2', default=False)
	mono = models.BooleanField(verbose_name='Одиночная', default=False)
	status = models.BooleanField(verbose_name='Статус', default=True)
	start = models.BooleanField(verbose_name='Выгружать', default=False)
	name = models.CharField(verbose_name='Название', max_length=500)
	code = models.CharField(verbose_name='Код обработки', max_length=100)
	fname = models.CharField(verbose_name='Файл', max_length=200, blank=True)
	sort = models.PositiveIntegerField(verbose_name='Сортировка', default=0)
	comment= models.TextField(verbose_name='Комментарий', max_length=30000, blank=True)
	
	
	def __str__(self):
		return u'%s %s' % (self.code, self.name)

	class Meta:
		ordering=['-sort']
		verbose_name = u'Процедура обмена'
		verbose_name_plural = u'Процедура обмена'
		



def make_upload_logexchange(instance, filename):
	#print instance._get_FIELD_display
	#print dir(instance.__class__)
	category = instance.__class__.__name__ #имя модели, каталог категория
	fieldname = 'sourcefile' #имя поля модели, каталог подкатегория
	fileext = re.compile(r'^.*\.(?P<ext>\w+)$').match(filename).group('ext')
	#filename = id_generator() #NOT GENERATE FILENAME, USE ORIGINAL
	return u"uploads/%s_%s/%s" % (category, fieldname, '%s.%s' % (filename, fileext))	
	
class logexchange(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	success = models.BooleanField(verbose_name='С.Обр.', default=False)
	procedureexchange = models.ForeignKey(procedureexchange, on_delete=models.CASCADE, verbose_name='Обработка', null=True, blank=True)
	target = models.CharField(verbose_name='Цель', max_length=500, blank=True)
	ctime = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
	ftime = models.DateTimeField(verbose_name='Время файла', null=True, blank=True)
	fname = models.CharField(verbose_name='Файл название', max_length=500)
	sourcefile = models.FileField(upload_to=make_upload_logexchange, max_length=500, blank=True)
	#контроль времени выгрузки
	startexectime = models.TimeField(verbose_name='Старт выгрузки', auto_now_add=True)
	endexectime = models.TimeField(verbose_name='Конец выгрузки', default=timezone.now)
	
	def __str__(self):
		return u'%s' % (self.id)

	class Meta:
		ordering=['-id']
		verbose_name = u'Лог обмена'
		verbose_name_plural = u'Лог обмена'