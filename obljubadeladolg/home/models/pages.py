from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from ..blocks import RichTextBlock


class HomePage(Page):
    pass


class ContentPage(Page):
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Opis"),
    )
    body = StreamField(
        [("rich_text", RichTextBlock())],
        null=True,
        blank=True,
        verbose_name=_("Vsebina"),
    )

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        StreamFieldPanel("body"),
    ]
