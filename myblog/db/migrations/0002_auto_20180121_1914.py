# Generated by Django 2.0.1 on 2018-01-21 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['mbc_parent_id', 'mbc_order'], 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='category',
            name='mbc_parent_id',
            field=models.SmallIntegerField(default=0, verbose_name='Parent Category ID'),
        ),
    ]
