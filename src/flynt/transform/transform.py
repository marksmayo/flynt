import ast
import copy
import logging
from typing import Tuple

from flynt import state
from flynt.exceptions import ConversionRefused
from flynt.format import QuoteTypes
from flynt.transform.FstringifyTransformer import fstringify_node
from flynt.utils import fixup_transformed

log = logging.getLogger(__name__)


def transform_chunk(
    code: str,
    quote_type: str = QuoteTypes.triple_double,
    transform_percent: bool = True,
    transform_format: bool = True,
) -> Tuple[str, bool]:
    """Convert a block of code to an f-string

    Args:
        code: The code to convert.
        quote_type: the quote type to use for the transformed result
        transform_percent: whether to transform percent format strings
        transform_format: whether to transform format calls

    Returns:
       Tuple: resulting code, boolean: was it changed?
    """

    try:
        tree = ast.parse(code)
        converted, changed, str_in_str = fstringify_node(
            copy.deepcopy(tree),
            transform_percent=transform_percent,
            transform_format=transform_format,
        )
    except ConversionRefused as cr:
        log.warning("Not converting code '%s': %s", code, cr)
        state.invalid_conversions += 1
        return code, False
    except Exception:
        log.exception("Exception during conversion of code '%s'", code)
        state.invalid_conversions += 1
        return code, False
    else:
        if changed:
            if str_in_str and quote_type == QuoteTypes.single:
                quote_type = QuoteTypes.double
            new_code = fixup_transformed(converted, quote_type=quote_type)
            try:
                ast.parse(new_code)
            except SyntaxError:
                log.error(
                    "Failed to parse transformed code '%s'' given original '%s'",
                    new_code,
                    code,
                    exc_info=True,
                )
                state.invalid_conversions += 1
                return code, False
            else:
                return new_code, changed

        return code, False
