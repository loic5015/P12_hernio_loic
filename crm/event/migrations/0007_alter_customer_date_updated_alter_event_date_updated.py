# Generated by Django 4.0.6 on 2022-07-21 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0006_alter_contract_date_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='date_updated',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='date_updated',
            field=models.DateTimeField(null=True),
        ),
    ]
