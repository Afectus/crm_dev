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



class panelmenu(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	name = models.CharField(verbose_name='Название', max_length=100)
	icon = models.CharField(verbose_name='Иконка', max_length=100, blank=True, default='<i class="fa fa-folder" aria-hidden="true"></i>')
	url = models.CharField(verbose_name='Путь', max_length=100, default='#')
	parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Родитель', null=True, blank=True, limit_choices_to={'parent__isnull': True,})
	sort = models.PositiveIntegerField(verbose_name='Сортировка', default=0)
	role = models.CharField(verbose_name='Роль', max_length=80, choices=(('all', 'Все'), ('kassir', 'Кассир'), ('office', 'Офис'),), default='all')
	comment= models.TextField(verbose_name=u'Комментарий', help_text=u'Комментарий', max_length=30000, blank=True)

	def __str__(self):
		return u'%s %s' % (self.id, self.name)

	class Meta:
		ordering=['-sort']
		verbose_name = u'Меню'
		verbose_name_plural = u'Меню'




def get_normal_name(self):
	return '%s %s (%s)' % (self.first_name, self.last_name, self.username)

User.add_to_class("__unicode__", get_normal_name)
		
#профайл пользователя наследование от User
class profileuser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='user') #OneToOneField is unique=True
	phone = models.CharField(verbose_name='Телефон', max_length=15, blank=True)
	#поля которые мы удалим после полного переноса на анкеты
	shop = models.ManyToManyField(shop, verbose_name='Магазины', blank=True)
	shopstock = models.ManyToManyField(shopstock, verbose_name='Магазин/склад', blank=True)
	#
	email = models.CharField(verbose_name='Электронная почта', max_length=100, blank=True)
	#анкета
	bday = models.DateField(verbose_name='Дата рождения', help_text='формат: dd.mm.yyyy', null=True, blank=True)
	status = models.CharField(verbose_name='Статус', max_length=80, choices=(('on', 'Действующий'), ('off', 'Уволен'), ('wait', 'Резерв'), ('drop', 'Черный список')), default='on')
	role = models.CharField(verbose_name='Роль', max_length=80, choices=(('kassir', 'Кассир'), ('office', 'Офис'), ('system', 'Служебные')), default='kassir')
	#
	photo = models.ImageField(verbose_name=u'Фото', upload_to=make_upload_path, max_length=300, blank=True)
	photosmall = ImageSpecField(source='photo', processors=[ResizeToFill(200, 200)], format='PNG', options={'quality': 75})
	
	#for template mail
	position = models.CharField(verbose_name='Отдел for template mail', max_length=200, blank=True)
	phonemobile = models.CharField(verbose_name='Мобильный телефон for template mail', max_length=200, blank=True)
	phonework = models.CharField(verbose_name='Рабочий телефон for template mail', max_length=200, blank=True)
	address = models.CharField(verbose_name='Адрес for template mail', max_length=300, blank=True)
	
	#personal data
	passport = models.CharField(verbose_name='Паспорт серия номер', max_length=200, blank=True)
	propiska = models.TextField(verbose_name='Прописка', max_length=1000, blank=True)
	
	edu = models.CharField(verbose_name='Образование', max_length=80, choices=(('a', 'Общее'), ('b', 'Высшее'), ('c', 'Средние'),), default='a')
	diplom = models.TextField(verbose_name='Диплом об образовании', max_length=1000, blank=True)
	nprikaza = models.TextField(verbose_name='Номер приказа о принятии на работу', max_length=1000, blank=True)
	uvolen = models.TextField(verbose_name='Причина увольнения', max_length=1000, blank=True)
	funcworker = models.TextField(verbose_name='Исполнительные функции', max_length=1000, blank=True)
	inn= models.CharField(verbose_name='ИНН', max_length=200, blank=True)
	snils= models.CharField(verbose_name='СНИЛС', max_length=200, blank=True)
	message = models.TextField(verbose_name='Общая информация', help_text='Общая информация', max_length=100000, blank=True)
	
	telegram = models.CharField(verbose_name='telegram', max_length=500, blank=True)

	def __str__(self):
		return '%s %s (%s)' % (self.user.first_name, self.user.last_name, self.user.username)

	class Meta:
		ordering=['-id']
		verbose_name = u'Профайл пользователя'
		verbose_name_plural = u'Профайл пользователя'



#список детей для печати или обзвона
class childbook(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	ctime = models.DateTimeField(verbose_name=u'Дата', auto_now_add=True)
	child = models.ForeignKey(child, on_delete=models.CASCADE, verbose_name=u'Ребенок')
	
	def __str__(self):
		return u'%s' % (self.id)

	class Meta:
		ordering=['-id']
		verbose_name = u'Список детей'
		verbose_name_plural = u'Список детей'	
		
		
		
		
#баги товара
class goodfix(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	goods = models.ForeignKey(goods, on_delete=models.CASCADE, verbose_name='Товар', blank=True, null=True)
	status = models.CharField(verbose_name='Статус', max_length=80, choices=(('open', 'Открыто'), ('close', 'Закрыто'),), default='open')
	priority = models.CharField(verbose_name='Важность', max_length=80, choices=(('fast', 'Срочно'), ('normal', 'Обычно'), ('slow', 'Не срочно')), default='normal')
	ctime = models.DateTimeField(verbose_name='Дата', auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
	#
	link = models.CharField(verbose_name=u'Ссылка на страницу товара', help_text='', max_length=500, blank=True)
	name = models.CharField(verbose_name=u'Название товара', help_text='Название, ID, Артикул или др.', max_length=200, blank=True)
	message= models.TextField(verbose_name=u'Комментарий', help_text=u'Комментарий', max_length=30000)
	
	def __str__(self):
		return u'%s %s %s %s %s' % (self.id, self.status, self.ctime, self.user, self.name)

	class Meta:
		ordering=['-status']
		verbose_name = u'Корректировка позиции товара'
		verbose_name_plural = u'Корректировка позиций товара'
		
		
		
#План продаж по магазинам
class saleplanshop(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	status = models.BooleanField(verbose_name='Статус', default=True) 
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Кто задал план')
	name = models.CharField(verbose_name=u'Название', help_text='Название плана', max_length=200, blank=True)
	value = models.FloatField(verbose_name='Сумма')
	shop = models.ForeignKey(shop, on_delete=models.CASCADE, verbose_name='Магазин')
	ctime = models.DateTimeField(verbose_name='Время для сортировки', auto_now_add=True)
	utime = models.DateTimeField(verbose_name='Время редактирования плана', auto_now=True)
	sdate = models.DateField(verbose_name='Период от', default=timezone.now)
	edate = models.DateField(verbose_name='Период до', default=timezone.now)
	
	def __str__(self):
		return '%s %s' % (self.status, self.value)

	class Meta:
		ordering=['-id']
		verbose_name = u'План продаж магазина'
		verbose_name_plural = u'План продаж магазина'
		
	
	

#Событие обзвон клиента
class eventcall(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Менеджер', blank=True, null=True)
	ctime = models.DateTimeField(verbose_name='Дата/Время', default=timezone.now)
	buyer = models.ForeignKey(buyer, on_delete=models.CASCADE, verbose_name='Покупатель')
	comment = models.TextField(verbose_name='Комментарий', max_length=30000)
	
	def __str__(self):
		return '%s %s' % (self.id, self.comment)

	class Meta:
		ordering=['id']
		verbose_name = u'Обзвон клиента'
		verbose_name_plural = u'Обзвон клиента'

	
	

#База изображений
class imagebase(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	ctime = models.DateTimeField(verbose_name=u'Дата', auto_now_add=True)
	title = models.CharField(verbose_name=u'Заголовок', help_text='Заголовок', max_length=200)

	#pict
	pict = models.ImageField(verbose_name=u'Картинка', upload_to=make_upload_path, max_length=300)
	pict100 = ImageSpecField(source='pict', processors=[ResizeToFit(100, 100)], format='PNG', options={'quality': 75})
	pict200 = ImageSpecField(source='pict', processors=[ResizeToFit(200, 200)], format='PNG', options={'quality': 75})
	pict300 = ImageSpecField(source='pict', processors=[ResizeToFit(300, 300)], format='PNG', options={'quality': 75})
	
	def __str__(self):
		return u'%s' % (self.id)

	class Meta:
		ordering=['-id']
		verbose_name = u'База изображений'
		verbose_name_plural = u'База изображений'		
		
		