# Generated by Django 3.2.4 on 2021-06-18 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0023_add_choose_permissions'),
        ('home', '0023_promisestatus_order_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promisecategory',
            name='image',
        ),
        migrations.AddField(
            model_name='promisecategory',
            name='image_card',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Slika na kartici'),
        ),
        migrations.AddField(
            model_name='promisecategory',
            name='image_listing_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Slika na seznamu obljub'),
        ),
        migrations.AlterField(
            model_name='promiseupdate',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='home.promisestatus', verbose_name='Stanje'),
        ),
    ]
