"""djLint Attempt to logically shrink html."""

import regex as re

from ..helpers import (
    is_ignored_block_closing,
    is_ignored_block_opening,
    is_ignored_group_closing,
    is_ignored_group_opening,
)
from ..settings import Config


def _clean_line(line: str) -> str:
    """Clean up a line of html.

    * remove duplicate spaces
    * remove trailing spaces

    """
    return re.sub(r" {2,}", " ", line.strip())


def _strip_html_whitespace(html: str, config: Config) -> str:
    """Remove unnecessary whitespace from text."""
    rawcode_flat = ""
    is_block_ignored = False
    is_group_ignored = False
    lstrip = False

    for item in html.strip().splitlines():
        # we can left strip ignored blocks on the opening tag.
        lstrip = not is_group_ignored and bool(
            re.search(config.ignored_group_opening, item, re.IGNORECASE | re.VERBOSE)
        )

        # start of ignored block. If we are already in an ingored block, keep true.
        is_group_ignored = is_group_ignored or bool(
            is_ignored_group_opening(config, item)
        )

        # find ignored blocks and retain indentation, otherwise strip white space
        if re.findall(
            fr"(?:{config.ignored_inline_blocks})",
            item,
            flags=re.IGNORECASE | re.VERBOSE,
        ):
            tmp = _clean_line(item)

        elif is_ignored_block_closing(config, item) and is_group_ignored is False:
            # do not format ignored lines
            tmp = _clean_line(item)
            is_block_ignored = False

        elif is_ignored_block_opening(config, item) and is_group_ignored is False:
            # do not format ignored lines
            tmp = _clean_line(item)
            is_block_ignored = True

        elif lstrip:
            tmp = item.lstrip()

        elif is_group_ignored or is_block_ignored:
            tmp = item

        else:
            tmp = _clean_line(item)

        # end of ignore raw code
        if is_ignored_group_closing(config, item):
            is_group_ignored = False
            lstrip = False

        rawcode_flat = rawcode_flat + tmp + "\n"

    return rawcode_flat


def compress_html(html: str, config: Config) -> str:
    """Compress back tags that do not need to be expanded."""
    # put empty tags on one line

    html = _strip_html_whitespace(html, config)

    # put short single line tags on one line
    html = re.sub(
        re.compile(
            fr"(<({config.single_line_html_tags})(?:\s(?:(?:{{%[^(?:%}}]*?%}})|(?:{{{{[^(?:}}}})]*?}}}})|[^<>])*)?>)\s*([^<\n]{{,80}})\s*?(</(\2)>)",
            re.IGNORECASE | re.MULTILINE | re.DOTALL | re.VERBOSE,
        ),
        r"\1\3\4",
        html,
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )

    # put short template tags back on one line
    html = re.sub(
        re.compile(
            rf"({{%-?[ ]*?({config.single_line_template_tags})[^\n(?:%}})]{{,30}}%}})\s*([^%\n]{{,50}})\s*?({{%-?[ ]+?end(\2)[ ]*?%}})",
            flags=re.IGNORECASE | re.MULTILINE | re.VERBOSE,
        ),
        r"\1\3\4",
        html,
    )

    return html
