# Generated by Django 3.2.11 on 2022-08-30 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0062_comment_models_and_pagesubscription'),
        ('wagtailimages', '0023_add_choose_permissions'),
        ('home', '0045_auto_20220828_2138'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contentpage',
            options={'verbose_name': 'Navadna stran z vsebino', 'verbose_name_plural': 'Navadne strani z vsebino'},
        ),
        migrations.AlterModelOptions(
            name='governmentpage',
            options={'verbose_name': 'Opis vlade', 'verbose_name_plural': 'Opisi vlade'},
        ),
        migrations.AlterModelOptions(
            name='infopush',
            options={'verbose_name': 'Obvestilo na domači strani', 'verbose_name_plural': 'Obvestila na domači strani'},
        ),
        migrations.AlterModelOptions(
            name='newsletterpage',
            options={'verbose_name': 'Stran za urejanje naročnine', 'verbose_name_plural': 'Strani za urejanje naročnine'},
        ),
        migrations.AlterModelOptions(
            name='promiselistingpage',
            options={'verbose_name': 'Vlada', 'verbose_name_plural': 'Vlade'},
        ),
        migrations.AlterModelOptions(
            name='promiseupdate',
            options={'ordering': ['date']},
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='newsletter_image',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='social_media_image',
        ),
        migrations.AlterField(
            model_name='promiselistingpage',
            name='about_statuses_link',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.page', verbose_name="Povezava do strani z razlago 'Kaj pomenijo posamezni statusi?'"),
        ),
        migrations.AlterField(
            model_name='promisepage',
            name='meta_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='OG slika'),
        ),
    ]