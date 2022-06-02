from django.db import models
from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.core import blocks
from wagtail.core.models import Page, Orderable
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.core.fields import RichTextField, StreamField
from taggit.models import TaggedItemBase

from wagtail_embed_videos import get_embed_video_model_string
from wagtail_embed_videos.edit_handlers import EmbedVideoChooserPanel
from wagtailmedia.edit_handlers import MediaChooserPanel
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, StreamFieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from django.contrib.auth.models import User
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.snippets.models import register_snippet


# todo: add events landing page
class MissionsLisitingPage(Page):
    page_title = models.CharField(max_length=255, blank=True, null=True)
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('page_title'),
        FieldPanel('body', classname="full"),
        InlinePanel('missions_ministry_upcoming', label="Upcoming Missions", max_num=3),
        InlinePanel('missions_ministry_faqs', label="Frequently asked questions about the KBC missions ministry", help_text="Upload images to the carousel"),
    ]
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # TODO: Handling Pagination
        all_events_pages = MissionPage.objects.live(
        ).public().order_by('-last_published_at')

        # @TODO: paginate change integer to 8 per page
        paginator = Paginator(all_events_pages, 8)
        page = request.GET.get('page')
        try:
            events_pages = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            events_pages = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            events_pages = paginator.page(paginator.num_pages)
        context["events_pages"] = events_pages

        return context

class upcomingMissions(Orderable):
    page = ParentalKey('MissionsLisitingPage', related_name='missions_ministry_upcoming')
    mission_promo_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    mission_title = models.CharField(max_length=255, blank=True, null=True)
    mission_venue = models.CharField(max_length=255, blank=True, null=True)
    mission_date = models.DateField(blank=True, null=True)
    mission_body = RichTextField(blank=True)

    panels = [
        ImageChooserPanel('mission_promo_image'),
        FieldPanel('mission_title'),
        FieldPanel('mission_venue'),
        FieldPanel('mission_date'),
        FieldPanel('mission_body'),
    ]
class MissionsPageFaqs(Orderable):
    page = ParentalKey(MissionsLisitingPage, related_name='missions_ministry_faqs')
    question = models.CharField(max_length=800, blank=True)
    answer = models.CharField (blank=True, max_length=800)
    panels = [
        FieldPanel('question'),
        FieldPanel('answer'),
    ]
# todo: single event page
class MissionPage(Page):
    page_title = models.CharField(max_length=255, blank=True, null=True)
    featured_image = models.ForeignKey('wagtailimages.Image', null=True, on_delete=models.SET_NULL, related_name='+')
    event_date = models.DateField(blank=True, null=True)
    event_venue = models.CharField(max_length=255, blank=True, null=True)
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('page_title'),
        ImageChooserPanel('featured_image'),
        FieldPanel('event_date'),
		FieldPanel('event_venue'),
        FieldPanel('body', classname="full"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('title', partial_match=True, boost=10),
        index.SearchField('event_date', partial_match=True),
        index.SearchField('event_venue', partial_match=True),
    ]

    @route(r"^search/$")
    def search(self, request, *args, **kwargs):
        search_query = request.GET.get("q", None)
        self.event_pages = self.get_event_pages(
        ).objects.live().autocomplete("name", search_query)
        if search_query:
            self.event_pages = self.event_pages.search(search_query)
        return self.render(request)
# todo: add Summons Landing page
class SummonsLisitingPage(Page):
    page_title = models.CharField(max_length=255, blank=True, null=True)
    hero_image = models.ForeignKey('wagtailimages.Image', null=True, on_delete=models.SET_NULL, related_name='+')
    hero_title = models.CharField(max_length=255, blank=True, null=True)
    hero_caption = models.CharField(max_length=255, blank=True, null=True)
    content_panels = Page.content_panels + [
        FieldPanel('page_title'),
        ImageChooserPanel('hero_image'),
        FieldPanel('hero_title'),
        FieldPanel('hero_caption'),
        InlinePanel('summons_ministry_upcoming', label="Upcoming Summons", max_num=3),
        InlinePanel('featured_summons', label="featured summons", help_text="Upload images to the carousel", max_num=3),
    ]
class FeaturedSummons(Orderable):
    page = ParentalKey(SummonsLisitingPage, related_name='featured_summons')
    video = models.ForeignKey(get_embed_video_model_string(), null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    title = models.CharField(max_length=255, blank=True, null=True)
    media = models.ForeignKey('wagtailmedia.Media', null=True, blank=True, on_delete=models.SET_NULL, related_name="+", help_text="Video or image to be displayed on the home page")
    date = models.DateField(blank=True, null=True, help_text="Date of the summons")
    panels = [
        EmbedVideoChooserPanel('video', help_text="This is the most recent video stream"),
        MediaChooserPanel("media", media_type="audio"),
        FieldPanel('title'),
        FieldPanel('date'),
    ]
class upcomingSummons(Orderable):                      
    page = ParentalKey(SummonsLisitingPage, related_name='summons_ministry_upcoming')
    Summon_video = models.ForeignKey(get_embed_video_model_string(), null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    summons_title = models.CharField(max_length=255, blank=True, null=True)
    audio_media = models.ForeignKey('wagtailmedia.Media', null=True, blank=True, on_delete=models.SET_NULL, related_name="+", help_text="Video or image to be displayed on the home page")
    summon_date = models.DateField(blank=True, null=True, help_text="Date of the summons")
    panels = [
        EmbedVideoChooserPanel('Summon_video', help_text="This is the most recent video stream"),
        MediaChooserPanel("audio_media", media_type="audio"),
        FieldPanel('summons_title'),
        FieldPanel('summon_date'),
    ]


class ShortSummonsPage(Page):
    hero_image = models.ForeignKey('wagtailimages.Image', null=True, on_delete=models.SET_NULL, related_name='+')
    hero_title = models.CharField(max_length=255, blank=True, null=True)
    hero_caption = models.CharField(max_length=255, blank=True, null=True)
    content_panels = Page.content_panels + [
        ImageChooserPanel('hero_image'),
        FieldPanel('hero_title'),
        FieldPanel('hero_caption'),
        InlinePanel('summons', label="Upcoming Summons", max_num=6),
    ]

class Summons(Orderable):
    page = ParentalKey(ShortSummonsPage, related_name='summons')
    Summon_video = models.ForeignKey(get_embed_video_model_string(), null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    summons_title = models.CharField(max_length=255, blank=True, null=True)
    summon_date = models.DateField(blank=True, null=True, help_text="Date of the summons")
    panels = [
        EmbedVideoChooserPanel('Summon_video', help_text="This is the most recent video stream"),
        FieldPanel('summons_title'),
        FieldPanel('summon_date'),
    ]

