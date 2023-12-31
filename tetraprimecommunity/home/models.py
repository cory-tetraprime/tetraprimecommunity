from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageChooserBlock


class HomePage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),  # assuming you have 'wagtail.images' in your INSTALLED_APPS
        # you can add as many block types here as you want
    ], use_json_field=True, null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body',),
    ]

