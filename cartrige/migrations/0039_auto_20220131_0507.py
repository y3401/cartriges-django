# Generated by Django 3.2.2 on 2022-01-31 02:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cartrige', '0038_logs_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kod', models.IntegerField(verbose_name='Код операции')),
                ('operation_name', models.CharField(max_length=25, verbose_name='Операция')),
            ],
            options={
                'verbose_name_plural': 'Операции',
            },
        ),
        migrations.RemoveField(
            model_name='logs',
            name='name_table',
        ),
        migrations.AlterField(
            model_name='logs',
            name='action',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cartrige.operation', verbose_name='Операция'),
        ),
    ]
