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
from .promise import PromiseCategory, PromiseStatus, PromiseUpdate, Party, PartyMember


class HomePage(Page):
    subtitle = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Podnaslov"),
    )
    # če ne bo popravkov, izbriši ta field
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
        verbose_name=_("Povezava do prejšnjega mandata"),
    )
    # če ne bo popravkov, izbriši ta field
    more_link_text = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Povezava pod opisom (tekst)"),
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name=_('Naslovna slika'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    current_mandate = models.ForeignKey(
        "wagtailcore.Page",
        verbose_name=_('Trenutno aktualna stran z obljubami'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    current_mandate_government_page = models.ForeignKey(
        "wagtailcore.Page",
        verbose_name=_('Trenutno aktualna vladna stran'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        # FieldPanel("description"),
        PageChooserPanel("more_link"),
        # FieldPanel("more_link_text"),
        ImageChooserPanel("image"),
        PageChooserPanel("current_mandate"),
        PageChooserPanel("current_mandate_government_page"),
    ]

    parent_page_types = []

    def get_context(self, request):
        context = super().get_context(request)

        context["promise_categories"] = PromiseCategory.objects.all().order_by('id') # TODO this is a hack

        promises = (
            PromisePage.objects.live()
            .child_of(self.current_mandate) # promises that belong to this mandate
        )
        context["promises"] = promises.annotate(latest_update=Max("updates__date")).order_by("-latest_update")[:5]
        
        all_statuses = PromiseStatus.objects.all().order_by('order_no')
        context["promise_statuses"] = all_statuses
        # get number of filtered promises for each status
        promises_by_statuses = {}
        for promise in promises:
            if (promises_by_statuses.get(promise.status.slug)):
                promises_by_statuses[promise.status.slug].append(promise)
            else:
                promises_by_statuses[promise.status.slug] = [promise]
        context["promises_by_statuses"] = promises_by_statuses

        context["current_mandate"] = self.current_mandate

        return context


class PromisePage(Page):
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
    # to polje ostane, ker imajo stare obljube tu dodane slike, ampak se skrije v adminu
    image = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name=_('Slika'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    meta_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='OG slika',
    )
    party = models.ForeignKey(
        'Party', 
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Stranka, ki je dala obljubo',
    )
    party_promised = models.TextField(
        blank=True, 
        verbose_name='Stranka je obljubila'
    )
    newsletter_box_title = models.TextField(
        blank=True,
        verbose_name='Novičnik naslov v škatli'
    )
    newsletter_box_text = models.TextField(
        blank=True,
        verbose_name='Novičnik tekst v škatli'
    )

    content_panels = Page.content_panels + [
        FieldPanel("quote"),
        MultiFieldPanel(
            [
                FieldPanel("source_name"),
                FieldPanel("source_url"),
            ],
            heading="Vir",
        ),
        # ImageChooserPanel("image"),
        FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
        FieldPanel("party"),
        FieldPanel("party_promised"),
        InlinePanel("updates", label="Posodobitve", min_num=1),
        FieldPanel("newsletter_box_title"),
        FieldPanel("newsletter_box_text"),
    ]

    promote_panels = Page.promote_panels + [
        ImageChooserPanel("meta_image"),
    ]

    search_fields = Page.search_fields # + [ index.SearchField("full_text"), ]

    parent_page_types = ["home.PromiseListingPage"]

    def sorted_updates(self):
        return self.updates.order_by("date")[1:] # vemo, da bo vedno vsaj ena, sicer obljube ne moreš ustvariti

    @property
    def latest_updates(self):
        sorted_updates = self.updates.order_by("-date")
        latest_update = sorted_updates.first() if sorted_updates else None
        second_to_latest_update = sorted_updates[1] if len(sorted_updates) > 1 else None
        return (latest_update, second_to_latest_update)

    @property
    def status(self):
        latest_update = self.updates.order_by("-date").first()
        return latest_update.status if latest_update else None

    @property
    def first_category(self):
        cat = self.categories.first()
        return cat.image_card if cat else None


    def get_context(self, request):
        context = super().get_context(request)
        context["current_mandate"] = self.get_parent()

        return context

    class Meta:
        verbose_name = "Obljuba"
        verbose_name_plural = "Obljube"

# ta model predstavlja eno vlado
class PromiseListingPage(Page):
    about_statuses_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Povezava do strani z razlago 'Kaj pomenijo posamezni statusi?'"
    )

    content_panels = Page.content_panels + [
        FieldPanel("about_statuses_link"),
    ]

    parent_page_types = ["home.HomePage"]

    def get_context(self, request):
        context = super().get_context(request)
        context["promise_categories"] = PromiseCategory.objects.all()
        all_statuses = PromiseStatus.objects.all().order_by('order_no')
        context["promise_statuses"] = all_statuses

        # kje je to že needed? 
        context['category_image'] = None
        chosen_category = PromiseCategory.objects.filter(slug=request.GET.get('kategorija', None)).first()
        if chosen_category:
            context['category_image'] = chosen_category.image_listing_page
            context['category_name'] = chosen_category.name
        # ***********************

        # get set of all promises and order them by latest update
        all_promises = (
            PromisePage.objects.all()
            .child_of(self) # promises that belong to this mandate
            .annotate(latest_update=Max("updates__date"))
            .order_by("latest_update")
        )

        # filter promises by search query, if there is one in url params
        search_query = request.GET.get("isci", None)
        if search_query:
            filtered_promises = all_promises.search(
                search_query,
                operator="and",
            ).get_queryset()
        else:
            filtered_promises = all_promises

        # filter promises by category, if there is one in url params
        category = request.GET.get("kategorija", None)
        if category:
           filtered_promises = filtered_promises.filter(categories__slug=category)

        # save number of all promises before filtering by status
        context["promises_no_all_statuses"] = len(filtered_promises)

        # get number of filtered promises for each status
        promises_by_statuses = {}
        for promise in filtered_promises:
            if (promises_by_statuses.get(promise.status.slug)):
                promises_by_statuses[promise.status.slug].append(promise)
            else:
                promises_by_statuses[promise.status.slug] = [promise]
        context["promises_by_statuses"] = promises_by_statuses

        # filter promises by status, if there is one in url params
        status_slug = request.GET.get("status", None)
        if status_slug:
            chosen_status = PromiseStatus.objects.filter(slug=status_slug).first()
            if chosen_status:
                context['chosen_status'] = chosen_status
            if (promises_by_statuses.get(status_slug)):
                filtered_promises = promises_by_statuses[status_slug]
            else:
                filtered_promises = []


        paginator = Paginator(filtered_promises, 100)
        page_number = request.GET.get("page", 1)
        promises = paginator.get_page(page_number)
        context["promises"] = promises
        context["paginator"] = paginator

        context["current_mandate"] = self

        return context

    class Meta:
        verbose_name = "Vlada"
        verbose_name_plural = "Vlade"


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
    meta_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        StreamFieldPanel("body"),
    ]

    promote_panels = Page.promote_panels + [
        ImageChooserPanel("meta_image"),
    ]

    class Meta:
        verbose_name = "Navadna stran z vsebino"
        verbose_name_plural = "Navadne strani z vsebino"

class NewsletterPage(Page):
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
        verbose_name = "Stran za urejanje naročnine"
        verbose_name_plural = "Strani za urejanje naročnine"

class GovernmentPage(Page):
    mandate = models.ForeignKey(
        "home.PromiseListingPage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Vladna stran za:"),
    )
    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("Slika v glavi"),
    )

    content_panels = Page.content_panels + [
        FieldPanel("mandate"),
        ImageChooserPanel("header_image"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["current_mandate"] = self.mandate

        mandate_parties = Party.objects.filter(mandate=self.mandate)
        context["mandate_parties"] = mandate_parties

        context["government_members"] = PartyMember.objects.filter(party__in=mandate_parties)

        return context

    class Meta:
        verbose_name = "Opis vlade"
        verbose_name_plural = "Opisi vlade"
