"""Implementation of Rule L040."""

from typing import Tuple, List
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler

from sqlfluff.rules.L010 import Rule_L010


class Rule_L040(Rule_L010):
    """Inconsistent capitalisation of boolean/null literal.

    **Anti-pattern**

    In this example, ``null`` and ``false`` are in lower-case whereas ``TRUE`` is in
    upper-case.

    .. code-block:: sql

        select
            a,
            null,
            TRUE,
            false
        from foo

    **Best practice**

    Ensure all literal ``null``/``true``/``false`` literals are consistently
    upper or lower case

    .. code-block:: sql

        select
            a,
            NULL,
            TRUE,
            FALSE
        from foo

        -- Also good

        select
            a,
            null,
            true,
            false
        from foo

    """

    name = "capitalisation.literals"
    aliases = ("CP04",)

    crawl_behaviour = SegmentSeekerCrawler({"null_literal", "boolean_literal"})
    _exclude_elements: List[Tuple[str, str]] = []
    _description_elem = "Boolean/null literals"
    is_fix_compatible = True
