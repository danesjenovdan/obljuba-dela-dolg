from django import forms
from django.core.paginator import Paginator
from django.db import models
from django.db.models import Max
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    StreamFieldPanel,
)
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from ..blocks import RichTextBlock
from .promise import PromiseCategory, PromiseStatus


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
    more_link_text = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name=_('Slika'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
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
    latest_button_text = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    social_heading = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    newsletter_image = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name=_('Slika ob polju za prijavo na novice'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    social_media_image = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name=_('Slika ob polju za delitev na družbenih omrežjih'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        PageChooserPanel("more_link"),
        FieldPanel("more_link_text"),
        ImageChooserPanel("image"),
        FieldPanel("categories_heading"),
        FieldPanel("search_heading"),
        FieldPanel("search_placeholder"),
        PageChooserPanel("search_link"),
        FieldPanel("latest_heading"),
        PageChooserPanel("latest_link"),
        FieldPanel("latest_button_text"),
        FieldPanel("social_heading"),
        ImageChooserPanel("newsletter_image"),
        ImageChooserPanel("social_media_image"),
    ]

    parent_page_types = []

    def get_context(self, request):
        context = super().get_context(request)
        context["promise_categories"] = PromiseCategory.objects.all()
        context["promises"] = (
            PromisePage.objects.all()
            .live()
            .annotate(latest_update=Max("updates__date"))
            .order_by("-latest_update")[:10]
        )
        return context


class PromisePage(Page):
    full_text = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Polno besedilo obljube"),
    )
    quote = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Citat"),
    )
    source_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Ime vira"),
    )
    source_url = models.URLField(
        null=True,
        blank=True,
        verbose_name=_("Povezava do vira"),
    )
    categories = ParentalManyToManyField(
        "home.PromiseCategory",
        blank=True,
        verbose_name=_("Kategorije"),
    )

    content_panels = Page.content_panels + [
        FieldPanel("full_text"),
        FieldPanel("quote"),
        MultiFieldPanel(
            [
                FieldPanel("source_name"),
                FieldPanel("source_url"),
            ],
            heading="Vir",
        ),
        FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
        InlinePanel("updates", label="Posodobitve", min_num=1),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("full_text"),
    ]

    parent_page_types = ["home.PromiseListingPage"]

    def sorted_updates(self):
        return self.updates.order_by("-date")

    def status(self):
        latest_update = self.updates.order_by("-date").last()
        return latest_update.status if latest_update else None

    class Meta:
        verbose_name = "Obljuba"
        verbose_name_plural = "Obljube"


class PromiseListingPage(Page):
    search_title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Naslov te strani, ko prikazuje rezultate iskanja"),
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

    parent_page_types = ["home.HomePage"]

    def get_context(self, request):
        context = super().get_context(request)
        context["promise_categories"] = PromiseCategory.objects.all()
        context["promise_statuses"] = PromiseStatus.objects.all().order_by('order_no')

        all_promises = (
            PromisePage.objects.all()
            .child_of(self)
            .annotate(latest_update=Max("updates__date"))
            .order_by("-latest_update")
        )

        search_query = request.GET.get("query", None)
        if search_query:
            all_promises = all_promises.search(
                search_query,
                operator="and",
            ).get_queryset()

        category = request.GET.get("category", None)
        if category:
           all_promises = all_promises.filter(categories__slug=category)


        paginator = Paginator(all_promises, 100)
        page_number = request.GET.get("page", 1)
        promises = paginator.get_page(page_number)
        context["promises"] = promises
        context["paginator"] = paginator

        return context

    class Meta:
        verbose_name = "Seznam obljub"
        verbose_name_plural = "Seznami obljub"


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

    class Meta:
        verbose_name = "Vsebina"
        verbose_name_plural = "Vsebine"
