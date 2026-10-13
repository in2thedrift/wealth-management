"""INR formatting with Indian digit grouping (12,34,567)."""
import re
from typing import Optional

NOT_PROVIDED = "Not provided"


def format_inr(value: Optional[float], decimals: int = 0) -> str:
    """Format a number as Indian rupees. None -> 'Not provided'. Display rounding only."""
    if value is None:
        return NOT_PROVIDED
    sign = "-" if value < 0 else ""
    whole, _, frac = f"{abs(value):.{decimals}f}".partition(".")
    head, tail = whole[:-3], whole[-3:]
    if head:
        head = re.sub(r"(\d)(?=(\d\d)+$)", r"\1,", head) + ","
    return f"{sign}\u20b9{head}{tail}" + (f".{frac}" if frac else "")
