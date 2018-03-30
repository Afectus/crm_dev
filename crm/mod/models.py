# -*- coding: utf-8 -*-
from django.db import models

from PIL import Image
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit, SmartResize, Transpose, Adjust

from django.db.models.signals import post_delete, post_save
from django.db.models.signals import pre_delete

from django.contrib.auth.models import User, Group, UserManager

from node.models import *





class ballconfitem(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id',)
	name = models.CharField(max_length=100, verbose_name='Название', blank=True)
	bid = models.PositiveIntegerField(verbose_name='id', blank=True)
	x = models.FloatField(verbose_name='x', blank=True)
	y = models.FloatField(verbose_name='y', blank=True)
	radius = models.PositiveIntegerField(verbose_name='radius', blank=True)
	color = models.CharField(verbose_name='color', max_length=100, blank=True)
	colortext = models.CharField(verbose_name='Код цвета', max_length=100, blank=True)
	background = models.CharField(verbose_name='Задний фон', max_length=500, blank=True)
	
	def __str__(self):
		return '%s' % (self.id)

	class Meta:
		ordering=['-id']
		verbose_name = u'Конструктор шариков'
		verbose_name_plural = u'Конструктор шариков'
		
	
class goreport(models.Model):
	id = models.AutoField(primary_key=True)
	time = models.DateTimeField(auto_now_add=True)
	ua = models.CharField(verbose_name=u'User Agent', max_length=300, blank=True)
	ip = models.GenericIPAddressField(verbose_name=u'IP', null=True, blank=True)

	def __str__(self):
		return '%s' % (self.id)
	
	class Meta:
		ordering=['-id']
		verbose_name = u'Go Отчет (babah24.ru/go)'
		verbose_name_plural = u'Go Отчеты (babah24.ru/go)'
		
		
class qrcodereport(models.Model):
	id = models.AutoField(primary_key=True)
	time = models.DateTimeField(auto_now_add=True)
	ua = models.CharField(verbose_name=u'User Agent', max_length=300, blank=True)
	ip = models.GenericIPAddressField(verbose_name=u'IP', null=True, blank=True)
	comment = models.CharField(verbose_name='Комментарий', max_length=300, blank=True)

	def __str__(self):
		return '%s' % (self.id)
	
	class Meta:
		ordering=['-id']
		verbose_name = u'Отчет переход по QR коду'
		verbose_name_plural = u'Отчет переходы по QR кодам'

