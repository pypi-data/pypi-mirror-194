"""Implementation of Rule L023."""

from typing import List

from sqlfluff.core.rules import BaseRule, LintResult, RuleContext
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler

from sqlfluff.utils.functional import FunctionalContext, sp
from sqlfluff.utils.reflow.sequence import ReflowSequence


class Rule_L023(BaseRule):
    """Single whitespace expected after ``AS`` in ``WITH`` clause.

    **Anti-pattern**

    .. code-block:: sql

        WITH plop AS(
            SELECT * FROM foo
        )

        SELECT a FROM plop


    **Best practice**

    Add a space after ``AS``, to avoid confusing it for a function.
    The ``•`` character represents a space.

    .. code-block:: sql
       :force:

        WITH plop AS•(
            SELECT * FROM foo
        )

        SELECT a FROM plop
    """

    groups = ("all", "core")
    crawl_behaviour = SegmentSeekerCrawler({"common_table_expression"})
    target_keyword = "AS"
    strip_newlines = True
    is_fix_compatible = True

    def _eval(self, context: RuleContext) -> List[LintResult]:
        """Single whitespace expected in mother middle segment."""
        functional = FunctionalContext(context)

        as_keyword = (
            functional.segment.children(sp.is_keyword(self.target_keyword))
            .first()
            .get()
        )
        if not as_keyword:
            # No target keyword. Abort.
            return []

        # Respace the section immediately after the keyword. If any fixes
        # are returned it implies there was an issue.
        return (
            ReflowSequence.from_around_target(
                as_keyword,
                context.parent_stack[0],
                config=context.config,
                sides="after",
            )
            .respace(strip_newlines=self.strip_newlines)
            .get_results()
        )
