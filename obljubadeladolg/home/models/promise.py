from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


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
    # TODO: icon

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Stanje obljub"
        verbose_name_plural = "Stanja obljub"
