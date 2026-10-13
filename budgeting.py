"""Budget summaries. Educational allocation examples never exceed available cash flow."""
from typing import Dict, List
from services.calculators import sip_fv


def summarize(income: float, expenses: Dict[str, float], savings_target: float = 0.0) -> Dict:
    if income < 0 or savings_target < 0 or any(v < 0 for v in expenses.values()):
        raise ValueError("Amounts cannot be negative.")
    total = sum(expenses.values())
    remaining = income - total
    return dict(total_expenses=total, remaining=remaining, overspend=remaining < 0,
                target_feasible=savings_target <= max(remaining, 0), max_feasible_saving=max(remaining, 0),
                annual_total=total * 12, annual_remaining=remaining * 12)


def example_budgets(income: float, obligations: float) -> List[Dict]:
    """Illustrative savings levels, capped by what is left after obligations."""
    free = max(income - obligations, 0.0)
    out = []
    for name, pct in [("Lean (10% of income)", 0.10), ("Balanced (20%)", 0.20), ("Ambitious (30%)", 0.30)]:
        save = min(pct * income, free)
        out.append(dict(scenario=name, savings=save, flexible_spending=free - save, capped=save < pct * income))
    return out


def extra_saving_effect(extra_monthly: float, annual_rate: float, years: int) -> Dict[str, float]:
    months = years * 12
    return dict(contributed=extra_monthly * months, estimated_value=sip_fv(extra_monthly, annual_rate, months))
