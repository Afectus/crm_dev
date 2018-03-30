# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from PIL import Image
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit, SmartResize, Transpose, Adjust
from django.db.models.signals import post_delete, post_save, pre_save
from django.db.models.signals import pre_delete

from dj.views import *

from django.utils.safestring import mark_safe

from django.utils import timezone

from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User, Group

import re

from node.models import *


class callreportlog(models.Model):
	id = models.AutoField(primary_key=True)
	ctime = models.DateTimeField(auto_now_add=True)
	# user = models.ForeignKey(User, verbose_name='Менеджер', blank=True, null=True)
	route = models.CharField(verbose_name='Маршрут звонка', max_length=300, choices=(('external', 'Внешний звонок'), ('internal', 'Внутренний звонок'), ('callback', 'Обратный звонок')), default='external')
	phone = models.CharField(verbose_name='Номер клиента', max_length=20, blank=True)
	phone8 = models.CharField(verbose_name='Номер клиента', max_length=20, blank=True)
	incoming_number = models.CharField(verbose_name='Входящий номер', max_length=20, blank=True)
	# text = models.CharField(verbose_name='Текст сообщения', max_length=1000, blank=True)
	info = models.TextField(verbose_name='Инфо', max_length=3000, blank=True)

	def __str__(self):
		return '%s' % (self.id)
	
	class Meta:
		ordering=['-id']
		verbose_name = 'Лог звонки'
		verbose_name_plural = 'Лог звонки'



# class smsreport(models.Model):
	# id = models.AutoField(primary_key=True)
	# user = models.ForeignKey(User, verbose_name='Менеджер', blank=True, null=True)
	# phone = models.CharField(verbose_name='Номер телефона', max_length=20)
	# time = models.DateTimeField(auto_now_add=True)
	# text = models.CharField(verbose_name='Текст сообщения', max_length=1000, blank=True)
	# status = models.TextField(verbose_name='Результат отправки', max_length=3000, blank=True)

	# def __str__(self):
		# return '%s %s' % (self.id, self.phone)
	
	# class Meta:
		# ordering=['-id']
		# verbose_name = u'SMS Отчет'
		# verbose_name_plural = u'SMS Отчеты'
		
		
# class smstemplate(models.Model):
	# id = models.AutoField(primary_key=True)
	# status = models.BooleanField(verbose_name='Статус', default=False)
	# sort = models.PositiveIntegerField(verbose_name='Приоритет', default=100)
	# name = models.CharField(verbose_name='Название', max_length=200)
	# message = models.TextField(verbose_name='Шаблон', max_length=300)

	# def __str__(self):
		# return '%s %s %s' % (self.id, self.status, self.name)
	
	# class Meta:
		# ordering=['-sort']
		# verbose_name = u'SMS Шаблон'
		# verbose_name_plural = u'SMS Шаблоны'
		
		
# class smsqsend(models.Model):
	# id = models.AutoField(primary_key=True)
	# cdate = models.DateTimeField(auto_now_add=True)
	# buyer = models.ForeignKey(buyer, verbose_name='Покупатель')
	# status = models.BooleanField(verbose_name='Работает', default=False)
	# send= models.BooleanField(verbose_name='Отправлено', default=False)
	# back= models.BooleanField(verbose_name='Переход клиента', default=False)
	# backurl = models.CharField(verbose_name='Обратная ссылка', max_length=100, blank=True)
	# #
	# message = models.TextField(verbose_name='Шаблон', max_length=500)
	# result = models.CharField(verbose_name='Результат', max_length=1000, blank=True)

	# def __str__(self):
		# return '%s %s' % (self.id, self.status)
	
	# class Meta:
		# ordering=['-id']
		# verbose_name = u'SMS Очередь'
		# verbose_name_plural = u'SMS Очередь'

		
		
		
		

# class callreport(models.Model):
	# id = models.AutoField(primary_key=True)
	# user = models.ForeignKey(User, verbose_name='Менеджер', blank=True, null=True)
	# phone = models.CharField(verbose_name='Номер телефона', max_length=20)
	# time = models.DateTimeField(auto_now_add=True)
	# text = models.CharField(verbose_name='', max_length=1000, blank=True)
	# status = models.TextField(verbose_name='Результат', max_length=3000, blank=True)

	# def __str__(self):
		# return '%s %s' % (self.id, self.phone)
	
	# class Meta:
		# ordering=['-id']
		# verbose_name = u'Виртуальная АТС отчет'
		# verbose_name_plural = u'Виртуальная АТС отчет'
