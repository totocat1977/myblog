# Generated by Django 2.0.1 on 2018-01-27 05:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0007_auto_20180127_1303'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['mbc_order'], 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
    ]