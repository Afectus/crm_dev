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


def make_upload_filetask(instance, filename):
	category = instance.__class__.__name__ #имя модели, каталог категория
	fileext = re.compile(r'^.*\.(?P<ext>\w+)$').match(filename).group('ext')
	filename = id_generator()
	return u"uploads/%s/%s" % (category, '%s.%s' % (filename, fileext))		


class usertask(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	status = models.CharField(verbose_name='Статус', max_length=80, choices=(('open', 'Открыто'), ('close', 'Закрыто'),), default='open')
	type = models.CharField(verbose_name='Тип', max_length=80, choices=(('free', 'Свободное задание'), ('user', 'Регламентное задание'),), default='free')
	ctime = models.DateTimeField(verbose_name='Дата', auto_now_add=True)
	etime = models.DateTimeField(verbose_name='Дедлайн', blank=True, null=True)
	priority = models.CharField(verbose_name='Приоритет', max_length=80, choices=(('slow', 'Низкий'), ('normal', 'Обычный'), ('fast', 'Срочно'), ('speed', 'Очень срочно')), default='normal')
	rating = models.PositiveIntegerField(verbose_name='Оценка задания', validators=[MinValueValidator(0), MaxValueValidator(10)], default=0)
	#like = models.PositiveIntegerField(verbose_name='Лайки', default=0)
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
	executor = models.ManyToManyField(profileuser, verbose_name='Исполнитель', blank=True)
	shop = models.ForeignKey(shop, on_delete=models.CASCADE, verbose_name='Магазин', blank=True, null=True)
	name = models.CharField(verbose_name=u'Заголовок', help_text='Тема задания', max_length=200)
	message= models.TextField(verbose_name=u'Сообщение', help_text=u'Текст задания', max_length=30000)
	#pict
	#pict1 = models.ImageField(verbose_name=u'Картинка 1', upload_to=make_upload_path, max_length=300, blank=True)
	#pict1200 = ImageSpecField(source='pict1', processors=[ResizeToFill(200, 200)], format='PNG', options={'quality': 75})
	#pict2 = models.ImageField(verbose_name=u'Картинка 2', upload_to=make_upload_path, max_length=300, blank=True)
	#pict2200 = ImageSpecField(source='pict2', processors=[ResizeToFill(200, 200)], format='PNG', options={'quality': 75})
	#pict3 = models.ImageField(verbose_name=u'Картинка 3', upload_to=make_upload_path, max_length=300, blank=True)
	#pict3200 = ImageSpecField(source='pict3', processors=[ResizeToFill(200, 200)], format='PNG', options={'quality': 75})
	#filetask = models.ManyToManyField(filetask, verbose_name='Приложения', blank=True)
	
	
	
	def __str__(self):
		return u'%s' % (self.id)

	class Meta:
		ordering=['-status']
		verbose_name = u'Задание'
		verbose_name_plural = u'Задания'



class filetask(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	usertask = models.ForeignKey(usertask, on_delete=models.CASCADE, verbose_name='Задание', blank=True, null=True)
	type = models.CharField(verbose_name='Тип', max_length=80, choices=(('image', 'Картинка'), ('file', 'Файл'),), default='file')
	name = models.CharField(verbose_name=u'Название', max_length=200, blank=True)
	#
	sourcefile = models.FileField(verbose_name='Файл', upload_to=make_upload_filetask, max_length=500, blank=True)
	
	#pict
	pict = models.ImageField(verbose_name=u'Картинка', upload_to=make_upload_path, max_length=300, blank=True)
	pict1 = ImageSpecField(source='pict', processors=[ResizeToFit(200, 200)], format='PNG', options={'quality': 75})

	def __str__(self):
		return u'%s' % (self.id)

	class Meta:
		ordering=['-id']
		verbose_name = u'Файлы заданий'
		verbose_name_plural = u'Файлы заданий'
		
		
class liketask(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	usertask = models.ForeignKey(usertask, on_delete=models.CASCADE, verbose_name='Задание')
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
	value = models.PositiveIntegerField(verbose_name='Рейтинг', validators=[MinValueValidator(1), MaxValueValidator(5)], default=1)

	def __str__(self):
		return u'%s' % (self.id)

	class Meta:
		ordering=['-id']
		verbose_name = u'Понравилось задание (like)'
		verbose_name_plural = u'Понравилось задание (like)'

		
class commenttask(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	ctime = models.DateTimeField(verbose_name='Дата', auto_now_add=True,)
	usertask = models.ForeignKey(usertask, on_delete=models.CASCADE, verbose_name='Задание', blank=True, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', blank=True, null=True)
	message= models.TextField(verbose_name=u'Сообщение', help_text=u'Комментарий', max_length=30000)

	#pict
	pict = models.ImageField(verbose_name=u'Картинка', upload_to=make_upload_path, max_length=300, blank=True)
	pict1 = ImageSpecField(source='pict', processors=[ResizeToFit(100, 100)], format='PNG', options={'quality': 75})
	
	def __str__(self):
		return u'%s' % (self.id)

	class Meta:
		ordering=['ctime']
		verbose_name = u'Комментарий задания'
		verbose_name_plural = u'Комментарии заданий'





class notificationtask(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	ctime = models.DateTimeField(verbose_name='Дата', auto_now_add=True,)
	usertask = models.ForeignKey(usertask, on_delete=models.CASCADE, verbose_name='Задание')
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
	
	def __str__(self):
		return u'%s' % (self.id)

	class Meta:
		ordering=['ctime']
		verbose_name = u'Оповещение о новом задании'
		verbose_name_plural = u'Оповещение о новом задании'




		