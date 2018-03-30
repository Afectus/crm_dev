# -*- coding: utf-8 -*-
from django.db import models

from django.db.models.signals import post_delete, post_save
from django.db.models.signals import pre_delete

from django.utils import timezone

from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User, Group


handlerdefault=('telegram', 'Telegram')
handlerchoice=(('sms4b', 'Sms4b'), handlerdefault,)


#обработчики
class notifyhandler(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	status = models.BooleanField(verbose_name='Статус', default=True)
	name = models.CharField(verbose_name='Название', max_length=200)
	
	def __str__(self):
		return '%s %s %s' % (self.id, self.status, self.name)

	class Meta:
		ordering=['-id']
		verbose_name = u'Обработчики оповещений'
		verbose_name_plural = u'Обработчики оповещений'

#id пользователей к обработчикам
class notifyuserkey(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
	handler = models.ForeignKey(notifyhandler, on_delete=models.CASCADE, verbose_name='Обработчик')
	value = models.CharField(verbose_name='Значение', max_length=500)
	
	def __str__(self):
		return '%s %s %s' % (self.id,self.handler, self.value)

	class Meta:
		ordering=['-id']
		verbose_name = u'Ключи пользователей'
		verbose_name_plural = u'Ключи пользователей'



#очередь оповещений на отправку
class notifyqueue(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', blank=True, null=True)
	ctime = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
	during = models.BooleanField(verbose_name='В процессе', default=True)
	handler = models.ForeignKey(notifyhandler, on_delete=models.CASCADE)
	target = models.CharField(verbose_name='Цель/Адрес', max_length=500, blank=True)
	value = models.CharField(verbose_name='Сообщение', max_length=10000)
	
	def __str__(self):
		return '%s %s %s %s' % (self.id, self.ctime, self.during, self.handler)

	class Meta:
		ordering=['-id']
		verbose_name = u'Очередь оповещений'
		verbose_name_plural = u'Очередь оповещений'
		
	
