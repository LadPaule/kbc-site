# stream fields live here
from wagtail.core import blocks
from wagtail.contrib.table_block.blocks import TableBlock

class TableBlock(blocks.StreamBlock):
    table = TableBlock()

    class Meta:
        icon = "table"
        label = "Table"