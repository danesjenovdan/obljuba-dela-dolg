# Generated by Django 3.2.11 on 2022-08-17 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0032_infopush'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='subtitle',
            field=models.TextField(blank=True, null=True, verbose_name='Podnaslov'),
        ),
    ]
