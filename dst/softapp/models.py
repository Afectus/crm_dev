from django.db import models
from datetime import datetime
from dj.views import make_upload_file
from django.contrib.auth.models import User

class softs(models.Model):
	"""Модель для банеров"""
	id = models.AutoField(primary_key=True, unique=True)
	createuser = models.ForeignKey(User, related_name='softs_createuser',on_delete=models.CASCADE, blank=True, null=True,)
	updateuser = models.ForeignKey(User, related_name='softs_updateuser',on_delete=models.CASCADE, blank=True, null=True,)
	ctime = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True,)
	utime = models.DateTimeField(verbose_name='Дата обновления объекта', auto_now=True,)
	name = models.CharField(verbose_name='Название', max_length=100)
	desc = models.TextField(verbose_name = "Описание программы", max_length=1000, blank=True, null=True,)
	soft = models.FileField(upload_to=make_upload_file, verbose_name = "Загружаеммая программа")

	def clean(self):
		self.utime = datetime.now()

	def __str__(self):
		return u'%s' % (self.id)
