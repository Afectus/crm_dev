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
from panel.models import *


class aclobject(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	name = models.CharField(verbose_name=u'Название', max_length=200)
	objectid = models.CharField(verbose_name=u'ID объекта', max_length=200)
	
	def __str__(self):
		return u'%s %s %s' % (self.id, self.name, self.objectid)

	class Meta:
		ordering=['-id']
		verbose_name = u'aclobject'
		verbose_name_plural = u'aclobject'


grantchoice=(('A', 'All'), ('L', 'Список'), ('R', 'Чтение'), ('C', 'Создание'), ('U', 'Редактирование'),)

class aclu(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	#name = models.CharField(verbose_name=u'Название', max_length=200)
	status = models.BooleanField(verbose_name='Статус', default=True)
	#
	aclobject = models.ForeignKey(aclobject, on_delete=models.CASCADE)
	#users = models.ManyToManyField(profileuser, verbose_name='Пользователи', blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
	type = models.CharField(verbose_name='Права', max_length=80, choices=grantchoice, default='R')
	#
	ctime = models.DateTimeField(verbose_name='Время начало', blank=True, null=True)
	etime = models.DateTimeField(verbose_name='Время конец', blank=True, null=True)
	
	def __str__(self):
		return u'%s %s (%s-%s)' % (self.aclobject.name, self.user, self.type, self.get_type_display())

	class Meta:
		ordering=['-id']
		verbose_name = u'aclu'
		verbose_name_plural = u'aclu'		

		
class aclg(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	#name = models.CharField(verbose_name=u'Название', max_length=200)
	status = models.BooleanField(verbose_name='Статус', default=True)
	#
	aclobject = models.ForeignKey(aclobject, on_delete=models.CASCADE)
	group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Группа')
	type = models.CharField(verbose_name='Права', max_length=80, choices=grantchoice, default='R')
	#
	ctime = models.DateTimeField(verbose_name='Время начало', blank=True, null=True)
	etime = models.DateTimeField(verbose_name='Время конец', blank=True, null=True)
	
	def __str__(self):
		return u'%s' % (self.id)

	class Meta:
		ordering=['-id']
		verbose_name = u'aclg'
		verbose_name_plural = u'aclg'	