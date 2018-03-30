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


		
class workgraph(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	status = models.BooleanField(verbose_name='Статус', default=True)
	sdate = models.DateField(verbose_name='Период от', default=timezone.now)
	edate = models.DateField(verbose_name='Период до', default=timezone.now)
	user = models.ForeignKey(profileuser, on_delete=models.CASCADE, verbose_name='Сотрудник', limit_choices_to={'role': 'kassir'},)
	message= models.TextField(verbose_name=u'Текст', help_text=u'Текст', max_length=30000, blank=True)
	
	def __str__(self):
		return u'%s' % (self.id)

	class Meta:
		ordering=['-edate']
		verbose_name = u'График работы'
		verbose_name_plural = u'График работы'

		
		
		
		