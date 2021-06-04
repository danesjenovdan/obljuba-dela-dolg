# Generated by Django 3.2.3 on 2021-06-04 09:53

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0062_comment_models_and_pagesubscription'),
        ('home', '0007_promiselistingpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromisePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('source_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ime vira')),
                ('source_url', models.URLField(blank=True, null=True, verbose_name='Povezava do vira')),
                ('categories', modelcluster.fields.ParentalManyToManyField(blank=True, to='home.PromiseCategory', verbose_name='Kategorije')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
