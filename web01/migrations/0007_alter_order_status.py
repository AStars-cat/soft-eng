# Generated by Django 5.1.3 on 2024-12-08 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web01', '0006_order_admin_alter_customer_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[(0, '已完成'), (1, '未完成')], default=1, max_length=50, verbose_name='状态'),
        ),
    ]
