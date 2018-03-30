# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models

from PIL import Image
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit, SmartResize, Transpose, Adjust

from django.db.models.signals import post_delete, post_save
from django.db.models.signals import pre_delete

from django.contrib.auth.models import User, Group, UserManager

from django.core.validators import MinValueValidator, MaxValueValidator

from dj.views import *
from node.models import *

from panel.models import *


class picture(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	pict = models.ImageField(verbose_name=u'Картинка', upload_to=make_upload_path, max_length=500)
	pict20 = ImageSpecField(source='pict', processors=[ResizeToFit(20, 20)], format='PNG', options={'quality': 95})
	pict40 = ImageSpecField(source='pict', processors=[ResizeToFit(40, 40)], format='PNG', options={'quality': 95})
	desc = models.CharField(verbose_name='Описание картинки', max_length=255, blank=True)

class file(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	sourcefile = models.FileField(verbose_name='Файл', upload_to=make_upload_file, max_length=500)
	desc = models.CharField(verbose_name='Описание файла', max_length=255, blank=True)

# Разделы биржи идей
class ideasection(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	name = models.CharField(verbose_name='Название раздела', help_text='Название раздела', max_length=200)
	
	def __str__(self):
		return '%s %s' % (self.id, self.name)

	class Meta:
		ordering=['id']
		verbose_name = 'Раздел биржи идей'
		verbose_name_plural = 'Разделы биржи идей'

#идеи
SLIST = (
	('under_consideration', 'На рассмотрении'),
	('adopted', 'Принята'),
	('rejected', 'Отклонена')
)

class useridea(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	section = models.ForeignKey(ideasection, verbose_name='Раздел', on_delete=models.CASCADE)
	ctime = models.DateTimeField(verbose_name='Дата', auto_now_add=True)
	rating = models.PositiveIntegerField(verbose_name='Оценка задания', validators=[MinValueValidator(1), MaxValueValidator(5)], default=0)
	user = models.ForeignKey(profileuser, verbose_name='Пользователь', on_delete=models.CASCADE)
	name = models.CharField(verbose_name='Тема', max_length=200)
	message= models.TextField(verbose_name='Текст идеи', max_length=30000)
	pict = models.ManyToManyField(picture, blank=True)
	file = models.ManyToManyField(file, blank=True)
	status = models.CharField(verbose_name='Статус', max_length=30, choices=SLIST, default='under_consideration')

	def __str__(self):
		return '%s %s' % (self.id, self.name)

	class Meta:
		ordering=['-rating']
		verbose_name = 'Идея'
		verbose_name_plural = 'Идеи'

#комментарии
class commentidea(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	ctime = models.DateTimeField(verbose_name='Дата', auto_now_add=True,)
	useridea = models.ForeignKey(useridea, verbose_name='Идея', blank=True, null=True, on_delete=models.CASCADE)
	user = models.ForeignKey(profileuser, verbose_name='Пользователь', blank=True, null=True, on_delete=models.CASCADE)
	message= models.TextField(verbose_name=u'Сообщение', help_text=u'Комментарий', max_length=30000)
	pict = models.ManyToManyField(picture, blank=True)
	file = models.ManyToManyField(file, blank=True)
	# #pict
	# pict = models.ImageField(verbose_name=u'Картинка', upload_to=make_upload_path, max_length=300, blank=True)
	# pict1 = ImageSpecField(source='pict', processors=[ResizeToFit(100, 100)], format='PNG', options={'quality': 75})
	
	def __str__(self):
		return u'%s' % (self.id)

	class Meta:
		ordering=['ctime']
		verbose_name = u'Комментарий идеи'
		verbose_name_plural = u'Комментарии идей'

class likeidea(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	useridea = models.ForeignKey(useridea, verbose_name='Идея', on_delete=models.CASCADE)
	user = models.ForeignKey(profileuser, verbose_name='Пользователь', on_delete=models.CASCADE)
	value = models.PositiveIntegerField(verbose_name='Рейтинг', validators=[MinValueValidator(1), MaxValueValidator(5)], default=1)

	def __str__(self):
		return u'%s' % (self.id)

	class Meta:
		ordering=['-id']
		verbose_name = u'Понравилась идея (like)'
		verbose_name_plural = u'Понравилась идея (like)'
