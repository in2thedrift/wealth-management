"""Transparent financial-health indicators. Not a score; each indicator explains itself."""
from typing import Dict, Optional


def _div(a: float, b: float) -> Optional[float]:
    return None if b == 0 else a / b


def assess(income: Optional[float], essential: Optional[float], discretionary: float = 0.0,
           emi_total: float = 0.0, liquid_savings: Optional[float] = None,
           assets: Optional[float] = None, liabilities: Optional[float] = None) -> Dict[str, dict]:
    """Return indicators; any indicator lacking data has value None (UI shows 'Not provided')."""
    out: Dict[str, dict] = {}
    spend = None if essential is None else essential + discretionary + emi_total
    surplus = None if income is None or spend is None else income - spend
    out["surplus"] = dict(value=surplus, label="Monthly surplus / deficit",
        formula="Take-home income - (essential + discretionary + EMIs)",
        meaning="Positive means money is left each month; negative means spending exceeds income.",
        limits="Ignores irregular income, annual bills and cash not entered.")
    out["savings_rate"] = dict(value=None if surplus is None else _div(surplus, income or 0),
        label="Savings rate", formula="Surplus / take-home income (undefined when income is 0)",
        meaning="Share of income not spent. Can be negative.",
        limits="Says nothing about where the surplus goes or whether it is actually saved.")
    out["emergency_months"] = dict(value=None if liquid_savings is None or not essential else
        liquid_savings / (essential + emi_total), label="Emergency coverage (months)",
        formula="Liquid savings / (essential expenses + EMIs)",
        meaning="How many months of must-pay costs liquid savings could cover.",
        limits="Excludes market-linked or locked-in money; assumes expenses stay the same.")
    out["dti"] = dict(value=None if income is None else _div(emi_total, income),
        label="Debt-payment-to-income", formula="Monthly EMIs / take-home income",
        meaning="Share of income committed to loan payments.",
        limits="Does not reflect interest rates, remaining tenure or income stability.")
    nw = None if assets is None or liabilities is None else assets - liabilities
    out["net_worth"] = dict(value=nw, label="Estimated net worth", formula="Assets - liabilities (user-entered)",
        meaning="A snapshot of what you own minus what you owe.", limits="Values are your own estimates, not verified.")
    return out
