from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.conf.urls.static import static
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls

from django_comments_xtd import urls as django_comments_xtd_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.contrib.sitemaps.views import sitemap
from newsletter import views as newsletter_views

from search import views as search_views

urlpatterns = [
    path('django-admin/', admin.site.urls),

    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('comments', include(django_comments_xtd_urls)),
    path('newsletter/signup/', newsletter_views.signup, name='newsletter-signup'),
    path('search/', search_views.search, name='search'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path('', include('allauth.urls')),
    path('sitemap.xml', sitemap),
    path("", include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
