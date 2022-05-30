from email.policy import default
from django.db import models
from streams.blocks import TableBlock as tableblock
from wagtail.core.models import Page, Orderable
from modelcluster.fields import ParentalKey
from wagtail.core.fields import RichTextField, StreamField
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail_embed_videos import get_embed_video_model_string
from wagtail_embed_videos.edit_handlers import EmbedVideoChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, StreamFieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailmedia.edit_handlers import MediaChooserPanel
from wagtail.search import index
from wagtailcaptcha.models import WagtailCaptchaEmailForm
from wagtail.documents.models import Document
from wagtail.documents.edit_handlers import DocumentChooserPanel



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
    luganda_bible_study =  models.ForeignKey('wagtaildocs.Document', blank=True, null=True,  on_delete=models.SET_NULL, related_name='+')
    English_bible_study =  models.ForeignKey('wagtaildocs.Document', blank=True, null=True,  on_delete=models.SET_NULL, related_name='+')

    pray_with_us = RichTextField(blank=True)
    tabled = StreamField(tableblock(), blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full", help_text="This is the body of the page"),
        EmbedVideoChooserPanel('video', help_text="This is the most recent video stream"),
        MediaChooserPanel("featured_media", media_type="audio"),
        DocumentChooserPanel("luganda_bible_study", help_text="This is the most recent Luganda bible study guideline"),
        DocumentChooserPanel("English_bible_study", help_text="This is the most recent English bible study guideline"),
        InlinePanel('gallery_images', label="Carousel or Slider images", help_text="Upload images to the carousel"),
        InlinePanel('ministries', label="ministry Cards", help_text="Edit the ministries&apos; cards"),
        FieldPanel('pray_with_us', classname="full", help_text="this is the Pray concerns fiels"),
        StreamFieldPanel('tabled', help_text="This table for the Weekly Activities"),
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
    church_history_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    more_history = RichTextField(blank=True)
    church_philosophy = RichTextField(blank=True)
    membership = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('church_history', classname="full", help_text="This is the body of the page"),
        ImageChooserPanel('church_history_image', help_text="This is the most recent video stream"),
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
    hero_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True,on_delete=models.SET_NULL, related_name='+')
    thank_you_text=RichTextField(blank=True)
    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', help_text="This is the body of the page"),
        ImageChooserPanel('hero_image', help_text="This is the most recent video stream"),
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
class PrayerRequestPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    hero_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True,on_delete=models.SET_NULL, related_name='+')
    thank_you_text = RichTextField(blank=True)
    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', classname="full", help_text="This is the intro of the Contact Page"),
        ImageChooserPanel('hero_image', help_text="This is the most recent video stream"),
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
class AppointmentsPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    hero_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True,on_delete=models.SET_NULL, related_name='+')
    thank_you_text = RichTextField(blank=True)
    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', classname="full", help_text="This is the intro of the Contact Page"),
        ImageChooserPanel('hero_image', help_text="This is the most recent video stream"),
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
    hero_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True,on_delete=models.SET_NULL, related_name='+')
    statement_body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        ImageChooserPanel('hero_image', help_text="This is the most recent video stream"),
        FieldPanel('statement_body', classname="full", help_text="This is the body of the Page"),
    ]

# convenant page
class ConvenantPage(Page):
    hero_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True,on_delete=models.SET_NULL, related_name='+')
    convenant_body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        ImageChooserPanel('hero_image', help_text="This is the most recent video stream"),
        FieldPanel('convenant_body', classname="full", help_text="This is the body of the Page"),
    ]
# Ministries
class ChildrenPage(Page):
    hero_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True,on_delete=models.SET_NULL, related_name='+')
    about_body = RichTextField(blank=True)
    video = models.ForeignKey(
        get_embed_video_model_string(),
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    content_panels = Page.content_panels + [
        ImageChooserPanel('hero_image', help_text="This is the most recent video stream"),
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

class YouthPage(Page):
    hero_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True,on_delete=models.SET_NULL, related_name='+')
    about_body = RichTextField(blank=True)
    video = models.ForeignKey(
        get_embed_video_model_string(),
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    content_panels = Page.content_panels + [
        ImageChooserPanel('hero_image', help_text="This is the most recent video stream"),
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
    hero_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True,on_delete=models.SET_NULL, related_name='+')
    about_body = RichTextField(blank=True)
    
    video = models.ForeignKey(
        get_embed_video_model_string(),
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    content_panels = Page.content_panels + [
        ImageChooserPanel('hero_image', help_text="This is the most recent video stream"),
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
    hero_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True,on_delete=models.SET_NULL, related_name='+')
    about_body = RichTextField(blank=True)
    video = models.ForeignKey(
        get_embed_video_model_string(),
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    content_panels = Page.content_panels + [
        ImageChooserPanel('hero_image', help_text="This is the most recent video stream"),
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
class HomeGalleryPage(Page):
    content_panels = Page.content_panels + [
        InlinePanel('gallery_image', label="Gallery Images", help_text="Upload images to the gallery"),
        InlinePanel('image_tag', label="Gallery tags", help_text="add or edit the tags for the gallery images"),
    ]
class HomeGalleryPageGalleryImage(Orderable):
    page = ParentalKey('HomeGalleryPage', on_delete=models.CASCADE, related_name='gallery_image')
    photo_caption = models.CharField(blank=True, max_length=250)
    photograph = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    photograph_tag= models.CharField(blank=True, max_length=250)
    panels = [ ImageChooserPanel('photograph'),
        FieldPanel('photo_caption'),
        FieldPanel('photograph_tag'),
    ]
class HomeGalleryPageTag(Orderable):
    page = ParentalKey('HomeGalleryPage', on_delete=models.CASCADE, related_name='image_tag')
    tag= models.CharField(blank=True, max_length=250)
    panels = [FieldPanel('tag'), ]

#Elders Board Page
class EldersBoardPage(Page):
    intro = RichTextField(blank=True)
    profile_photo = models.ForeignKey('wagtailimages.Image', null=True, blank=True,on_delete=models.SET_NULL, related_name='+')
    side_story = RichTextField(blank=True)
    more_story = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full", help_text="This is the body of the page"),
        ImageChooserPanel('profile_photo', help_text="This is the profile photo of the page"),
        FieldPanel('side_story', classname="full", help_text="This is the side story of the page"),
        FieldPanel('more_story', classname="full", help_text="This is the more story of the page"),
    ]
class DeaconsBoardPage(Page):
    intro = RichTextField(blank=True)
    profile_photo = models.ForeignKey('wagtailimages.Image', null=True, blank=True,on_delete=models.SET_NULL, related_name='+')
    side_story = RichTextField(blank=True)
    more_story = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full", help_text="This is the body of the page"),
        ImageChooserPanel('profile_photo', help_text="This is the profile photo of the page"),
        FieldPanel('side_story', classname="full", help_text="This is the side story of the page"),
        FieldPanel('more_story', classname="full", help_text="This is the more story of the page"),
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

class AnnouncementPage(Page):
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
    FieldPanel('intro', classname="full", help_text="This is the body of the page"),
    InlinePanel('announcement', label="Anouncement body", help_text="This is the body of the page"),
    ]

class AnnouncementPageGalleryImage(Orderable):
    page = ParentalKey('AnnouncementPage', on_delete=models.CASCADE, related_name='announcement')
    announcement_title = models.CharField(blank=True, max_length=250)
    photograph = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, null=True, related_name='+')
    body = RichTextField(blank=True)
    panels = [ 
        FieldPanel('announcement_title'),
        ImageChooserPanel('photograph'),
        FieldPanel('body'),
    ]

class WeddingBannsPage(Page):
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full", help_text="This is the body of the page"),
        InlinePanel('wedding_banns_profile', label="profiles of the couple", help_text="provide or edit the profiles of the couple"),
    ]
class WeddingBannsPageGalleryImage(Orderable):
    page = ParentalKey('WeddingBannsPage', on_delete=models.CASCADE, related_name='wedding_banns_profile')
    title= models.CharField(blank=True, max_length=250)
    image_image_of_the_groom_tobe = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    image_image_of_the_bride_tobe = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    body= RichTextField(blank=True)
    panels = [ 
        FieldPanel('title'),
        ImageChooserPanel('image_image_of_the_groom_tobe'),
        ImageChooserPanel('image_image_of_the_bride_tobe'),
        FieldPanel('body'),
    ]

class TermsOfServicePage(Page):
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full", help_text="This is the body of the page"),
    ]
class PrivacyPolicyPage(Page):
    intro = RichTextField(blank=True)
    body= RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full", help_text="This is the body of the page"),
        FieldPanel('body', classname="full", help_text="This is the body of the page"),
    ]

class CouplesPage(Page):
    featured_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True,on_delete=models.SET_NULL, related_name='+')
    about_body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('about_body', classname="full", help_text="This is the intro of the Page"),
        ImageChooserPanel('featured_image', help_text="This is the featured image of the Page"),
        InlinePanel('couples_ministry_faqs', label="Frequently asked questions about the KBC couples ministry", help_text="Upload images to the carousel"),
    
    ]
class CouplesPageFaqs(Orderable):
    page = ParentalKey('CouplesPage', related_name='couples_ministry_faqs')
    question = models.CharField(max_length=800, blank=True)
    answer = models.CharField (blank=True, max_length=800)
    panels = [
        FieldPanel('question'),
        FieldPanel('answer'),
    ] 
class MenPage(Page):
    hero_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True,on_delete=models.SET_NULL, related_name='+')
    about_body = RichTextField(blank=True, null=True)
    event_title = models.CharField(max_length=250, blank=True, null=True)
    event_body = RichTextField(blank=True, null=True)
    men_blog_title = models.CharField(max_length=2000, blank=True, null=True)
    men_blog_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True,on_delete=models.SET_NULL, related_name='+')
    men_blog_body = RichTextField(blank=True, null=True)
    content_panels = Page.content_panels + [
        ImageChooserPanel('hero_image', help_text="This is the most recent video stream"),
        FieldPanel('event_title', classname="full", help_text="This is the intro of the Page"),
        FieldPanel('event_body', classname="full", help_text="This is the intro of the Page"),
        ImageChooserPanel('men_blog_image', help_text="men blog featured image"),
        FieldPanel('men_blog_title', help_text="This is the title of the blog"),
        FieldPanel('men_blog_body',help_text="This is the body of the men blog" ),
        FieldPanel('about_body', classname="full", help_text="This is the intro of the Page"),
        InlinePanel('men_ministry_faqs', label="Frequently asked questions about the KBC Men ministry", help_text="Upload images to the carousel"),
    
    ]
class MenPageFaqs(Orderable):
    page = ParentalKey('MenPage', related_name='men_ministry_faqs')
    question = models.CharField(max_length=800, blank=True)
    answer = models.CharField (blank=True, max_length=800)
    panels = [
        FieldPanel('question'),
        FieldPanel('answer'),
    ]

class WomenPage(Page):
    featured_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True,on_delete=models.SET_NULL, related_name='+')
    about_body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('about_body', classname="full", help_text="This is the intro of the Page"),
        ImageChooserPanel('featured_image', help_text="This is the most recent video stream"),
        InlinePanel('women_ministry_faqs', label="Frequently asked questions about the KBC women ministry", help_text="Upload images to the carousel"),
    
    ]
class WomenPageFaqs(Orderable):
    page = ParentalKey('WomenPage', related_name='women_ministry_faqs')
    question = models.CharField(max_length=800, blank=True)
    answer = models.CharField (blank=True, max_length=800)
    panels = [
        FieldPanel('question'),
        FieldPanel('answer'),
    ]

class ChurchCarePage(Page):
    about_body = RichTextField(blank=True)
    hero_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True,on_delete=models.SET_NULL, related_name='+')
    featured_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True,on_delete=models.SET_NULL, related_name='+')
    content_panels = Page.content_panels + [
        FieldPanel('about_body', classname="full", help_text="This is the intro of the Page"),
        ImageChooserPanel('hero_image', help_text="This is the most recent video stream"),
        ImageChooserPanel('featured_image', help_text="This is the most recent video stream"),
        InlinePanel('church_care_ministry_faqs', label="Frequently asked questions about the KBC women ministry", help_text="Upload images to the carousel"),
    
    ]
class ChurchCarePageFaqs(Orderable):
    page = ParentalKey('ChurchCarePage', related_name='church_care_ministry_faqs')
    question = models.CharField(max_length=800, blank=True)
    answer = models.CharField (blank=True, max_length=800)
    panels = [
        FieldPanel('question'),
        FieldPanel('answer'),
    ]

class YoungAdultsPage(Page):
    hero_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True,on_delete=models.SET_NULL, related_name='+')
    about_body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('about_body', classname="full", help_text="This is the intro of the Page"),
        ImageChooserPanel('hero_image', help_text="This is the most recent video stream"),
        InlinePanel('young_adults_ministry_faqs', label="Frequently asked questions about the KBC women ministry", help_text="Upload images to the carousel"),
    
    ]
class YoungAdultsPageFaqs(Orderable):
    page = ParentalKey('YoungAdultsPage', related_name='young_adults_ministry_faqs')
    question = models.CharField(max_length=800, blank=True)
    answer = models.CharField (blank=True, max_length=800)
    panels = [
        FieldPanel('question'),
        FieldPanel('answer'),
    ]
