# Generated by Django 5.1.3 on 2024-12-05 04:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web01', '0005_alter_customer_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='admin',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='web01.admin', verbose_name='管理员'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='gender',
            field=models.SmallIntegerField(choices=[(0, '男'), (1, '女')], default=0, verbose_name='性别'),
        ),
    ]
