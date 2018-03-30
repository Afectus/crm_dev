# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# from notify.models import *

# названия шаблонов по умолчанию
DEFAULT_NAMES = (
	('ttppe', 'Шаблон при публикации проекта для исполнителей проекта'),
	('ttppc', 'Шаблон при публикации проекта для общего чата'),
	('ttape', 'Шаблон при переводе проекта в архив для исполнителей проекта'),
	('ttapc', 'Шаблон при переводе проекта в архив для общего чата'),
	('ttcpe', 'Шаблон при изменении проекта для исполнителей проекта'),
	('ttcpc', 'Шаблон при изменении проекта для общего чата'),
	('ttacp', 'Шаблон при добавлении комментариев в проект'),
	('ttapse', 'Шаблон при добавлении этапа в проект для исполнителей'),
	('ttapsc', 'Шаблон при добавлении этапа в проект для общего чата'),
	('ttcpse', 'Шаблон при изменении этапа проекта для исполнителей'),
	('ttcpsc', 'Шаблон при изменении этапа проекта для общего чата'),
	('ttacps', 'Шаблон при добавлении комментариев в этап проекта'),
	('tteps', 'Шаблон при завершении этапа проекта')
)

class telegramtemplate(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	name = models.CharField(verbose_name='id шаблона', max_length=200)
	desc = models.CharField(verbose_name='Описание', max_length=200, blank=True)
	message = models.TextField(verbose_name='Шаблон')
	# user = models.ForeignKey(User, blank=True, null=True)
	# handler = models.ForeignKey(notifyhandler, blank=True, null=True)

	# status = models.BooleanField(verbose_name='Статус', default=False)
	# sort = models.PositiveIntegerField(verbose_name='Приоритет', default=100)
	
	def __str__(self):
		return '%s %s' % (self.id, self.name)

	class Meta:
		ordering=['id']
		verbose_name = u'Список шаблонов для telegram-рассылки'
		verbose_name_plural = u'Список шаблонов для telegram-рассылки'

