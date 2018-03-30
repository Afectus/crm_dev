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



	
#инвентарный лист
class invlist(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	name = models.CharField(verbose_name=u'Название', max_length=200)
	cdate = models.DateField(verbose_name='Дата')
	status = models.BooleanField(verbose_name='Статус', default=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
	message= models.TextField(verbose_name=u'Комментарий', help_text=u'Комментарий', max_length=30000, blank=True)
	
	def __str__(self):
		return u'%s %s' % (self.id, self.name)

	class Meta:
		ordering=['-cdate']
		verbose_name = u'Инвентаризация'
		verbose_name_plural = u'Инвентаризация'
		
#инвентарный лист
class invitem(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	ctime = models.DateField(verbose_name='Время', auto_now_add=True)
	invlist = models.ForeignKey(invlist, on_delete=models.CASCADE)
	goods = models.ForeignKey(goods, on_delete=models.CASCADE, verbose_name='Товар', blank=True, null=True)
	barcode = models.CharField(verbose_name='Штрих код', max_length=100)
	lifedate = models.DateField(verbose_name='Срок годности', help_text='формат: dd.mm.yyyy', blank=True, null=True)
	col = models.PositiveIntegerField(verbose_name='Количество', default=1)
	message= models.TextField(verbose_name='Комментарий', max_length=30000, blank=True)
	
	def __str__(self):
		return u'%s' % (self.id)

	class Meta:
		ordering=['-id']
		verbose_name = u'Инвентаризация список'
		verbose_name_plural = u'Инвентаризация список'		
