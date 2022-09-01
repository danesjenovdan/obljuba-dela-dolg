from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable
from wagtail.images.edit_handlers import ImageChooserPanel


class PromiseCategory(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Ime"),
    )
    slug = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Ključ (če je prazno se avtomatsko ustvari iz imena)"),
    )
    image_card = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name=_("Slika na kartici"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    image_listing_page = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name=_("Slika na seznamu obljub"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    mandate = models.ForeignKey(
        "home.PromiseListingPage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Mandat vlade"),
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        if self.mandate:
            return self.name + " --- " + self.mandate.title
        else:
            return self.name

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        ImageChooserPanel("image_card"),
        ImageChooserPanel("image_listing_page"),
        FieldPanel("mandate"),
    ]

    class Meta:
        verbose_name = "Kategorija obljub"
        verbose_name_plural = "Kategorije obljub"


class PromiseStatus(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Ime"),
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Opis"),
    )
    slug = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Ključ (če je prazno se avtomatsko ustvari iz imena)"),
    )
    color = models.CharField(
        max_length=32,
        verbose_name=_(
            "Barva (veljavni vsi css formati, npr. rgb(255, 255, 255), #fff ali #ffffff)"
        ),
    )
    icon = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name=_("Ikona"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    order_no = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name=_("Vrstni red"),
        default=1,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
        FieldPanel("slug"),
        FieldPanel("color"),
        ImageChooserPanel("icon"),
        FieldPanel("order_no"),
    ]

    class Meta:
        verbose_name = "Stanje obljub"
        verbose_name_plural = "Stanja obljub"


class PromiseUpdate(Orderable):
    page = ParentalKey(
        "home.PromisePage",
        on_delete=models.CASCADE,
        related_name="updates",
    )
    title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Naslov"),
    )
    # TODO this field should be renamed
    # to timestamp or something
    date = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("Datum"),
    )
    update_author = models.TextField(
        blank=True,
        verbose_name=_("Avtor/ica posodobitve")
    )
    status = models.ForeignKey(
        "home.PromiseStatus",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("Stanje"),
    )
    content = RichTextField(
        null=True,
        blank=True,
        verbose_name=_("Vsebina"),
    )
    conclusion = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Sklep"),
    )

    class Meta:
        ordering = ['date']


class Party(models.Model):
    name = models.TextField(verbose_name=_("Ime stranke"))
    icon = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name=_("Logotip"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    mandate = models.ForeignKey(
        "home.PromiseListingPage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Mandat vlade"),
    )

    def __str__(self):
        return self.name + ", " + self.mandate.title if self.name and self.mandate else self.name

    panels = [
        FieldPanel("name"),
        ImageChooserPanel("icon"),
        FieldPanel("mandate"),
    ]

    class Meta:
        verbose_name = "Stranka"
        verbose_name_plural = "Stranke"

class PartyMember(models.Model):
    name = models.TextField(verbose_name=_("Ime"))
    role = models.TextField(verbose_name=_("Vloga"))
    image = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name=_("Slika"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    party = models.ForeignKey(
        Party,
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("Stranka"),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("role"),
        ImageChooserPanel("image"),
        FieldPanel("party"),
    ]

    class Meta:
        verbose_name = "Član vlade"
        verbose_name_plural = "Člani vlade"