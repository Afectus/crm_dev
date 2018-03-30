# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from .models import *
from acl.models import *
from acl.views import *

# Create your models here.
class accountstorage(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	name = models.CharField(verbose_name='Название', max_length=500)
	login = models.CharField(verbose_name='Логин', max_length=200)
	password = models.CharField(verbose_name='Пароль', max_length=200)
	comment = models.TextField(verbose_name='Комментарии', max_length=1000, blank=True)
	aclu = models.ManyToManyField(aclu, verbose_name='Права', limit_choices_to={'aclobject__objectid': 'accountstorage'}, blank=True)
	
	def __str__(self):
		return '%s %s' % (self.id, self.name)
