"""Implementation of Rule L004."""
from sqlfluff.core.parser import WhitespaceSegment
from sqlfluff.core.rules import BaseRule, LintResult, LintFix, RuleContext
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler
from sqlfluff.utils.reflow.reindent import construct_single_indent


class Rule_L004(BaseRule):
    """Incorrect indentation type.

    .. note::
       Note 1: spaces are only fixed to tabs if the number of spaces in the
       indent is an integer multiple of the ``tab_space_size`` config.

       Note 2: fixes are only applied to indents at the start of a line. Indents
       after other text on the same line are not fixed.

    **Anti-pattern**

    Using tabs instead of spaces when ``indent_unit`` config set to ``space`` (default).

    .. code-block:: sql
       :force:

        select
        ••••a,
        →   b
        from foo

    **Best practice**

    Change the line to use spaces only.

    .. code-block:: sql
       :force:

        select
        ••••a,
        ••••b
        from foo
    """

    # TODO: combine with other LN01 rules
    name = "layout.indent.c"
    aliases = ("LN01c",)
    groups = ("all", "core", "layout")
    crawl_behaviour = SegmentSeekerCrawler({"whitespace"}, provide_raw_stack=True)
    is_fix_compatible = True

    # TODO fix indents after text:
    # https://github.com/sqlfluff/sqlfluff/pull/590#issuecomment-739484190
    def _eval(self, context: RuleContext) -> LintResult:
        """Incorrect indentation found in file."""
        # Config type hints
        tab_space_size: int = context.config.get("tab_space_size", ["indentation"])
        indent_unit: str = context.config.get("indent_unit", ["indentation"])

        tab = "\t"
        space = " "
        correct_indent = construct_single_indent(indent_unit, tab_space_size)
        wrong_indent = tab if indent_unit == "space" else space * tab_space_size
        if (
            context.segment.is_type("whitespace")
            and wrong_indent in context.segment.raw
        ):
            fixes = []
            description = "Incorrect indentation type found in file."
            edit_indent = context.segment.raw.replace(wrong_indent, correct_indent)
            pre_seg = context.raw_stack[-1] if context.raw_stack else None
            # Ensure that the number of space indents is a multiple of tab_space_size
            # before attempting to convert spaces to tabs to avoid mixed indents
            # unless we are converted tabs to spaces (indent_unit = space)
            if (
                (
                    indent_unit == "space"
                    or context.segment.raw.count(space) % tab_space_size == 0
                )
                # Only attempt a fix at the start of a newline for now
                and (pre_seg is None or pre_seg.is_type("newline"))
            ):
                fixes = [
                    LintFix.replace(
                        context.segment,
                        [
                            WhitespaceSegment(raw=edit_indent),
                        ],
                    )
                ]
            elif not (pre_seg is None or pre_seg.is_type("newline")):
                # give a helpful message if the wrong indent has been found and is not
                # at the start of a newline
                description += (
                    " The indent occurs after other text, so a manual fix is needed."
                )
            else:
                # If we get here, the indent_unit is tabs, and the number of spaces is
                # not a multiple of tab_space_size
                description += " The number of spaces is not a multiple of "
                "tab_space_size, so a manual fix is needed."
            return LintResult(
                anchor=context.segment, fixes=fixes, description=description
            )
        return LintResult()
