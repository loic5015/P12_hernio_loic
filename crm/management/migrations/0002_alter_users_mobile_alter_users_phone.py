# Generated by Django 4.0.6 on 2022-07-06 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='mobile',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='users',
            name='phone',
            field=models.IntegerField(),
        ),
    ]
