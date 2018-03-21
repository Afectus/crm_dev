# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

import string
import random
import re
from dj.views import *
from django.utils import timezone
from panel.models import profileuser

def make_upload_corpmail(instance, filename):
	category = instance.__class__.__name__ #имя модели, каталог категория
	fileext = re.compile(r'^.*\.(?P<ext>\w+)$').match(filename).group('ext')
	filename = id_generator()
	return u"uploads/%s/%s" % (category, '%s.%s' % (filename, fileext))

SLIST = (
	('created', 'Создан'),
	('read','Прочитанный'),
	('archived', 'В архиве')
)

class corpmail(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	name = models.CharField(verbose_name='Тема', max_length=200)
	desc = models.CharField(verbose_name='Содержание', max_length=3000, blank=True, null=True)
	status = models.CharField(verbose_name='Статус', max_length=30, choices=SLIST, default='created')
	user = models.ForeignKey(profileuser, on_delete=models.CASCADE, verbose_name='Отправитель', related_name='Sender')
	addressee = models.ForeignKey(profileuser, on_delete=models.CASCADE, verbose_name='Адресат', related_name='Addressee')
	cdate = models.DateTimeField(verbose_name='Дата и время написания', auto_now_add=True)
	corpmail = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Родитель', blank=True, null=True, related_name='corpmail_parent')
	
	def __str__(self):
		return '%s' % (self.id)

	class Meta:
		ordering=['-id']
	
class corpmailfile(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	name = models.CharField(verbose_name='Название', max_length=200, blank=True, null=True)
	sourcefile = models.FileField(verbose_name='Файл', upload_to=make_upload_corpmail, max_length=500)
	corpmail = models.ForeignKey(corpmail, on_delete=models.CASCADE, blank=True, null=True)
	# desc = models.CharField(verbose_name='Описание', max_length=500, blank=True, null=True)
