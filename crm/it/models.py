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


def make_upload_tech(instance, filename):
	category = instance.__class__.__name__ #имя модели, каталог категория
	filename = id_generator()
	return u"uploads/%s/%s" % (category, '%s.zip' % filename)


class techinfo(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(verbose_name='Название', max_length=100)
	desc = models.TextField(verbose_name='Текст', max_length=1000, blank=True)
	pict = models.ImageField(verbose_name=u'Картинка', upload_to=make_upload_path, max_length=300, blank=True)
	pict1 = ImageSpecField(source='pict', processors=[ResizeToFill(500, 500)], format='PNG', options={'quality': 95})
	
	techfile = models.FileField(verbose_name=u'Файл, ТОЛЬКО ZIP АРХИВ', upload_to=make_upload_tech, max_length=500, blank=True)

	def __str__(self):
		return '%s %s' % (self.id, self.name)
	
	class Meta:
		ordering=['-id']
		verbose_name = u'Тех. информация'
		verbose_name_plural = u'Тех. информация'	



class usermanual(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(verbose_name='Название', max_length=100)
	desc = models.TextField(verbose_name='Текст', max_length=1000, blank=True)
	#pict = models.ImageField(verbose_name=u'Картинка', upload_to=make_upload_path, max_length=300, blank=True)
	#pict1 = ImageSpecField(source='pict', processors=[ResizeToFill(500, 500)], format='PNG', options={'quality': 95})
	
	#techfile = models.FileField(verbose_name=u'Файл, ТОЛЬКО ZIP АРХИВ', upload_to=make_upload_tech, max_length=500, blank=True)

	def __str__(self):
		return '%s %s' % (self.id, self.name)
	
	class Meta:
		ordering=['-id']
		verbose_name = u'Документация для пользователей'
		verbose_name_plural = u'Документация для пользователей'
		
		