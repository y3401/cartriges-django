# Generated by Django 3.2.2 on 2022-01-23 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartrige', '0034_records_c_agent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='records',
            name='c_agent',
            field=models.IntegerField(blank=True, null=True, verbose_name='Контрагент'),
        ),
    ]
