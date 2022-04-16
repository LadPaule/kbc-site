# stream fields live here
from wagtail.core import blocks

class TitleAndTextBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, help_text="Add your title")
    text = blocks.TextBlock(required=False, help_text="Add additional text")
    content = blocks.RichTextBlock(required=False, help_text="Add the rich content here")

    class Meta:
        template = "streams/title_and_text_block.html"
        icon = "edit"
        label = "Title & Text"