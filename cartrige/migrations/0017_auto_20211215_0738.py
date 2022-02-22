# Generated by Django 3.2.2 on 2021-12-15 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartrige', '0016_auto_20211215_0708'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartriges',
            name='metacart',
        ),
        migrations.AddField(
            model_name='cartriges',
            name='metacart',
            field=models.ManyToManyField(blank=True, related_name='metacart', to='cartrige.MetaCart', verbose_name='Группа картриджа'),
        ),
    ]