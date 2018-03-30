# -*- coding: utf-8 -*-
from django.db import models

from PIL import Image
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit, SmartResize, Transpose, Adjust
from django.db.models.signals import post_delete, post_save, pre_save
from django.db.models.signals import pre_delete

from dj.views import make_upload_path
from dj.views import id_generator

from django.utils.safestring import mark_safe

from django.utils import timezone

from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User, Group

import re

from node.models import *

#Отзывы в битриксе
class review(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	status = models.BooleanField(verbose_name='Статус', default=False)
	ctime = models.DateTimeField(verbose_name='Дата', auto_now_add=True)
	subj = models.CharField(verbose_name='Тема', max_length=200, choices=(('recall', 'Отзыв'), ('complaint', 'Жалоба'), ('sentence', 'Предложение'), ('expert', 'Вопрос эксперту'),), default='recall')
	uname = models.CharField(verbose_name='Имя', max_length=200)
	email = models.EmailField(verbose_name='Электронный адрес', blank=True)
	phone = models.CharField(verbose_name='Телефон', max_length=11, blank=True)
	order = models.CharField(verbose_name='Номер заказа', max_length=200, blank=True)
	message = models.TextField(verbose_name='Отзыв', max_length=10000)
	comment = models.TextField(verbose_name='Комментарий', max_length=10000, blank=True)
	
	
	def __str__(self):
		return '%s %s' % (self.id, self.email)

	class Meta:
		ordering=['id']
		verbose_name = u'Отзыв'
		verbose_name_plural = u'Отзывы'
		
		
		

#модификация персональных данных
class buyermessage(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	status = models.BooleanField(verbose_name='Статус', default=True)
	ctime = models.DateTimeField(verbose_name='Дата', auto_now_add=True)
	buyer = models.ForeignKey(buyer, on_delete=models.CASCADE, verbose_name='Покупатель', null=True, blank=True)
	message = models.TextField(verbose_name='Сообщение', max_length=10000)
	
	def __str__(self):
		return '%s' % (self.id)

	class Meta:
		ordering=['id']
		verbose_name = u'Модификация персональных данных'
		verbose_name_plural = u'Модификация персональных данных'
