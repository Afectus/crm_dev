# -*- coding: utf-8 -*-
from __future__ import unicode_literals
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


		
class marketing_report(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	name = models.CharField(verbose_name='Название', help_text='Название', max_length=200)
	cdate = models.DateField(verbose_name='Дата', help_text='формат: dd.mm.yyyy')
	creator = models.CharField(verbose_name='Организатор', help_text='Организатор', max_length=200)
	place = models.CharField(verbose_name='Место', help_text='Место', max_length=200)
	comment = models.TextField(verbose_name='Комментарий', help_text='Комментарий', max_length=100000)
	usepersonal = models.ManyToManyField(profileuser, verbose_name='Задействованные сотрудники')
	col = models.PositiveIntegerField(verbose_name='Количество посетителей', default=0)
	
	def __str__(self):
		return u'%s' % (self.id)

	class Meta:
		ordering=['-id']
		verbose_name = u'Маркетинг отчет'
		verbose_name_plural = u'Маркетинг отчет'	


class marketing_report_item(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	name = models.CharField(verbose_name='Название', help_text='Название', max_length=200)
	marketing_report = models.ForeignKey(marketing_report, on_delete=models.CASCADE)
	sum = models.FloatField(verbose_name='Сумма', default=0)
	comment = models.TextField(verbose_name='Комментарий', help_text='Комментарий', max_length=100000, blank=True)
	
	def __str__(self):
		return u'%s' % (self.id)

	class Meta:
		ordering=['-id']
		verbose_name = u'Маркетинг отчет - сумма'
		verbose_name_plural = u'Маркетинг отчет - сумма'		
		
		
		