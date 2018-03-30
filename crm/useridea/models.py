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

from node.models import *

from panel.models import *


#ИДЕИ
def make_upload_fileidea(instance, filename):
	category = instance.__class__.__name__ #имя модели, каталог категория
	fileext = re.compile(r'^.*\.(?P<ext>\w+)$').match(filename).group('ext')
	filename = id_generator()
	return u"uploads/%s/%s" % (category, '%s.%s' % (filename, fileext))		


class useridea(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	ctime = models.DateTimeField(verbose_name='Дата', auto_now_add=True)
	rating = models.PositiveIntegerField(verbose_name='Оценка задания', validators=[MinValueValidator(0), MaxValueValidator(10)], default=0)
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
	name = models.CharField(verbose_name=u'Заголовок', help_text='Тема задания', max_length=200)
	message= models.TextField(verbose_name=u'Сообщение', help_text=u'Текст задания', max_length=30000)
	
	def __str__(self):
		return u'%s' % (self.id)

	class Meta:
		ordering=['-id']
		verbose_name = u'Идея'
		verbose_name_plural = u'Идеи'



class fileidea(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	useridea = models.ForeignKey(useridea, on_delete=models.CASCADE, verbose_name='Идея', blank=True, null=True)
	type = models.CharField(verbose_name='Тип', max_length=80, choices=(('image', 'Картинка'), ('file', 'Файл'),), default='file')
	name = models.CharField(verbose_name=u'Название', max_length=200, blank=True)
	#
	sourcefile = models.FileField(verbose_name='Файл', upload_to=make_upload_fileidea, max_length=500, blank=True)
	
	#pict
	pict = models.ImageField(verbose_name=u'Картинка', upload_to=make_upload_path, max_length=300, blank=True)
	pict1 = ImageSpecField(source='pict', processors=[ResizeToFit(200, 200)], format='PNG', options={'quality': 75})

	def __str__(self):
		return u'%s' % (self.id)

	class Meta:
		ordering=['-id']
		verbose_name = u'Файлы идеи'
		verbose_name_plural = u'Файлы идей'
		
		
class likeidea(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	useridea = models.ForeignKey(useridea, on_delete=models.CASCADE, verbose_name='Идея')
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
	value = models.PositiveIntegerField(verbose_name='Рейтинг', validators=[MinValueValidator(1), MaxValueValidator(5)], default=1)

	def __str__(self):
		return u'%s' % (self.id)

	class Meta:
		ordering=['-id']
		verbose_name = u'Понравилась идея (like)'
		verbose_name_plural = u'Понравилась идея (like)'

		
class commentidea(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	ctime = models.DateTimeField(verbose_name='Дата', auto_now_add=True,)
	useridea = models.ForeignKey(useridea, on_delete=models.CASCADE, verbose_name='Идея', blank=True, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', blank=True, null=True)
	message= models.TextField(verbose_name=u'Сообщение', help_text=u'Комментарий', max_length=30000)

	#pict
	pict = models.ImageField(verbose_name=u'Картинка', upload_to=make_upload_path, max_length=300, blank=True)
	pict1 = ImageSpecField(source='pict', processors=[ResizeToFit(100, 100)], format='PNG', options={'quality': 75})
	
	def __str__(self):
		return u'%s' % (self.id)

	class Meta:
		ordering=['ctime']
		verbose_name = u'Комментарий идеи'
		verbose_name_plural = u'Комментарии идей'















		