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


class printtask(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	goods = models.ForeignKey(goods, on_delete=models.CASCADE, verbose_name='Товар')
	copies = models.PositiveIntegerField(verbose_name='Количество копий', default=1)
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', null=True, blank=True)
	status = models.BooleanField(verbose_name='Статус', default=True)
	report = models.TextField(verbose_name='Отчет', max_length=10000, blank=True)
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
		

	
#distributor
class distributormenu(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	name = models.CharField(verbose_name='Название', max_length=200)
	aclu = models.ManyToManyField(aclu, verbose_name='Права', limit_choices_to={'aclobject__objectid': 'distributormenu'}, blank=True)

	def __str__(self):
		return '%s %s' % (self.id, self.name)

	class Meta:
		ordering=['id']
		verbose_name = u'Поставщики меню'
		verbose_name_plural = u'Поставщики меню'

		
		
#distributortype=(('goods', 'Товар'), ('marketing', 'Рекламные услуги'), ('office', 'Обслуживание офиса'), )


def make_upload_pricefile(instance, filename):
	category = instance.__class__.__name__ #имя модели, каталог категория
	fileext = re.compile(r'^.*\.(?P<ext>\w+)$').match(filename).group('ext')
	filename = id_generator()
	return u"uploads/%s/%s" % (category, '%s.%s' % (filename, fileext))			
		
class distributor(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	name = models.CharField(verbose_name='Название', max_length=200)
	#type = models.CharField(verbose_name='Тип', max_length=300, choices=distributortype, default='goods')
	distributormenu = models.ForeignKey(distributormenu, on_delete=models.CASCADE, verbose_name='Категория')
	#tax = models.ManyToManyField(tax, verbose_name='Категория', blank=True)
	tax2 = models.TextField(verbose_name='Категория списком', max_length=10000, blank=True)
	#координаты
	a = models.CharField(verbose_name='Контактное лицо', max_length=10000, blank=True)
	b = models.TextField(verbose_name='Контактная информация', max_length=10000, blank=True)
	c = models.TextField(verbose_name='Банковские реквизиты', max_length=10000, blank=True)
	#csite = models.CharField(verbose_name='Сайт', max_length=1000, blank=True)
	#cmail = models.CharField(verbose_name='Почта', max_length=1000, blank=True)
	#cphone = models.CharField(verbose_name='Телефон', max_length=1000, blank=True)
	desc = models.TextField(verbose_name='Примечание', max_length=10000, blank=True)
	#
	pricefile = models.FileField(verbose_name='Прайс 1', upload_to=make_upload_pricefile, max_length=500, blank=True)
	pricefile2 = models.FileField(verbose_name='Прайс 2', upload_to=make_upload_pricefile, max_length=500, blank=True)
	pricefile3 = models.FileField(verbose_name='Прайс 3', upload_to=make_upload_pricefile, max_length=500, blank=True)
	
	def __str__(self):
		return '%s %s' % (self.id, self.name)

	class Meta:
		ordering=['id']
		verbose_name = u'Поставщики'
		verbose_name_plural = u'Поставщики'
		
		


		
		
		
		