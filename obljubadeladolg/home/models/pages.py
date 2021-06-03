from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from ..blocks import RichTextBlock


class HomePage(Page):
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Opis"),
    )
    more_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    categories_heading = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    search_heading = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    search_placeholder = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    search_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    latest_heading = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    latest_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    social_heading = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        PageChooserPanel("more_link"),
        FieldPanel("categories_heading"),
        FieldPanel("search_heading"),
        FieldPanel("search_placeholder"),
        PageChooserPanel("search_link"),
        FieldPanel("latest_heading"),
        PageChooserPanel("latest_link"),
        FieldPanel("social_heading"),
    ]

    parent_page_types = []


class PromiseListingPage(Page):
    search_title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    category_label = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    category_placeholder = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    search_label = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    search_placeholder = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    status_help_label = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    status_help_text = models.TextField(
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("search_title"),
        FieldPanel("category_label"),
        FieldPanel("category_placeholder"),
        FieldPanel("search_label"),
        FieldPanel("search_placeholder"),
        FieldPanel("status_help_label"),
        FieldPanel("status_help_text"),
    ]


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
