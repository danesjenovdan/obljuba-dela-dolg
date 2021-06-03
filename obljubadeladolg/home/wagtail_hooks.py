from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)

from .models import PromiseCategory, PromiseStatus


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
