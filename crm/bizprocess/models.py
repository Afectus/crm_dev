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


class bizplist(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	name = models.CharField(verbose_name='Название', max_length=200)
	#parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.CASCADE, blank=True, null=True)
	#cdate = models.DateField(verbose_name='date', default=timezone.now)
	
	def __str__(self):
		return '%s %s' % (self.id, self.name)

	class Meta:
		ordering=['id']
		verbose_name = u'bizplist'
		verbose_name_plural = u'bizplist'

class bizpstep(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	name = models.CharField(verbose_name='Название', max_length=200)
	process = models.ForeignKey(bizplist, verbose_name='Процесс', on_delete=models.CASCADE)
	parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.CASCADE, blank=True, null=True)
	sort = models.PositiveIntegerField(verbose_name='Сортировка', default=0)
	#cdate = models.DateField(verbose_name='date', default=timezone.now)
	#
	head = models.CharField(verbose_name='Отвественный', max_length=500, blank=True)
	#executor = models.CharField(verbose_name='Исполнитель', max_length=500, blank=True)
	bizpstepexecutor = models.CharField(verbose_name='Исполнитель', max_length=500, blank=True)
	desc = models.TextField(verbose_name='Описание', max_length=10000, blank=True)
	fulltext = models.TextField(verbose_name='Полный текст', max_length=30000, blank=True)
	
	def __str__(self):
		return '%s %s' % (self.id, self.name)

	class Meta:
		ordering=['id', 'sort',]
		verbose_name = u'bizpstep'
		verbose_name_plural = u'bizpstep'

