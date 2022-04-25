# Generated by Django 3.2.12 on 2022-04-25 04:33

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtaildocs', '0012_uploadeddocument'),
        ('wagtailcore', '0066_collection_management_permissions'),
        ('home', '0006_homegallerypagegalleryimage_photo_caption'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnnouncementPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('intro', wagtail.core.fields.RichTextField(blank=True)),
                ('document_file', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtaildocs.document')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
