# Generated by Django 2.0.1 on 2018-01-27 05:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0006_auto_20180126_2305'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
    ]
