# -*- coding: utf-8 -*-
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
import md5


def make_upload_doc(instance, filename):
	category = instance.__class__.__name__ #имя модели, каталог категория
	fileext = re.compile(r'^.*\.(?P<ext>\w+)$').match(filename).group('ext')
	filename = id_generator()
	return u"uploads/%s/%s" % (category, '%s.%s' % (filename, fileext))		


class doc(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	name = models.CharField(verbose_name='Название', max_length=200)
	namea = models.CharField(verbose_name='Название выбор', max_length=80, choices=((u'a', u'a'), (u'b', u'b'),), blank=True)
	user = models.ForeignKey(User, verbose_name='Пользователь')
	parent = models.ForeignKey('self', verbose_name='Родитель', limit_choices_to={'parent__isnull': True, 'status': True, }, blank=True, null=True)
	status = models.BooleanField(verbose_name='Статус', default=True) 
	desc = models.TextField(verbose_name='Полезная информация', max_length=10000, blank=True)
	valueint = models.IntegerField(verbose_name='Количество', validators=[MinValueValidator(0), MaxValueValidator(100000)], default=0,)
	valuepint = models.PositiveIntegerField(verbose_name=u'valuepint', default=0)
	utime = models.DateTimeField(verbose_name='Время последнего обновления', default=timezone.now)
	cdate = models.DateField(verbose_name='Дата', auto_now_add=True)
	md = models.DateField(verbose_name='индекс, денормализация)', blank=True, null=True,)
	mtm = models.ManyToManyField(MODELNAME, verbose_name='mtm', blank=True)
	price = models.FloatField(verbose_name='Цена', default=0)
	#
	pict = models.ImageField(verbose_name=u'Картинка', upload_to=make_upload_path, max_length=300, blank=True)
	pict1 = ImageSpecField(source='pict', processors=[ResizeToFill(230, 200)], format='PNG', options={'quality': 75})
	
	#
	sourcefile = models.FileField(upload_to=make_upload_doc, max_length=500, blank=True)
	
	@property
	def gethidephone(self):
		return hidephone(self.phone)
	
	def __str__(self):
		return '%s %s' % (self.id, self.name)

	class Meta:
		ordering=['id']
		verbose_name = u'Склад'
		verbose_name_plural = u'Склады'

@receiver(post_save, sender = doc)
def mdindexsave(instance, **kwargs):
	try:
		doc.objects.filter(id=instance.id).update(mdindexsave=instance.cdate.strftime("%d%m"))
	except:
		doc.objects.filter(id=instance.id).update(mdindexsave='none')

def delete_pict(sender, **kwargs):
	mf = kwargs.get("instance")
	mf.pict.delete(save=False)
post_delete.connect(delete_pict, pict)
	

