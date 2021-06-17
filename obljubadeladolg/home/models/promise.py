from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from modelcluster.fields import ParentalKey
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable


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
    image = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name=_('Slika'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

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
        'wagtailimages.Image',
        verbose_name=_('Ikona'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    order_no = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name=_("Vrstni red"),
        default=1
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

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
    date = models.DateField(
        default=timezone.now,
        verbose_name=_("Datum"),
    )
    status = models.ForeignKey(
        "home.PromiseStatus",
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
        blank=True,
        verbose_name=_("Stanje"),
    )
    content = RichTextField(
        null=True,
        blank=True,
        verbose_name=_("Vsebina"),
    )
