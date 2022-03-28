from django.db import models

from wagtail.core.models import Page, Orderable
from modelcluster.fields import ParentalKey
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index



class HomePage(Page):
    body = RichTextField(blank=True)
    video_url = models.URLField("Video URL", blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full", help_text="This is the body of the page"),
        FieldPanel('video_url', classname="full", help_text="This is the video url of the page"),
        InlinePanel('gallery_images', label="Carousel or Slider images", help_text="Upload images to the carousel"),
    ]
class HomePageGalleryImage(Orderable):
    DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
    page = ParentalKey('HomePage', on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    caption = models.CharField (blank=True, max_length=800)
    image_title= models.CharField(blank=True, max_length=250)

    panels = [ ImageChooserPanel('image'),
        FieldPanel('caption'),
        FieldPanel('image_title'),
    ]

class InceptionPage(Page):
    church_history = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        InlinePanel('Heroimages', label="Hero Image", help_text="Upload images to the hero Section/ kbc website banner"),
        FieldPanel('church_history', classname="full", help_text="This is the body of the page"),
        InlinePanel('Heroimages', label="Side Image", help_text="Upload images to the hero Section/ kbc website banner"),
    ]

class InceptionPageGalleryImage(Orderable):
    DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
    page = ParentalKey('InceptionPage', on_delete=models.CASCADE, related_name='Heroimages')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    side_image = models.ForeignKey('wagtailimages.Image', blank=True, null=True, on_delete=models.CASCADE, related_name='+')
    caption = models.CharField (blank=True, max_length=800)
    image_title= models.CharField(blank=True, max_length=250)

    panels = [ ImageChooserPanel('image'),
        FieldPanel('caption'),
        FieldPanel('image_title'),
    ]


class ContactPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)
    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', classname="full", help_text="This is the intro of the Contact Page"),
        InlinePanel('contact_page_form_fields', label="Contact Form Fields", help_text="Add Contact Form Fields"),
        FieldPanel('thank_you_text', classname="full", help_text="This is the appreciative text of the Contact Page"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], heading="Email Settings"),
    ]

class FormField(AbstractFormField):
    DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
    page = ParentalKey('ContactPage', on_delete=models.CASCADE, related_name='contact_page_form_fields')


# Prayer Request Page
class PrayerRequestPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)
    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', classname="full", help_text="This is the intro of the Contact Page"),
        InlinePanel('Heroimage', label="Carousel or Slider images", help_text="Upload images to the carousel"),
        InlinePanel('prayer_request_page_form_fields', label="Contact Form Fields", help_text="Add Contact Form Fields"),
        FieldPanel('thank_you_text', classname="full", help_text="This is the appreciative text of the Contact Page"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], heading="Email Settings"),
    ]

class PrayerRequestPageFormField(AbstractFormField):
    DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
    page = ParentalKey('PrayerRequestPage', on_delete=models.CASCADE, related_name='prayer_request_page_form_fields')

class PrayerRequestPageGalleryImage(Orderable):
    DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
    page = ParentalKey('PrayerRequestPage', on_delete=models.CASCADE, related_name='Heroimage')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    caption = models.CharField (blank=True, max_length=800)
    image_title= models.CharField(blank=True, max_length=250)

    panels = [ ImageChooserPanel('image'),
        FieldPanel('caption'),
        FieldPanel('image_title'),
    ]


# Appointments Page
class AppointmentsPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)
    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', classname="full", help_text="This is the intro of the Contact Page"),
        InlinePanel('Heroimage', label="Carousel or Slider images", help_text="Upload images to the carousel"),
        InlinePanel('prayer_request_page_form_fields', label="Appointment Form Fields", help_text="Add Contact Form Fields"),
        FieldPanel('thank_you_text', classname="full", help_text="This is the appreciative text of the Contact Page"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], heading="Email Settings"),
    ]
class AppointmentsPageFormField(AbstractFormField):
    DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
    page = ParentalKey('AppointmentsPage', on_delete=models.CASCADE, related_name='prayer_request_page_form_fields')

class AppointmentsPageGalleryImage(Orderable):
    page = ParentalKey('AppointmentsPage', on_delete=models.CASCADE, related_name='Heroimage')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    caption = models.CharField (blank=True, max_length=800)
    image_title= models.CharField(blank=True, max_length=250)

    panels = [ ImageChooserPanel('image'),
        FieldPanel('caption'),
        FieldPanel('image_title'),
    ]

