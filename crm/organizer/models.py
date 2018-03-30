#-*- coding: utf-8 -*-

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

# Create your models here.
class organizer(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(verbose_name='Имя записи', max_length=50)
	ctime = models.DateTimeField(verbose_name='Время записи', auto_now_add=True)
	stime = models.DateTimeField(verbose_name='Старт', default=timezone.now)
	etime = models.DateTimeField(verbose_name='Окончание', blank=True, null=True)
	desc = models.TextField(verbose_name='Описание', max_length=200)
	#
	icon = models.CharField(verbose_name='Иконка', max_length=100, default='fa-info')
	classname = models.CharField(verbose_name='className', max_length=100, default='bg-color-darken')
	
	
	
	
	