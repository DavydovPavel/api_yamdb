# Generated by Django 3.0.5 on 2020-08-30 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200830_0838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, default='user', max_length=30),
        ),
    ]
