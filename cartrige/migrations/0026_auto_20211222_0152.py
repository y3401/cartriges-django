# Generated by Django 3.2.2 on 2021-12-21 22:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cartrige', '0025_auto_20211217_2339'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sklad',
            options={'ordering': ['cartriges'], 'verbose_name_plural': 'Склад'},
        ),
        migrations.RenameField(
            model_name='sklad',
            old_name='id_cart',
            new_name='cartriges',
        ),
    ]
