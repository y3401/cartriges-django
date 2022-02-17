# Generated by Django 3.2.2 on 2021-12-17 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartrige', '0023_alter_records_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='records',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[('1', 'Новый'), ('2', 'Установлен'), ('3', 'Пустой'), ('4', 'Заправка'), ('5', 'Заправлен'), ('6', 'Дефект'), ('7', 'Списан')], default='5', help_text='Статус картриджа', verbose_name='Статус'),
        ),
    ]
