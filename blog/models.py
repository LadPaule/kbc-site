from django.db import models
from django import forms

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey, ParentalManyToManyField

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from wagtail.snippets.models import register_snippet
from wagtail.search import index

from wagtail.contrib.routable_page.models import RoutablePageMixin, route

class BlogIndexPage(RoutablePageMixin, Page):

    # getting the posts to  appear in a reverse order
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        #@TODO: Handling Pagination
        all_sponsored_pages = BlogPage.objects.live().public().order_by('-last_published_at')

        paginator = Paginator(all_sponsored_pages, 4) #@TODO: paginate change integer to 8 per page
        page = request.GET.get('page')
        try:
            sponsored_pages = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            sponsored_pages = paginator.page(1)    
        except EmptyPage:  
            # If page is out of range (e.g. 9999), deliver last page of results.
            sponsored_pages = paginator.page(paginator.num_pages)
        context["sponsored_pages"] = sponsored_pages

        return context

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class BlogTagIndexPage(Page):

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context

@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'blog categories'

class BlogPage(RoutablePageMixin, Page):
    date = models.DateField("Post date")
    author= models.CharField(max_length=100, default='Pr. Andrew Mwenge')
    comments=RichTextField(blank=True)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None
    search_fields = Page.search_fields + [
        index.SearchField('categories', partial_match=True, boost=10),
        index.SearchField('tags', partial_match=True),
        index.SearchField('date', partial_match=True),
        index.SearchField('body', partial_match=True),
    ]
    @route(r"^search/$")
    def search(self, request, *args, **kwargs):
        search_query = request.GET.get("q", None)
        self.sponsored_pages = self.get_sponsored_pages().objects.live().autocomplete("categories", search_query)
        if search_query:
            self.sponsored_pages = self.sponsored_pages.search(search_query)
        return self.render(request)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('author'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Blog Information"),
        FieldPanel('body', classname="full"),
        InlinePanel('gallery_images', label="Gallery images"),
        FieldPanel('comments'),
    ]

class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]