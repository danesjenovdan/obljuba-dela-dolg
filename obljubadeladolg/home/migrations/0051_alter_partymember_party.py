# Generated by Django 3.2.11 on 2022-09-01 19:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0050_partymember_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partymember',
            name='party',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='home.party', verbose_name='Stranka'),
        ),
    ]