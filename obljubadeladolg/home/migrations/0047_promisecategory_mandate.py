# Generated by Django 3.2.11 on 2022-08-31 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0046_auto_20220830_1943'),
    ]

    operations = [
        migrations.AddField(
            model_name='promisecategory',
            name='mandate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='home.promiselistingpage', verbose_name='Mandat vlade'),
        ),
    ]
