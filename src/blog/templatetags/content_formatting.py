import re

from django import template
from django.utils.html import format_html, format_html_join

register = template.Library()


@register.filter
def article_content(value):
    blocks = re.split(r"\n\s*\n", value.strip())
    rendered_blocks = []

    for block in blocks:
        heading = re.fullmatch(r"(#{1,3})\s+(.+)", block.strip())
        if heading:
            level = len(heading.group(1))
            rendered_blocks.append(
                format_html(
                    "<h{}>{}</h{}>",
                    level,
                    heading.group(2),
                    level,
                )
            )
            continue

        lines = format_html_join("<br>", "{}", ((line,) for line in block.splitlines()))
        rendered_blocks.append(format_html("<p>{}</p>", lines))

    return format_html_join("", "{}", ((block,) for block in rendered_blocks))
