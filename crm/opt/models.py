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

from dj.views import *
from node.models import *


class optbuyer(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	status = models.BooleanField(verbose_name='Статус', default=True)
	name = models.CharField(verbose_name='Название', max_length=100)
	#
	phone = models.CharField(verbose_name='Телефон', max_length=500, blank=True)
	email = models.CharField(verbose_name='E-mail', max_length=100, blank=True)
	#реквизиты
	#formorg = models.CharField(verbose_name='Форма организации (Индивидуальный предприниматель, ООО)', max_length=500, blank=True)
	fullname = models.CharField(verbose_name='Полное наименование', max_length=500, blank=True)
	namedir = models.CharField(verbose_name='ФИО Директора (полностью)', max_length=500, blank=True)
	org = models.CharField(verbose_name='На основании чего действует', max_length=500, blank=True)
	inn = models.CharField(verbose_name='ИНН/КПП', max_length=500, blank=True)
	ogrn = models.CharField(verbose_name='ОГРН', max_length=500, blank=True)
	bik = models.CharField(verbose_name='БИК', max_length=500, blank=True)
	bankname = models.CharField(verbose_name='Наименование банка', max_length=500, blank=True)
	checkaccount = models.CharField(verbose_name='Рас. счет', max_length=500, blank=True)
	coraccount = models.CharField(verbose_name='Кор. счет', max_length=500, blank=True)
	uraddr = models.CharField(verbose_name='Юр. Адрес', max_length=500, blank=True)
	
	def __str__(self):
		return u'%s %s' % (self.id, self.name)

	class Meta:
		ordering=['-id']
		verbose_name = u'Опт покупатель'
		verbose_name_plural = u'Опт покупатель'



class optprice(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	optbuyer = models.ForeignKey(optbuyer, on_delete=models.CASCADE, verbose_name='Оптовый покупатель')
	ctime = models.DateTimeField(verbose_name='Дата', auto_now_add=True)
	utime = models.DateTimeField(verbose_name='Дата формирования', auto_now=True)
	status = models.CharField(verbose_name='Статус', max_length=80, choices=(('create', u'Создан'), ('accept', u'Принят'), ('contract', u'Договор'), ('success', u'Выполнен'), ('cancel', u'Отменен'),), default='create')
	name = models.CharField(verbose_name='Название', max_length=100)
	url = models.CharField(verbose_name='Путь', max_length=100, default=id_generator())
	comment= models.TextField(verbose_name='Комментарий', help_text=u'Комментарий', max_length=30000, blank=True)
	#
	contract = models.FileField(verbose_name='Договор', upload_to=make_upload_file, max_length=500, blank=True)
	
	def __str__(self):
		return u'%s %s' % (self.id, self.name)

	class Meta:
		ordering=['-id']
		verbose_name = u'Опт ссылка'
		verbose_name_plural = u'Опт ссылка'
		
		
class optpricecart(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	ctime = models.DateTimeField(verbose_name='Дата', auto_now_add=True)
	optprice = models.ForeignKey(optprice, on_delete=models.CASCADE, verbose_name='Прайс') 
	goods = models.ForeignKey(goods, on_delete=models.CASCADE, verbose_name='Товар') 
	quant = models.FloatField(verbose_name='Количество', default=0)
	price = models.FloatField(verbose_name='Цена', default=0)

	def __str__(self):
		return u'%s' % (self.id)

	class Meta:
		ordering=['-id']
		verbose_name = u'Опт прайс корзина'
		verbose_name_plural = u'Опт прайс корзина'
