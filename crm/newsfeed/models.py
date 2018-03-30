# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from PIL import Image
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit, ResizeToFill, SmartResize, Transpose, Adjust
import string
import random
import re
from dj.views import *
from django.utils import timezone
from panel.models import profileuser

class news(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	name = models.CharField(verbose_name='Название', max_length=200)
	user = models.ForeignKey(profileuser, verbose_name='Автор', on_delete=models.CASCADE) 
	cdate = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
	# readers = models.ManyToManyField(profileuser, verbose_name='Адресаты',related_name='Адресаты')
	text = models.TextField(verbose_name='Текст', max_length=30000)
	
	def __str__(self):
		return '%s %s' % (self.id, self.name)
		
	class Meta:
		ordering=['-cdate']

class newspicture(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	news = models.ForeignKey(news, on_delete=models.CASCADE)
	pict = models.ImageField(verbose_name=u'Картинка', upload_to=make_upload_path, max_length=500)
	pict20 = ImageSpecField(source='pict', processors=[ResizeToFit(20, 20)], format='PNG', options={'quality': 95})
	pict40 = ImageSpecField(source='pict', processors=[ResizeToFit(40, 40)], format='PNG', options={'quality': 95})
	desc = models.CharField(verbose_name='Описание картинки', max_length=255, blank=True)

