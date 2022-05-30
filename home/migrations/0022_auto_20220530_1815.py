# Generated by Django 3.2.12 on 2022-05-30 18:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailforms', '0004_add_verbose_name_plural'),
        ('wagtailcore', '0066_collection_management_permissions'),
        ('wagtailredirects', '0007_add_autocreate_fields'),
        ('home', '0021_auto_20220530_1749'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='missionspagefaqs',
            name='page',
        ),
        migrations.RemoveField(
            model_name='upcomingmissions',
            name='event_image',
        ),
        migrations.RemoveField(
            model_name='upcomingmissions',
            name='page',
        ),
        migrations.DeleteModel(
            name='MissionsPage',
        ),
        migrations.DeleteModel(
            name='MissionsPageFaqs',
        ),
        migrations.DeleteModel(
            name='UpcomingMissions',
        ),
    ]
