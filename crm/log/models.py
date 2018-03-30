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

from node.models import *

class commonlog(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	ctime = models.DateTimeField(verbose_name='Дата/Время', auto_now_add=True)
	name = models.CharField(verbose_name='Название', max_length=200)
	desc = models.TextField(verbose_name='Полезная информация', max_length=10000, blank=True)
	
	def __str__(self):
		return '%s %s %s' % (self.id, self.ctime, self.name)

	class Meta:
		ordering=['id']
		verbose_name = u'Общий лог'
		verbose_name_plural = u'Общий лог'
		
		
class kassirlog(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	ctime = models.DateTimeField(verbose_name='Дата/Время', auto_now_add=True)
	name = models.CharField(verbose_name='Название', max_length=200)
	desc = models.TextField(verbose_name='Полезная информация', max_length=10000, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', blank=True, null=True)
	
	def __str__(self):
		return '%s %s %s' % (self.id, self.ctime, self.name)

	class Meta:
		ordering=['id']
		verbose_name = u'Кассир лог'
		verbose_name_plural = u'Кассир лог'	
		
		
		
class mailres(models.Model):
	id = models.AutoField(primary_key=True, verbose_name='id',)
	status = models.BooleanField(verbose_name='Статус', default=True)
	ctime = models.DateField(verbose_name='Время создания', auto_now_add=True)
	email = models.EmailField(verbose_name='Электронный адрес', max_length=80, blank=True)
	action = models.CharField(verbose_name='Действие', max_length=500, blank=True)
	result = models.CharField(verbose_name='Отчет', max_length=500, blank=True)

	def __str__(self):
		return '%s' % (self.id)

	class Meta:
		ordering=['-id']
		verbose_name = u'Результат отправки почты'
		verbose_name_plural = u'Результат отправки почты'