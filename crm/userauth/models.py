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

from node.models import *



class userloginblockdb(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id',)
	user = models.CharField(max_length=100, verbose_name='логин::пароль', blank=True)
	ip = models.CharField(verbose_name='IP адресс', max_length=100, blank=True)
	starttime = models.DateTimeField(auto_now_add=True, verbose_name='Время начала блокировки')
	blocktime = models.IntegerField(verbose_name='сколько секунд блокировать')
	
	def __str__(self):
		return u'%s' % self.id

