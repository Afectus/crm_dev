# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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


from node.models import *


#Плейлисты, радио
class playlist(models.Model):
	id = models.AutoField(primary_key=True)
	status = models.BooleanField(verbose_name='Статус', default=True)
	name = models.CharField(verbose_name='Название', max_length=100)
	type = models.CharField(verbose_name='Тип', max_length=80, choices=(('url', 'Внешний url'), ('path', 'Каталог')), default='url')
	url = models.CharField(verbose_name='URL Адрес или путь', max_length=200, blank=True)
	
	def __str__(self):
		return '%s %s' % (self.id, self.name)
	
	class Meta:
		ordering=['-id']
		verbose_name = u'Плейлист'
		verbose_name_plural = u'Плейлисты'	


#таблица параметров для магазина
class shopset(models.Model):
	id = models.AutoField(primary_key=True)
	shop = models.ForeignKey(shop, on_delete=models.CASCADE, verbose_name='Магазин', blank=True, null=True)
	#
	mixpromo = models.BooleanField(verbose_name='Смешивать проморолики', default=False)
	mixaudio = models.BooleanField(verbose_name='Смешивать радио', default=False)
	#
	promoperiod = models.IntegerField(verbose_name='Через сколько воспроизводить', default=120)
	previewtimeout = models.IntegerField(default=5)
	radioping = models.IntegerField(default=120)
	#
	playlist = models.ForeignKey(playlist, on_delete=models.CASCADE, verbose_name='Плейлист', blank=True, null=True)
	#
	audiopromoperiod = models.IntegerField(default=600)
	
	def __str__(self):
		return '%s' % (self.shop.name)
	
	class Meta:
		ordering=['id']
		verbose_name = u'Настройки магазина'
		verbose_name_plural = u'Настройки магазина'





#устройства расберри
class device(models.Model):
	id = models.AutoField(primary_key=True)
	token = models.CharField(verbose_name='Ключ доступа', max_length=100, default=id_generator())
	shopset = models.ForeignKey(shopset, on_delete=models.CASCADE, verbose_name='Настройки магазин', blank=True, null=True)
	#ping
	pingsave = models.DateTimeField(verbose_name='Ping last save', auto_now=True)
	pingsetip = models.DateTimeField(verbose_name='Ping set IP', auto_now_add=True)
	pingcron = models.DateTimeField(verbose_name='Ping dev cron', auto_now_add=True)
	#
	name = models.CharField(verbose_name='Название устройства', max_length=100)
	ip = models.CharField(verbose_name='IP', max_length=100, blank=True, null=True)
	vpnip = models.CharField(verbose_name='VPN IP', max_length=100, blank=True, null=True)
	mac = models.CharField(verbose_name='MAC устройства', max_length=100, unique=True)
	status = models.BooleanField(verbose_name='S', default=True)
	reboot = models.BooleanField(verbose_name='Перезагрузка (в течении 5 минут)', default=False)
	#
	videostream = models.BooleanField(verbose_name='Видео устройство', default=False)
	audiostream = models.BooleanField(verbose_name='Аудио устройство', default=False)
	touchscreen = models.BooleanField(verbose_name='Тачскрин устройство', default=False)
	radiostream = models.BooleanField(verbose_name='Радио устройство', default=False)
	#
	promovideo = models.BooleanField(verbose_name='Промо видео', default=False)
	promotouchscreen = models.BooleanField(verbose_name='Промо-тачскрин', default=False)
	#
	updatetime = models.IntegerField(verbose_name='Время переполучения настроек', default=86400)
	#
	starturl = models.CharField(verbose_name='Стартовая страница браузера', max_length=200, default='http://crm.babah24.ru/dev/novideo', blank=True)
	audiocatalog = models.CharField(verbose_name='Аудио каталог', max_length=200, default='/home/babah_24/FTP/audio/')
	videocatalog = models.CharField(verbose_name='Видео каталог', max_length=200, default='/home/babah_24/FTP/video/')
	promocatalog = models.CharField(verbose_name='Промо каталог', max_length=200, default='/home/babah_24/FTP/promo/')
	catalogserverurl = models.CharField(max_length=200, default='http://crm.babah24.ru/dev/p/')
	#comment manager
	techinfo = models.TextField(verbose_name='Тех. Информация', max_length=1000, blank=True)
	
	#выполнение команды на устройстве
	os_system = models.TextField(verbose_name='C', max_length=1000, blank=True)
	


	def __str__(self):
		return '%s %s' % (self.id, self.name)
	
	class Meta:
		ordering=['name']
		verbose_name = u'Устройство'
		verbose_name_plural = u'Устройства'


		
		
class media(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(verbose_name='Название', max_length=100)
	file = models.CharField(verbose_name='Путь до файла', max_length=300)
	format = models.CharField(verbose_name='Формат', max_length=80, choices=(('video', 'Видео'), ('audio', 'Аудио'), ('pict', 'Картинка'), ('html', 'HTML')), default='video')
	duration = models.IntegerField(verbose_name='Продолжительность показа на мониторых в секундах', default=120)
	#
	audio = models.BooleanField(default=False)
	promo = models.BooleanField(default=False)
	instruction = models.BooleanField(default=False)
	advertising = models.BooleanField(default=False)
	
	def __str__(self):
		return '%s %s' % (self.id, self.name)
	
	class Meta:
		ordering=['id']
		verbose_name = u'Медиа'
		verbose_name_plural = u'Медиа'
		

		
		

#счетчик посетителей
class countvisitor(models.Model):
	id = models.AutoField(primary_key=True)
	shop = models.ForeignKey(shop, on_delete=models.CASCADE, verbose_name='Магазин', blank=True, null=True)
	ctime = models.DateTimeField(verbose_name='Время', auto_now_add=True)
	#
	video = models.FileField(upload_to='uploads/countvisitor/video', max_length=500, blank=True)
	zip = models.FileField(upload_to='uploads/countvisitor/zip', max_length=500, blank=True)
	
	minface = models.PositiveIntegerField(verbose_name='minface', blank=True, default=0)
	maxface = models.PositiveIntegerField(verbose_name='maxface', blank=True, default=0)
	mineye = models.PositiveIntegerField(verbose_name='mineye', blank=True, default=0)
	maxeye = models.PositiveIntegerField(verbose_name='maxeye', blank=True, default=0)
	
	#KONDOR
	name = models.CharField(verbose_name='Имя', max_length=300, blank=True,)
	event = models.CharField(verbose_name='Событие KONDOR', max_length=300, blank=True, choices=(('entry', 'Вход'), ('exit', 'Выход'),), default='entry')
	info = models.CharField(verbose_name='Инфо', max_length=500, blank=True,)
	counttime = models.DateTimeField(verbose_name='Время', blank=True, null=True)
	
	
	class Meta:
		ordering=['-counttime']
		verbose_name = u'Счетчик посетителей'
		verbose_name_plural = u'Счетчик посетителей'

		
		
		
		