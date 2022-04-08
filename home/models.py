from django.db import models

from wagtail.core.models import Page, Orderable
from modelcluster.fields import ParentalKey
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtailcaptcha.models import WagtailCaptchaEmailForm



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
    more_history = RichTextField(blank=True)
    church_philosophy = RichTextField(blank=True)
    membership = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('church_history', classname="full", help_text="This is the body of the page"),
        InlinePanel('side_image', label="Side Image", help_text="Upload images to the hero Section/ kbc website banner"),
        FieldPanel('more_history', classname="full", help_text="This is more history of the page"),
        FieldPanel('church_philosophy', classname="full", help_text="This is where the church philosophy is"),
        FieldPanel('membership', classname="full", help_text="This is where the membership detail is contained"),
    ]

class InceptionPageGalleryImage(Orderable):
    page = ParentalKey('InceptionPage', on_delete=models.CASCADE, related_name='side_image')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    caption = models.CharField (blank=True, max_length=800)
    image_title= models.CharField(blank=True, max_length=250)
    panels = [ 
        ImageChooserPanel('image'),
        FieldPanel('caption'),
        FieldPanel('image_title'),
    ]


class ContactPage(WagtailCaptchaEmailForm):
    template="home/contact_page.html"
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)
    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', classname="full", help_text="This is the intro of the Contact Page"),
        InlinePanel('form_fields', label="Contact Form Fields", help_text="Add Contact Form Fields"),
        FieldPanel('thank_you_text', classname="full", help_text="This is the appreciative text of the Contact Page"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], heading="Email Settings"),
    ]

class ContactPageFormField(AbstractFormField):
    page = ParentalKey('ContactPage', on_delete=models.CASCADE, related_name='form_fields')

# Prayer Request Page
class PrayerRequestPage(WagtailCaptchaEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)
    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', classname="full", help_text="This is the intro of the Contact Page"),
        InlinePanel('form_fields', label="Contact Form Fields", help_text="Add Contact Form Fields"),
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
    page = ParentalKey('PrayerRequestPage', on_delete=models.CASCADE, related_name='form_fields')


# Appointments Page
class AppointmentsPage(WagtailCaptchaEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)
    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', classname="full", help_text="This is the intro of the Contact Page"),
        InlinePanel('form_fields', label="Appointment Form Fields", help_text="Add Contact Form Fields"),
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
    page = ParentalKey('AppointmentsPage', on_delete=models.CASCADE, related_name='form_fields')


# Statement of Faith
class StatementOfFaithPage(Page):
    intro = RichTextField(blank=True)
    statement_body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full", help_text="This is the intro of the Page"),
        FieldPanel('statement_body', classname="full", help_text="This is the body of the Page"),
    ]

  

# convenant page
class ConvenantPage(Page):
    intro = RichTextField(blank=True)
    convenant_body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        InlinePanel('Heroimage', label="Banner Image", help_text="Upload images to the banner area of the Page "),
        FieldPanel('intro', classname="full", help_text="This is the intro of the Page"),
        FieldPanel('convenant_body', classname="full", help_text="This is the body of the Page"),
    ]
class ConvenantPageImage(Orderable):
    page = ParentalKey('ConvenantPage', on_delete=models.CASCADE, related_name='Heroimage')
    image = models.ForeignKey('wagtailimages.image', on_delete=models.CASCADE, related_name="+")
    caption = models.CharField(blank=True, max_length=700)
    panels = [ ImageChooserPanel('image'),
        FieldPanel('caption'),
    ] 

# Ministries

# Leadership

# Give Page
class GivePage(Page):
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full", help_text="This is the intro of the Page"),
        InlinePanel('card_information', label="card Information", help_text="Upload images to the give give card"),
    ]

class GivePageGalleryImage(Orderable):
    page = ParentalKey('GivePage', on_delete=models.CASCADE, related_name='card_information')
    card_image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    card_title= models.CharField(blank=True, max_length=250)
    card_text = models.CharField (blank=True, max_length=2200)
    card_back_side = models.CharField (blank=True, max_length=2200)
    panels = [ ImageChooserPanel('card_image'),
        FieldPanel('card_title'),
        FieldPanel('card_text'),
        FieldPanel('card_back_side'),
    ]


# Gallery Page
#Elders Board Page
class EldersBoardPage(Page):
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
    FieldPanel('intro', classname="full", help_text="This is the body of the page"),
    InlinePanel('profile_image', label="Individual Photo files", help_text="Upload Photos of the elders"),
    ]
class EldersBoardPageGalleryImage(Orderable):
    page = ParentalKey('EldersBoardPage', on_delete=models.CASCADE, related_name='profile_image')
    photograph = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    designation = models.CharField (blank=True, max_length=800)
    elders_name= models.CharField(blank=True, max_length=250)
    panels = [ ImageChooserPanel('photograph'),
        FieldPanel('designation'),
        FieldPanel('elders_name'),
    ]

class PastoratePage(Page):
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
    FieldPanel('intro', classname="full", help_text="This is the body of the profile"),
    InlinePanel('profile_image', label="Individual Photo files", help_text="Upload Photos of the pastors"),
    ]
class PastoratePageGalleryImage(Orderable):
    page = ParentalKey('PastoratePage', on_delete=models.CASCADE, related_name='profile_image')
    photograph = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    story = RichTextField(blank=True)
    elders_name= models.CharField(blank=True, max_length=250)
    panels = [ ImageChooserPanel('photograph'),
        FieldPanel('story'),
        FieldPanel('elders_name'),
    ]

class StaffPage(Page):
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
    FieldPanel('intro', classname="full", help_text="This is the body of the page"),
    InlinePanel('profile_image', label="Individual Photo files", help_text="Upload Photos of the elders"),
    ]
class StaffPageGalleryImage(Orderable):
    page = ParentalKey('StaffPage', on_delete=models.CASCADE, related_name='profile_image')
    photograph = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    designation = models.CharField (blank=True, max_length=800)
    staff_name = models.CharField(blank=True, max_length=250)
    twitter = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    linkedIn = models.URLField(blank=True)
    panels = [ ImageChooserPanel('photograph'),
        FieldPanel('designation'),
        FieldPanel('staff_name'),
        FieldPanel('twitter'),
        FieldPanel('facebook'),
        FieldPanel('linkedIn'),
    ]  

