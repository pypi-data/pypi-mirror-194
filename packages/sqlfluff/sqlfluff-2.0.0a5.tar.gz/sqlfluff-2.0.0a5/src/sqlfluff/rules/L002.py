"""Implementation of Rule L002."""
from typing import Optional

from sqlfluff.core.rules import BaseRule, LintResult, LintFix, RuleContext
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler


class Rule_L002(BaseRule):
    """Mixed Tabs and Spaces in single whitespace.

    This rule will fail if a single section of whitespace
    contains both tabs and spaces.

    **Anti-pattern**

    The ``•`` character represents a space and the ``→`` character represents a tab.
    In this example, the second line contains two spaces and one tab.

    .. code-block:: sql
       :force:

        SELECT
        ••→a
        FROM foo

    **Best practice**

    Change the line to use spaces only.

    .. code-block:: sql
       :force:

        SELECT
        ••••a
        FROM foo

    """

    # TODO: combine with other LN01 rules
    name = "layout.indent.a"
    aliases = ("LN01a",)
    groups = ("all", "core", "layout")
    crawl_behaviour = SegmentSeekerCrawler({"whitespace"}, provide_raw_stack=True)
    is_fix_compatible = True

    def _eval(self, context: RuleContext) -> Optional[LintResult]:
        """Mixed Tabs and Spaces in single whitespace.

        Only trigger from whitespace segments if they contain
        multiple kinds of whitespace.
        """
        # Config type hints
        # TODO: Migrate to reflow?
        tab_space_size: int = context.config.get("tab_space_size", ["indentation"])

        if context.segment.is_type("whitespace"):
            if " " in context.segment.raw and "\t" in context.segment.raw:
                if not context.raw_stack or context.raw_stack[-1].is_type("newline"):
                    # We've got a single whitespace at the beginning of a line.
                    # It's got a mix of spaces and tabs. Replace each tab with
                    # a multiple of spaces
                    return LintResult(
                        anchor=context.segment,
                        fixes=[
                            LintFix.replace(
                                context.segment,
                                [
                                    context.segment.edit(
                                        context.segment.raw.replace(
                                            "\t", " " * tab_space_size
                                        )
                                    ),
                                ],
                            ),
                        ],
                    )
        return None
