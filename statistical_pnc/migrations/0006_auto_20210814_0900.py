# Generated by Django 3.2.5 on 2021-08-14 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistical_pnc', '0005_category_reference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reference',
            name='title',
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='word',
            name='string',
            field=models.CharField(max_length=32, unique=True),
        ),
    ]
