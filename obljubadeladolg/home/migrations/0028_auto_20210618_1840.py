# Generated by Django 3.2.4 on 2021-06-18 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0062_comment_models_and_pagesubscription'),
        ('home', '0027_merge_20210618_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='promiselistingpage',
            name='about_statuses_link',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.page'),
        ),
        migrations.AddField(
            model_name='promiselistingpage',
            name='about_statuses_text',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
