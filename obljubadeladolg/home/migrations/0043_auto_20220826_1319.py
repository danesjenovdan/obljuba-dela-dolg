# Generated by Django 3.2.11 on 2022-08-26 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0023_add_choose_permissions'),
        ('home', '0042_governmentpage_header_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='governmentpage',
            name='mandate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='home.promiselistingpage', verbose_name='Vladna stran za:'),
        ),
        migrations.CreateModel(
            name='PartyMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Ime')),
                ('role', models.TextField(verbose_name='Vloga')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Slika')),
            ],
            options={
                'verbose_name': 'Član vlade',
                'verbose_name_plural': 'Člani vlade',
            },
        ),
    ]
