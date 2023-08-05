# Generated by Django 4.1.3 on 2022-11-24 19:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('WebApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='station_elev',
            field=models.FloatField(blank=True, help_text='Station Elevation in meters above sea level - Optional',
                                    null=True),
        ),
        migrations.AlterField(
            model_name='station',
            name='station_year_established',
            field=models.IntegerField(blank=True, help_text='Year the station was established - Optional', null=True),
        ),
    ]
