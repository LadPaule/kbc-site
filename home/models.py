from email.policy import default
from django.db import models
from streams.blocks import TableBlock as tabeblock
from wagtail.core.models import Page, Orderable
from modelcluster.fields import ParentalKey
from wagtail.core.fields import RichTextField, StreamField
from wagtail_embed_videos import get_embed_video_model_string
from wagtail_embed_videos.edit_handlers import EmbedVideoChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, StreamFieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailmedia.edit_handlers import MediaChooserPanel
from wagtail.search import index
from wagtailcaptcha.models import WagtailCaptchaEmailForm


class HomePage(Page):
    body = RichTextField(blank=True)
    weekly_activities = RichTextField(blank=True)
    featured_media = models.ForeignKey('wagtailmedia.Media', null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+", help_text="Video or image to be displayed on the home page")
  
    video = models.ForeignKey(
        get_embed_video_model_string(),
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    pray_with_us = RichTextField(blank=True)
    tabled = StreamField(tabeblock(), blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full", help_text="This is the body of the page"),
        EmbedVideoChooserPanel('video', help_text="This is the most recent video stream"),
        InlinePanel('stream_media', label="Audio Media", help_text="Upload audio to the Home Page"),
        InlinePanel('gallery_images', label="Carousel or Slider images", help_text="Upload images to the carousel"),
        InlinePanel('ministries', label="ministry Cards", help_text="Edit the ministries&apos; cards"),
        FieldPanel('pray_with_us', classname="full", help_text="this is the Pray concerns fiels"),
        StreamFieldPanel('tabled', help_text="This table for the Weekly Activities"),
    ]

class HomePageMedia(Orderable):
    page = ParentalKey('HomePage', on_delete=models.CASCADE, related_name='stream_media')
    media = models.ForeignKey('wagtailmedia.Media', on_delete=models.CASCADE, related_name='+')
    media_text = models.CharField(max_length=255, blank=True)
    panels = [
        MediaChooserPanel('media'),
        FieldPanel('media_text'),
    ]
class HomePageGalleryImage(Orderable):
    page = ParentalKey('HomePage', on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    caption = models.CharField (blank=True, max_length=800)
    image_title= models.CharField(blank=True, max_length=250)
    panels = [ ImageChooserPanel('image'),
        FieldPanel('image_title'),
        FieldPanel('caption'),
    ]

class HomePageMinistry(Orderable):
    page = ParentalKey('HomePage', on_delete=models.CASCADE, related_name='ministries')
    ministry_title = models.CharField(blank=True, max_length=250)
    short_description = models.CharField(blank=True, max_length=2000)
    icon_class = models.CharField(blank=True, max_length=250)
    ministry_link = models.CharField(blank=True, max_length=100)
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    panels = [
        FieldPanel('ministry_title'),
        FieldPanel('short_description'),
        FieldPanel('icon_class'),
        FieldPanel('ministry_link'),
        ImageChooserPanel('image'),
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

class ContactPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text=RichTextField(blank=True)
    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', help_text="This is the body of the page"),
        InlinePanel('form_fields', label="Form Fields"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], heading="Email Settings")  
    ]

class ContactPageFormField(AbstractFormField):
    page = ParentalKey(ContactPage, on_delete=models.CASCADE, related_name='form_fields')
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
    statement_body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
       FieldPanel('statement_body', classname="full", help_text="This is the body of the Page"),
    ]

# convenant page
class ConvenantPage(Page):
    convenant_body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('convenant_body', classname="full", help_text="This is the body of the Page"),
    ]
# Ministries
class ChildrenPage(Page):
    about_body = RichTextField(blank=True)
    video = models.ForeignKey(
        get_embed_video_model_string(),
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    content_panels = Page.content_panels + [
        FieldPanel('about_body', classname="full", help_text="This is the intro of the Page"),
        EmbedVideoChooserPanel('video', help_text="This is the most recent video stream"),
        InlinePanel('children_ministry_faqs', label="Frequently asked questions about the children ministry", help_text="Upload images to the carousel"),
    
    ]  
class ChildrenPageFaqs(Orderable):
    page = ParentalKey('ChildrenPage', related_name='children_ministry_faqs')
    question = models.CharField(max_length=800, blank=True)
    answer = models.CharField (blank=True, max_length=800)
    panels = [
        FieldPanel('question'),
        FieldPanel('answer'),
    ]  

class AdultsPage(Page):
    about_body = RichTextField(blank=True)
    video = models.ForeignKey(
        get_embed_video_model_string(),
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    content_panels = Page.content_panels + [
        FieldPanel('about_body', classname="full", help_text="This is the intro of the Page"),
        EmbedVideoChooserPanel('video', help_text="This is the most recent video stream"),
        InlinePanel('adult_ministry_faqs', label="Frequently asked questions about the KBC Adults ministry", help_text="Upload images to the carousel"),
    
    ]
class AdultsPageFaqs(Orderable):
    page = ParentalKey('AdultsPage', related_name='adult_ministry_faqs')
    question = models.CharField(max_length=800, blank=True)
    answer = models.CharField (blank=True, max_length=800)
    panels = [
        FieldPanel('question'),
        FieldPanel('answer'),
    ]  

class YouthPage(Page):
    about_body = RichTextField(blank=True)
    video = models.ForeignKey(
        get_embed_video_model_string(),
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    content_panels = Page.content_panels + [
        FieldPanel('about_body', classname="full", help_text="This is the intro of the Page"),
        EmbedVideoChooserPanel('video', help_text="This is the most recent video stream"),
        InlinePanel('youth_ministry_faqs', label="Frequently asked questions about the KBC Youth ministry", help_text="Upload images to the carousel"),
    
    ]

class YouthPageFaqs(Orderable):
    page = ParentalKey('YouthPage', related_name='youth_ministry_faqs')
    question = models.CharField(max_length=800, blank=True)
    answer = models.CharField (blank=True, max_length=800)
    panels = [
        FieldPanel('question'),
        FieldPanel('answer'),
    ]

class WorshipPage(Page):
    about_body = RichTextField(blank=True)
    video = models.URLField("Video URL", blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('about_body', classname="full", help_text="This is the intro of the Page"),
        EmbedVideoChooserPanel('video', help_text="This is the most recent video stream"),
        InlinePanel('worship_ministry_faqs', label="Frequently asked questions about the KBC Worship ministry", help_text="Upload images to the carousel"),
    
    ]
class WorshipPageFaqs(Orderable):
    page = ParentalKey('WorshipPage', related_name='worship_ministry_faqs')
    question = models.CharField(max_length=800, blank=True)
    answer = models.CharField (blank=True, max_length=800)
    panels = [
        FieldPanel('question'),
        FieldPanel('answer'),
    ]  
class DiscipleshipPage(Page):
    about_body = RichTextField(blank=True)
    video = models.ForeignKey(
        get_embed_video_model_string(),
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    content_panels = Page.content_panels + [
        FieldPanel('about_body', classname="full", help_text="This is the intro of the Page"),
        EmbedVideoChooserPanel('video', help_text="This is the most recent video stream"),
        InlinePanel('Discipleship_ministry_faqs', label="Frequently asked questions about the KBC Discipleship ministry", help_text="Upload images to the carousel"),
    
    ]
class DiscipleshipPageFaqs(Orderable):
    page = ParentalKey('DiscipleshipPage', related_name='Discipleship_ministry_faqs')
    question = models.CharField(max_length=800, blank=True)
    answer = models.CharField (blank=True, max_length=800)
    panels = [
        FieldPanel('question'),
        FieldPanel('answer'),
    ]  


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
    name_of_the_pastor= models.CharField(blank=True, max_length=250)
    panels = [ ImageChooserPanel('photograph'),
        FieldPanel('story'),
        FieldPanel('name_of_the_pastor'),
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

