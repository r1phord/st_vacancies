# Generated by Django 3.0.7 on 2020-07-11 19:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('vacancies', '0006_auto_20200711_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='education',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='resume',
            name='experience',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='resume',
            name='portfolio',
            field=models.CharField(max_length=300),
        ),
    ]
