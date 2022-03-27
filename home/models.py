from django.db import models

from wagtail.core.models import Page, Orderable
from modelcluster.fields import ParentalKey
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
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
    page = ParentalKey('InceptionPage', on_delete=models.CASCADE, related_name='Heroimages')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    side_image = models.ForeignKey('wagtailimages.Image', blank=True, null=True, on_delete=models.CASCADE, related_name='+')
    caption = models.CharField (blank=True, max_length=800)
    image_title= models.CharField(blank=True, max_length=250)

    panels = [ ImageChooserPanel('image'),
        FieldPanel('caption'),
        FieldPanel('image_title'),
    ]