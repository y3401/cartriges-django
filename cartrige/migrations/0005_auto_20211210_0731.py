# Generated by Django 3.2.2 on 2021-12-10 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartrige', '0004_alter_printers_photo_prn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='printers',
            name='cart',
            field=models.ManyToManyField(blank=True, related_name='carts', to='cartrige.Cartriges', verbose_name='Совместимые картриджи'),
        ),
        migrations.AlterField(
            model_name='printers',
            name='name_printer',
            field=models.CharField(max_length=25, unique=True, verbose_name='Принтер'),
        ),
    ]