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
from panel.models import *
from acl.models import *
from acl.views import *


class pricequeue(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	ctime = models.DateTimeField(verbose_name='Время добавления', auto_now_add=True)
	goods = models.ForeignKey(goods, on_delete=models.CASCADE, verbose_name='Товар')
	copies = models.PositiveIntegerField(verbose_name='Количество копий', default=1)
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', null=True, blank=True)
	status = models.BooleanField(verbose_name='Статус', default=True)
	#report = models.TextField(verbose_name='Отчет', max_length=10000, blank=True)
	#штрихкод, потому, что их 2 и что бы можно было корректировать
	barcode = models.CharField(verbose_name='Штрихкод', max_length=200, blank=True)
	#ценник
	imageprice = models.ImageField(verbose_name=u'Ценник', upload_to=make_upload_path, max_length=500, blank=True)
	imageprice300 = ImageSpecField(source='imageprice', processors=[ResizeToFill(375, 350)], format='PNG', options={'quality': 100})
	imageprice500 = ImageSpecField(source='imageprice', processors=[ResizeToFit(500, 500)], format='PNG', options={'quality': 95})

	
	def __str__(self):
		return '%s' % (self.id)

	class Meta:
		ordering=['id']
		verbose_name = u'Задания печати'
		verbose_name_plural = u'Задания печати'
		

		
		