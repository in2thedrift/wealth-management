"""Goal projection under user-chosen inflation and growth assumptions."""
from typing import Dict
from services import calculators as c


def project(cost_today: float, years: float, inflation_pct: float, existing: float,
            monthly: float, growth_pct: float) -> Dict[str, float]:
    if years <= 0:
        raise ValueError("Target date must be in the future (years > 0).")
    if min(cost_today, existing, monthly) < 0:
        raise ValueError("Amounts cannot be negative.")
    months = max(1, round(years * 12))
    future_cost = c.inflate(cost_today, inflation_pct, years)
    projected = c.lump_sum_fv(existing, growth_pct, months / 12) + c.sip_fv(monthly, growth_pct, months)
    return dict(future_cost=future_cost, projected=projected, gap=future_cost - projected,
                required_monthly=c.required_monthly(future_cost, existing, growth_pct, months), months=months)
