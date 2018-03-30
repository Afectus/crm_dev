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

from dj.views import *

from node.models import *

class imagebase(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	desc = models.CharField(verbose_name='Описание', max_length=100, blank=True)
	sort = models.PositiveIntegerField(verbose_name='Сортировка', default=100)
	#
	pict = models.ImageField(verbose_name='Картинка', upload_to=make_upload_path, max_length=500)
	pictoriginal = ImageSpecField(source='pict', format='PNG', options={'quality': 75})
	pict40 = ImageSpecField(source='pict', processors=[ResizeToFill(40, 40)], format='PNG', options={'quality': 75})
	pict100 = ImageSpecField(source='pict', processors=[ResizeToFill(100, 100)], format='PNG', options={'quality': 75})
	pict200 = ImageSpecField(source='pict', processors=[ResizeToFill(200, 200)], format='PNG', options={'quality': 75})
	pict300 = ImageSpecField(source='pict', processors=[ResizeToFit(300, 300)], format='PNG', options={'quality': 75})
	pict400 = ImageSpecField(source='pict', processors=[ResizeToFill(400, 400)], format='PNG', options={'quality': 75})
	pict500 = ImageSpecField(source='pict', processors=[ResizeToFit(500, 500)], format='PNG', options={'quality': 75})
	pict800 = ImageSpecField(source='pict', processors=[ResizeToFit(1024, 2000)], format='PNG', options={'quality': 75})


	def __str__(self):
		return u'%s %s' % (self.id, self.desc)

	class Meta:
		ordering=['id']
		verbose_name = u'Картинка'
		verbose_name_plural = u'Картинки'
	
def delete_imagebase_pict(sender, **kwargs):
	mf = kwargs.get("instance")
	mf.pict.delete(save=False)
	
post_delete.connect(delete_imagebase_pict, imagebase)
