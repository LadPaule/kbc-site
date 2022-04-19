from wagtail.contrib.modeladmin.options import modeladmin_register
from birdsong.options import CampaignAdmin

from .models import Newsletter


@modeladmin_register
class NewsletterAdmin(CampaignAdmin):
    campaign = Newsletter
    menu_label = 'Newsletter'
    menu_icon = 'mail'
    menu_order = 200