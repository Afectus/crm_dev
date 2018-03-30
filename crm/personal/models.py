# -*- coding: utf-8 -*-
from django.db import models

from PIL import Image
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit, SmartResize, Transpose, Adjust

from django.db.models.signals import post_delete, post_save
from django.db.models.signals import pre_delete

from django.contrib.auth.models import User, Group, UserManager

from django.core.validators import MinValueValidator, MaxValueValidator

import datetime
from django.utils import timezone

from node.models import *
from panel.models import *


#Анкеты сотрудников
class personalanketa(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	profileuser = models.ForeignKey(profileuser, on_delete=models.CASCADE, verbose_name='Пользователь', blank=True, null=True)
	
	status = models.CharField(verbose_name='Статус', max_length=80, choices=(('on', 'Действующий'), ('off', 'Уволен'), ('wait', 'Резерв'), ('drop', 'Черный список')), default='on')
	
	name = models.CharField(verbose_name='Имя', help_text='Имя', max_length=200, blank=True)
	bday = models.DateField(verbose_name='Дата рождения', help_text='формат: dd.mm.yyyy', null=True, blank=True)
	phone = models.CharField(verbose_name='Телефон', help_text='Телефон', max_length=200, blank=True)
	message = models.TextField(verbose_name='Информация', help_text='Информация', max_length=100000, blank=True)
	pict = models.ImageField(verbose_name='Фото', upload_to=make_upload_path, max_length=500, blank=True)
	pict200 = ImageSpecField(source='pict', processors=[ResizeToFit(200, 200)], format='PNG', options={'quality': 95})
	pict300 = ImageSpecField(source='pict', processors=[ResizeToFit(300, 300)], format='PNG', options={'quality': 95})
	
	
	def __str__(self):
		return u'%s' % (self.id)

	class Meta:
		ordering=['-id']
		verbose_name = u'Внештатные сотрудники'
		verbose_name_plural = u'Внештатные сотрудники'	





#дети сотрудников
class personalchild(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	profileuser = models.ForeignKey(profileuser, on_delete=models.CASCADE, verbose_name='Пользователь')
	name = models.CharField(verbose_name='ФИО', max_length=200)
	bday = models.DateField(verbose_name='Дата рождения', help_text='формат %d.%m.%Y')

	def __str__(self):
		return '%s' % (self.id)

	class Meta:
		ordering=['-id']
		verbose_name = u'Дети сотрудников'
		verbose_name_plural = u'Дети сотрудников'



#подвиги сотрудников
class personalfeat(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	profileuser = models.ForeignKey(profileuser, on_delete=models.CASCADE, verbose_name='Пользователь')
	ctime = models.DateField(verbose_name=u'Дата',)
	name = models.CharField(verbose_name=u'Заголовок', help_text='Заголовок', max_length=200)
	message= models.TextField(verbose_name=u'Текст', help_text=u'Текст', max_length=30000)
	pict = models.ManyToManyField(imagebase, verbose_name='Изображения', blank=True)
	
	def __str__(self):
		return u'%s' % (self.id)

	class Meta:
		ordering=['-id']
		verbose_name = u'Подвиг сотрудника'
		verbose_name_plural = u'Подвиги сотрудников'	
	
