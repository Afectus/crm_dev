from django.db import models

from panel.models import profileuser






class biditem(models.Model):
    id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
    order = models.ForeignKey(order, on_delete=models.CASCADE, verbose_name='Заказ интернет магазина', null=True, blank=True)
    ctime = models.DateTimeField(verbose_name='Время создания', auto_now_add=True,)
    utime = models.DateTimeField(verbose_name='Время обновления', auto_now=True,)
    cuser = models.ForeignKey(profileuser, on_delete=models.CASCADE, verbose_name='Курьер', blank=True, null=True)
    status = models.CharField(verbose_name='Статус', max_length=80, choices=delstatusc, default='wait')

    points = models.IntegerField(verbose_name='Кол-во баллов', max_length=100, blank=True, choices=delareac,)
    addr = models.CharField(verbose_name='Адрес доставки', max_length=300, blank=True)
    comment = models.TextField(verbose_name='Комментарий', max_length=300, blank=True)


    def __str__(self):
        return '%s %s' % (self.id, self.status)