# Generated by Django 2.0.1 on 2018-03-06 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docflow', '0002_auto_20180302_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cash_payment_voucher',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Основание'),
        ),
    ]