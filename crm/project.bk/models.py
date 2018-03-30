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

def make_upload_projectfile(instance, filename):
    category = instance.__class__.__name__ #имя модели, каталог категория
    fileext = re.compile(r'^.*\.(?P<ext>\w+)$').match(filename).group('ext')
    filename = id_generator()
    return u"uploads/%s/%s" % (category, '%s.%s' % (filename, fileext))

class projectpict(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    pict = models.ImageField(verbose_name=u'Картинка', upload_to=make_upload_path, max_length=500)
    pict20 = ImageSpecField(source='pict', processors=[ResizeToFit(20, 20)], format='PNG', options={'quality': 95})
    pict40 = ImageSpecField(source='pict', processors=[ResizeToFit(40, 40)], format='PNG', options={'quality': 95})
    desc = models.CharField(verbose_name='Описание картинки', max_length=255, blank=True)

class projectfile(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    sourcefile = models.FileField(verbose_name='Файл', upload_to=make_upload_projectfile, max_length=500)
    desc = models.CharField(verbose_name='Описание файла', max_length=255, blank=True)

class projectcomment(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(User)
    value = models.TextField(verbose_name='Комментарии')
    pict = models.ManyToManyField(projectpict, blank=True)
    file = models.ManyToManyField(projectfile, blank=True)

MLIST = (
    ('created', 'Создан'),
    ('archived', 'В архиве')
)

class project(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(verbose_name='Название', max_length=200)
    status = models.CharField(verbose_name='Статус', max_length=30, choices=MLIST, default='created')
    desc = models.TextField(verbose_name='Описание проекта',)
    executor = models.ManyToManyField(profileuser, verbose_name='Исполнитель', related_name='project_executor')
    plansum = models.FloatField(verbose_name='Бюджет проекта')
    user = models.ForeignKey(User, blank=True, null=True)
    pict = models.ManyToManyField(projectpict, blank=True)
    file = models.ManyToManyField(projectfile, blank=True)
    projectcomment = models.ManyToManyField(projectcomment, blank=True)
    
    def __unicode__(self):
        return '%s %s' % (self.id, self.name)

class projectstep(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    projectstep = models.ForeignKey('self', verbose_name='Этап', blank=True, null=True, related_name='projectstep_projectstep')
    project = models.ForeignKey(project)
    #user = models.ForeignKey(User)
    name = models.CharField(verbose_name='Имя этапа', max_length=200)
    executor = models.ManyToManyField(profileuser, verbose_name='Исполнитель', related_name='projectstep_executor')
    cdate = models.DateTimeField(verbose_name='Дата начала этапа', auto_now_add=True)
    edate = models.DateField(verbose_name='Дедлайн', default=timezone.now)
    desc = models.TextField(verbose_name='Описание этапа', blank=True) 
    pict = models.ManyToManyField(projectpict, blank=True)
    file = models.ManyToManyField(projectfile, blank=True)
    projectcomment = models.ManyToManyField(projectcomment, blank=True)
    status = models.BooleanField(verbose_name='Активен',default=True)

    def __unicode__(self):
        return '%s %s' % (self.id, self.name)

    class Meta:
        ordering=['-id']
        verbose_name = u'Список этапов'
        verbose_name_plural = u'Список этапов'

