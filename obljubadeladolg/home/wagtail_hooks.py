from django.utils.html import escape
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)
from wagtail.core import hooks
from wagtail.core.rich_text import LinkHandler

from .models import PromiseCategory, PromiseStatus


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
    menu_icon = "group"
    list_display = ("name",)


class PromiseStatusAdmin(ModelAdmin):
    model = PromiseStatus
    menu_icon = "time"
    list_display = ("name",)


class PromiseGroup(ModelAdminGroup):
    menu_label = "Obljube"
    menu_icon = "folder-open-inverse"
    menu_order = 200
    items = (
        PromiseCategoryAdmin,
        PromiseStatusAdmin,
    )


modeladmin_register(PromiseGroup)
