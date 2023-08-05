"""Implementation of Rule L006."""


from typing import List

from sqlfluff.core.rules import (
    BaseRule,
    LintResult,
    RuleContext,
)
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler
from sqlfluff.utils.reflow import ReflowSequence


class Rule_L006(BaseRule):
    """Operators should be surrounded by a single whitespace.

    **Anti-pattern**

    In this example, there is a space missing between the operator and ``b``.

    .. code-block:: sql

        SELECT
            a +b
        FROM foo


    **Best practice**

    Keep a single space.

    .. code-block:: sql

        SELECT
            a + b
        FROM foo
    """

    name = "spacing.operators"
    aliases = ("LS03",)
    groups = ("all", "core", "layout", "spacing")
    crawl_behaviour = SegmentSeekerCrawler(
        {"binary_operator", "comparison_operator", "assignment_operator"}
    )
    is_fix_compatible = True

    def _eval(self, context: RuleContext) -> List[LintResult]:
        """Operators should be surrounded by a single whitespace.

        Rewritten to assess direct children of a segment to make
        whitespace insertion more sensible.

        We only need to handle *missing* whitespace because excess
        whitespace is handled by L039.

        NOTE: We also allow bracket characters either side.
        """
        # Iterate through children of this segment looking for any of the
        # target types. We also check for whether any of the children start
        # or end with the targets.

        # We ignore any targets which start or finish this segment. They'll
        # be dealt with by the parent segment. That also means that we need
        # to have at least three children.

        # Operators can be either a single raw segment or multiple, and
        # a significant number of them are multiple (thanks TSQL). While
        # we could provide an alternative route for single raws, this is
        # implemented to separately look before, and after. In the single
        # raw case - they'll be targeting the same segment, and potentially
        # waste some processing overhead, but this makes the code simpler.

        # If this is an operator within an operator, we'll double count
        # so abort.
        if context.parent_stack and context.parent_stack[-1].is_type(
            "assignment_operator"
        ):
            return []

        results = (
            ReflowSequence.from_around_target(
                context.segment, context.parent_stack[0], config=context.config
            )
            .respace()
            .get_results()
        )

        # Because *excess whitespace* is handled elsewhere until 2.0.0
        # we should only return results which *create* whitespace.

        return [
            result
            for result in results
            if all(fix.edit_type.startswith("create") for fix in result.fixes)
        ]
