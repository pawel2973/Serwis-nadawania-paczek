# Generated by Django 2.1.2 on 2018-12-22 02:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0013_auto_20181221_0626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='premium_points',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]