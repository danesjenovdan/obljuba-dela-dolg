from django.utils.html import escape
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)
from wagtail.core import hooks
from wagtail.core.rich_text import LinkHandler

from .models import PromiseCategory, PromiseStatus, Party


class NewTabExternalLinkHandler(LinkHandler):
    identifier = "external"

    @classmethod
    def expand_db_attributes(cls, attrs):
        href = attrs["href"]
        return '<a href="%s" target="_blank">' % escape(href)


# Run hook with order=1 so it runs after admin is loaded (default order=0) and overrides rules
@hooks.register("register_rich_text_features", order=1)
def register_extra_rich_text_features(features):
    features.default_features.append("blockquote")

    features.register_link_type(NewTabExternalLinkHandler)


class PromiseCategoryAdmin(ModelAdmin):
    model = PromiseCategory
    menu_icon = "folder-inverse"
    list_display = ("name",)


class PromiseStatusAdmin(ModelAdmin):
    model = PromiseStatus
    menu_icon = "tag"
    list_display = ("name",)


class PartyAdmin(ModelAdmin):
    model = Party
    menu_icon = "group"
    list_display = ("name",)


class PromiseGroup(ModelAdminGroup):
    menu_label = "Ostalo"
    menu_icon = "folder-open-inverse"
    menu_order = 200
    items = (
        PromiseCategoryAdmin,
        PromiseStatusAdmin,
        PartyAdmin,
    )


modeladmin_register(PromiseGroup)
