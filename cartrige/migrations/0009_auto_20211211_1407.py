# Generated by Django 3.2.2 on 2021-12-11 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartrige', '0008_auto_20211211_0808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allprinters',
            name='inventar_num',
            field=models.CharField(max_length=8, unique=True, verbose_name='Инвентарный номер'),
        ),
        migrations.AlterField(
            model_name='sklad',
            name='cart_buh',
            field=models.CharField(max_length=30, unique=True, verbose_name='Картридж по бухгалтерии'),
        ),
    ]
