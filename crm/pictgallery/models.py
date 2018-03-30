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


def make_upload_pictgallery(instance, filename):
	category = instance.__class__.__name__ #имя модели, каталог категория
	fileext = re.compile(r'^.*\.(?P<ext>\w+)$').match(filename).group('ext')
	filename = id_generator()
	return u"uploads/%s/%s" % (category, '%s.%s' % (filename, fileext))

class pictgallery(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	desc = models.CharField(verbose_name='Описание картинки', max_length=255, blank=True)
	user = models.ForeignKey(profileuser, on_delete=models.CASCADE)
	pict = models.ImageField(verbose_name=u'Картинка', upload_to=make_upload_pictgallery, max_length=500)
	pict100 = ImageSpecField(source='pict', processors=[ResizeToFit(100, 100)], format='PNG', options={'quality': 95})
	pict200 = ImageSpecField(source='pict', processors=[ResizeToFit(200, 200)], format='PNG', options={'quality': 95})
	pict300 = ImageSpecField(source='pict', processors=[ResizeToFit(300, 300)], format='PNG', options={'quality': 95})
	pict400 = ImageSpecField(source='pict', processors=[ResizeToFit(400, 400)], format='PNG', options={'quality': 95})
	pict500 = ImageSpecField(source='pict', processors=[ResizeToFit(500, 500)], format='PNG', options={'quality': 95})
	pict600 = ImageSpecField(source='pict', processors=[ResizeToFit(600, 600)], format='PNG', options={'quality': 95})
	pict700 = ImageSpecField(source='pict', processors=[ResizeToFit(700, 700)], format='PNG', options={'quality': 95})
	pict800 = ImageSpecField(source='pict', processors=[ResizeToFit(800, 800)], format='PNG', options={'quality': 95})
	
	def __str__(self):
		return '%s %s' % (self.id, self.desc)