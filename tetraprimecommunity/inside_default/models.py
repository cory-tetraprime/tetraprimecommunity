from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageChooserBlock


class InsidePage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),  # assuming you have 'wagtail.images' in your INSTALLED_APPS
        # you can add as many block types here as you want
    ], use_json_field=True, null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body',),
    ]

    # This is optional: it helps define how your model will appear in the Wagtail admin
    class Meta:
        verbose_name = "Inside Page"
        verbose_name_plural = "Inside Pages"
