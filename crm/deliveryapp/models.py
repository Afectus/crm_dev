from django.db import models
from order.models import *
from django.contrib.auth.models import User
from datetime import datetime
tc=(
	('car', 'Автомобиль'),
	('bike', 'Велосипед'),
	('foot', 'Пешком'),
	)
	
class ts(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Собственник')
	status = models.BooleanField(verbose_name='Статус', default=True)
	type = models.CharField(verbose_name='Тип транспорта', max_length=80, choices=tc, default='car')
	name = models.CharField(verbose_name='Наименование', max_length=200)
	#
	modelinfo = models.CharField(verbose_name='Модель ТС', max_length=200, blank=True)
	#
	numinfo = models.CharField(verbose_name='Номер ТС', max_length=200, blank=True)

	def __str__(self):
		return '%s %s %s' % (self.id, self.name, self.user)

	class Meta:
		ordering=['-id']
		verbose_name = u'Доставка_транспорт'
		verbose_name_plural = u'Доставка_транспорт'
		
		

delstatusc=(
	('wait', 'Ожидает'),
	('accept', 'Принят'),
	('success', 'Доставлен'),
	('cancel', 'Отменен'),
	)
		
delareac=(
	('a', 'Железнодорожный'),
	('b', u'Кировский'),
	('c', u'Ленинский'),
	('d', u'Октябрьский'),
	('e', u'Свердловский'),
	('f', u'Советский'),
	('g', u'Центральный'),
	)

class dellist(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	order = models.ForeignKey(order, on_delete=models.CASCADE, verbose_name='Заказ интернет магазина', null=True, blank=True) #это может быть и не заказ интернет магазина, тогда пусто
	ctime = models.DateTimeField(verbose_name='Время создания', auto_now_add=True,)
	utime = models.DateTimeField(verbose_name='Время обновления', auto_now=True,)
	courier = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Курьер', blank=True, null=True)
	status = models.CharField(verbose_name='Статус', max_length=80, choices=delstatusc, default='wait')
	#
	area = models.CharField(verbose_name='Район', max_length=100, blank=True, choices=delareac,)
	addr = models.CharField(verbose_name='Адрес доставки', max_length=300, blank=True)
	comment = models.TextField(verbose_name='Комментарий', max_length=300, blank=True)
	#

	def __str__(self):
		return '%s %s' % (self.id, self.status)

	class Meta:
		ordering=['-id']
		verbose_name = u'Доставка_список'
		verbose_name_plural = u'Доставка_список'




deleventc=(
	('add', 'Создан'), 
	('sms', 'Отправлено СМС'), (
	'update', 'Обновлен'), 
	('accept', 'Принят менеджером'), 
	('edit', 'Редактирование заказа'), 
	('statusedit', 'Изминение статуса заказа'), 
	('success', 'Обработан'),
	('other', 'Другие операции'),
	)
	
class delevent(models.Model):
	id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', blank=True, null=True)
	dellist = models.ForeignKey(dellist, on_delete=models.CASCADE, verbose_name='Доставка')
	ctime = models.DateTimeField(verbose_name='Время', auto_now_add=True)
	event = models.CharField(verbose_name='Событие', max_length=200, choices=deleventc)
	comment = models.TextField(verbose_name='Комментарий', max_length=500, blank=True)
	info = models.TextField(verbose_name='Тех.Информация', max_length=1000, blank=True)


	def __str__(self):
		return '%s %s %s %s' % (self.id, self.dellist, self.ctime, self.event)

	class Meta:
		ordering=['ctime']
		verbose_name = u'Доставка_событие'
		verbose_name_plural = u'Доставка_событие'
		