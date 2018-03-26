from django.db import models
from panel.models import profileuser



class points(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(profileuser, on_delete=models.CASCADE, default=0, verbose_name = "Выберите пользователя")
    type = models.CharField(verbose_name = "Тип баллов", max_length=200)
    point = models.FloatField(verbose_name='Кол-во баллов')
    comment = models.TextField(verbose_name = "Комментарий", max_length=1000, blank=True)
    edate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return u'%s' % (self.id)
