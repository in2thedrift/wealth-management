"""Generic slab-based tax engine. It contains NO rule values: slabs, cess and rebate are inputs the user
(or a verified FY rules file) supplies. Verify rules at incometax.gov.in before relying on any result."""
from typing import List, Optional, Tuple

Slab = Tuple[Optional[float], float]  # (upper limit or None for no limit, rate in %)


def slab_tax(taxable: float, slabs: List[Slab]) -> float:
    if taxable < 0:
        raise ValueError("Taxable income cannot be negative.")
    tax, lower = 0.0, 0.0
    for upper, rate in slabs:
        top = taxable if upper is None else min(taxable, upper)
        if top > lower:
            tax += (top - lower) * rate / 100
        if upper is None or taxable <= upper:
            break
        lower = upper
    return tax


def total_tax(taxable: float, slabs: List[Slab], cess_pct: float = 4.0, rebate_income_limit: float = 0.0, rebate_max: float = 0.0) -> dict:
    base = slab_tax(taxable, slabs)
    rebate = min(base, rebate_max) if taxable <= rebate_income_limit else 0.0
    after = base - rebate
    cess = after * cess_pct / 100
    return dict(slab_tax=base, rebate=rebate, cess=cess, total=after + cess)
