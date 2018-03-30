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


#лист учета посетителей
class kassirvisitorlog(models.Model):
	id = models.AutoField(primary_key=True)
	shop = models.ForeignKey(shop, on_delete=models.CASCADE, verbose_name='Магазин')
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', blank=True, null=True)
	ctime = models.DateTimeField(verbose_name='Время', auto_now_add=True)
	who = models.CharField(verbose_name='Кто', max_length=300, choices=(('buyer', 'Покупатель'), ('personal', 'Сотрудники'), ('other', 'Гости (по рекламе, курьеры и др.)'),), default='buyer')
	period = models.CharField(verbose_name='Время', max_length=300, choices=(('A', '9:00-11:00'), ('B', '11:00-13:00'), ('C', '13:00-15:00'), ('D', '15:00-18:00'), ('E', '18:00-20:00'), ), default='A')
	value = models.PositiveIntegerField(verbose_name='Количество', default=1)

	class Meta:
		ordering=['-id']
		verbose_name = u'Лист учета посетителей'
		verbose_name_plural = u'Лист учета посетителей'

