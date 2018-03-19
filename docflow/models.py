from django.db import models
from django.contrib.auth.models import User


from dj.views import *
from django.utils import timezone
from panel.models import profileuser
from acl.models import *
from acl.views import *
from node.models import kontragent


class docflow_category(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	name = models.CharField(verbose_name='Название', max_length=200)
	
	def __str__(self):
		return '%s %s' % (self.id, self.name)
		
	class Meta:
		ordering=['id']

CLIST = (
	('created', 'Создан'),
	('approved', 'Утвержден'),
)

class cash_payment_voucher(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	name = models.CharField(verbose_name='Основание', max_length=255, blank=True, null=True)
	sum = models.FloatField(verbose_name='Выданная сумма')
	user = models.ForeignKey(profileuser, on_delete=models.CASCADE, verbose_name='Кто выдал')
	addressee = models.ForeignKey(profileuser, on_delete=models.CASCADE, verbose_name='Кому выдана (сотрудник)',related_name='addressee', blank=True, null=True)
	kontragent = models.ForeignKey(kontragent, on_delete=models.CASCADE, verbose_name='Кому выдана (контрагент)',related_name='kontragent', blank=True, null=True)
	category = models.ForeignKey(docflow_category, on_delete=models.CASCADE, verbose_name='Категория ордера')
	comment = models.TextField(verbose_name='Комментарии', blank=True, null=True)
	ctime = models.DateTimeField(verbose_name='Дата и время написания', auto_now_add=True)
	status = models.CharField(verbose_name='Статус', max_length=300, choices=CLIST, default='created')

	def __str__(self):
		return '%s %s' % (self.id, self.name)
		
	class Meta:
		ordering=['id']

class docflowfile(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	sourcefile = models.FileField(verbose_name='Файл', upload_to=make_upload_file, max_length=500)
	name = models.CharField(verbose_name='Описание файла', max_length=255, blank=True)
	voucher = models.ForeignKey(cash_payment_voucher, on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return '%s %s' % (self.id, self.name)

	class Meta:
		ordering=['-id']
