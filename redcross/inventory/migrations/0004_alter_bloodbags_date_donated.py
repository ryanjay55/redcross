# Generated by Django 4.1.7 on 2023-04-30 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_alter_bloodbags_date_donated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloodbags',
            name='date_donated',
            field=models.DateTimeField(),
        ),
    ]
