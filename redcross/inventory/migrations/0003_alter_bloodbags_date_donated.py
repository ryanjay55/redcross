# Generated by Django 4.1.7 on 2023-04-30 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_alter_bloodbags_serial_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloodbags',
            name='date_donated',
            field=models.DateField(),
        ),
    ]
