# Generated by Django 3.2.4 on 2021-06-18 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0023_add_choose_permissions'),
        ('home', '0024_auto_20210618_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='promisepage',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Slika'),
        ),
    ]
