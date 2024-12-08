# Generated by Django 5.1.3 on 2024-12-08 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web01', '0008_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='paid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='已付金额'),
        ),
    ]
