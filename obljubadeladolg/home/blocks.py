from django.utils.translation import gettext_lazy as _
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.core import blocks


class RichTextBlock(blocks.StructBlock):
    alignment = blocks.ChoiceBlock(
        choices=[
            ("start", "Leva"),
            ("center", "Sredinska"),
            ("end", "Desna"),
        ],
        label=_("Poravnava"),
    )
    aligned_content = blocks.StreamBlock(
        [
            (
                "text",
                blocks.RichTextBlock(
                    label=_("Obogateno besedilo"),
                ),
            ),
            (
                "table",
                TableBlock(
                    label=_("Tabela"),
                    template="home/blocks/table.html",
                ),
            ),
        ],
        label=_("Vsebina"),
    )

    class Meta:
        label = _("Obogateno besedilo")
        template = "home/blocks/rich_text.html"
        icon = "pilcrow"
