# Generated by Django 3.2.2 on 2021-12-15 08:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cartrige', '0020_alter_cartriges_metacart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartriges',
            name='metacart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cartrige.metacart', verbose_name='Группа'),
        ),
    ]
