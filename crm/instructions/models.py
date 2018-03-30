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

def make_upload_instructionfile(instance, filename):
	category = instance.__class__.__name__ #имя модели, каталог категория
	fileext = re.compile(r'^.*\.(?P<ext>\w+)$').match(filename).group('ext')
	filename = id_generator()
	return u"uploads/%s/%s" % (category, '%s.%s' % (filename, fileext))

class instructions(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	name = models.CharField(verbose_name='Название', max_length=200)
	addressee = models.CharField(verbose_name='Кому предназначена', max_length=500, blank=True)
	file = models.FileField(verbose_name='Файл', upload_to=make_upload_instructionfile, max_length=500)
	#
	fulltext = models.TextField(verbose_name='Текст', max_length=30000, blank=True)
	
	def __str__(self):
		return '%s %s' % (self.id, self.name)
		
	class Meta:
		ordering=['-id']
		#verbose_name = u'aclg'
		#verbose_name_plural = u'aclg'	