# -*- coding: utf-8 -*-
from django.db import models

from django.db.models.signals import post_delete, post_save
from django.db.models.signals import pre_delete

from django.utils import timezone

from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User, Group

from node.models import *

orderstatuschoice=(
	('wait', 'Ожидает'),
	('accept', 'Принят/собрали'),
	('acceptcall', 'Принят/созвонились'),
	('acceptcheck', 'Принят/чек'),
	('pickup', 'Самовывоз'),
	('kupilsam', 'Купил сам'),
	('inway', 'У курьера'),
	('success', 'Доставлен'), #уходит в архив
	('zabrali', 'Забрали'), #уходит в архив
	('cancel', 'Отменен'), #уходит в архив
	)
	
	
orderareac=(
	('a', 'Железнодорожный'),
	('b', u'Кировский'),
	('c', u'Ленинский'),
	('d', u'Октябрьский'),
	('e', u'Свердловский'),
	('f', u'Советский'),
	('g', u'Центральный'),
	)

class order(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	bitrixorderid = models.CharField(verbose_name=u'# заказа Битрикс', max_length=100, blank=True)
	ctime = models.DateTimeField(verbose_name='Дата покупки', auto_now_add=True)
	status = models.CharField(verbose_name='Статус', max_length=80, choices=orderstatuschoice, default='wait')
	ordersum = models.FloatField(verbose_name='Цена', help_text='Сумма заказа', default=0)
	#
	uname = models.CharField(verbose_name='Имя покупателя', max_length=50, blank=True)
	phone = models.CharField(verbose_name='Телефон', max_length=20)
	city = models.CharField(verbose_name='Город', max_length=100, blank=True, choices=(('3912', u'Красноярск'), ('39151', u'Ачинск'),))
	area = models.CharField(verbose_name='Район', max_length=100, blank=True, choices=orderareac,)
	addr = models.CharField(verbose_name='Адрес доставки', max_length=300, blank=True)
	discont = models.CharField(verbose_name='Дисконтная карта', max_length=300, blank=True)
	comment = models.TextField(verbose_name='Комментарий', max_length=300, blank=True)
	terminal = models.BooleanField(verbose_name='Терминал', default=False)
	#
	cart = models.TextField(verbose_name='Корзина', max_length=10000, blank=True)
	sourcejson = models.TextField(verbose_name='json', max_length=10000, blank=True)
	#поля для менеджера
	timecomment = models.CharField(verbose_name='Время', max_length=1000, blank=True)
	sum = models.FloatField(verbose_name='Сумма', default=0)
	sumreturn = models.FloatField(verbose_name='Сдача', default=0)
	total = models.FloatField(verbose_name='Итого', default=0)


	def __str__(self):
		return '%s %s %s' % (self.id, self.uname, self.phone)

	class Meta:
		ordering=['-id']
		verbose_name = u'Ордер'
		verbose_name_plural = u'Ордер'

class ordercartlist(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	order = models.ForeignKey(order, on_delete=models.CASCADE, verbose_name='Заказ')
	ctime = models.DateTimeField(db_index=True, verbose_name='Время', auto_now_add=True)
	goods = models.ForeignKey(goods, on_delete=models.CASCADE, verbose_name='Товар', null=True, blank=True)
	name = models.CharField(verbose_name='Наименование', max_length=300, blank=True)
	price = models.FloatField(verbose_name='Цена', default=0)
	col = models.FloatField(verbose_name='Количество', default=0)
	discount_price = models.FloatField(verbose_name='discount_price', default=0)
	unit = models.CharField(verbose_name='Единица', max_length=300, blank=True)
	currency = models.CharField(verbose_name='Валюта', max_length=300, blank=True)
	order_price = models.CharField(verbose_name='order_price',  max_length=300, blank=True)
	comment = models.TextField(verbose_name='Комментарий', max_length=300, blank=True)

	def __str__(self):
		return u'%s' % (self.id)

	class Meta:
		ordering=['-id']
		verbose_name = u'Заказ: корзина'
		verbose_name_plural = u'Заказ: корзина'	


	
	
	

eventchoice=(
	('add', 'Создан'), 
	('sms', 'Отправлено СМС'), (
	'update', 'Обновлен'), 
	('accept', 'Принят менеджером'), 
	('edit', 'Редактирование заказа'), 
	('statusedit', 'Изминение статуса заказа'), 
	('success', 'Обработан'),
	('other', 'Другие операции'),
	)
	
class orderevent(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', blank=True, null=True)
	order = models.ForeignKey(order, on_delete=models.CASCADE, verbose_name='Заказ', blank=True, null=True)
	ctime = models.DateTimeField(verbose_name='Время', auto_now_add=True)
	event = models.CharField(verbose_name='Событие', max_length=200, choices=eventchoice)
	comment = models.TextField(verbose_name='Комментарий', max_length=500, blank=True)
	info = models.TextField(verbose_name='Тех.Информация', max_length=1000, blank=True)


	def __str__(self):
		return '%s %s %s %s' % (self.id, self.order, self.ctime, self.event)

	class Meta:
		ordering=['ctime']
		verbose_name = u'Ордер события'
		verbose_name_plural = u'Ордер события'
		

schedulechoice=((1, 'Пн'), (2, 'Вт'), (3, 'Ср'), (4, 'Чт'), (5, 'Пт'), (6, 'Сб'), (7, 'Вс'),)

class ordermanager(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
	schedule = models.PositiveIntegerField(verbose_name='График', choices=schedulechoice)
	sort = models.PositiveIntegerField(verbose_name='Приоритет', default=0)
	shift = models.BooleanField(verbose_name='Посменный график работы', default=False)
	handler = models.CharField(verbose_name='Обработчик', max_length=200, choices=(('sms4b', 'sms4b'), ('telegram', 'Telegram'),), default='sms4b')

	def __str__(self):
		return u'%s %s %s' % (self.id, self.user, self.sort)

	class Meta:
		ordering=['-id']
		verbose_name = u'Менеджер интернет магазина'
		verbose_name_plural = u'Менеджер интернет магазина'