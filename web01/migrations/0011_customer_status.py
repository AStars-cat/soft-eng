# Generated by Django 5.1.3 on 2024-12-08 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web01', '0010_customer_email_customer_phone_alter_company_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='status',
            field=models.SmallIntegerField(choices=[(0, '未分配'), (1, '已分配')], default=0, verbose_name='状态'),
        ),
    ]