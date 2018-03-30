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


def make_upload_filebook(instance, filename):
	category = instance.__class__.__name__ #имя модели, каталог категория
	fileext = re.compile(r'^.*\.(?P<ext>\w+)$').match(filename).group('ext')
	filename = id_generator()
	return u"uploads/%s/%s" % (category, '%s.%s' % (filename, fileext))		


class librarybook(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	ctime = models.DateTimeField(verbose_name='Дата', auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
	name = models.CharField(verbose_name=u'Название', help_text='verbose_name', max_length=500)
	desc= models.TextField(verbose_name=u'Описание', help_text=u'Описание', max_length=30000)
	
	#pict
	pict = models.ImageField(verbose_name=u'Обложка', upload_to=make_upload_path, max_length=300, blank=True)
	pict200 = ImageSpecField(source='pict', processors=[ResizeToFit(400, 400)], format='PNG', options={'quality': 75})
	pict400 = ImageSpecField(source='pict', processors=[ResizeToFit(400, 400)], format='PNG', options={'quality': 75})
	
	sourcefile = models.FileField(verbose_name='Файл', upload_to=make_upload_filebook, max_length=500, blank=True)
	
	def __str__(self):
		return u'%s' % (self.id)

	class Meta:
		ordering=['-id']
		verbose_name = u'Книга'
		verbose_name_plural = u'Книги'
		
		
class librarybooklike(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	librarybook = models.ForeignKey(librarybook, on_delete=models.CASCADE, verbose_name='Книга')
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
	value = models.PositiveIntegerField(verbose_name='Рейтинг', validators=[MinValueValidator(1), MaxValueValidator(5)], default=1)

	def __str__(self):
		return u'%s' % (self.id)

	class Meta:
		ordering=['-id']
		verbose_name = u'Оценил книгу (like)'
		verbose_name_plural = u'Оценили книгу (like)'

		
class librarybookcomment(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	ctime = models.DateTimeField(verbose_name='Дата', auto_now_add=True,)
	librarybook = models.ForeignKey(librarybook, on_delete=models.CASCADE, verbose_name='Книга')
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




		