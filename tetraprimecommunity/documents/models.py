from django.db import models

from wagtail.documents.models import Document, AbstractDocument

class CustomDocument(AbstractDocument):
    source = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    admin_form_fields = Document.admin_form_fields + (
        'source',
    )

