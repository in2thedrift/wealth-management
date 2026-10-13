"""Emergency-fund calculations."""
import math
from typing import Dict, Optional


def plan(essential_monthly: float, current: float, target_months: int, monthly_contribution: float) -> Dict[str, Optional[float]]:
    if essential_monthly < 0 or current < 0 or monthly_contribution < 0 or target_months <= 0:
        raise ValueError("Enter non-negative amounts and a target of at least 1 month.")
    target = essential_monthly * target_months
    shortfall = max(target - current, 0.0)
    months_needed = 0 if shortfall == 0 else (None if monthly_contribution == 0 else math.ceil(shortfall / monthly_contribution))
    coverage = None if essential_monthly == 0 else current / essential_monthly
    return dict(target=target, coverage=coverage, shortfall=shortfall, months_to_target=months_needed)


def scenario_runway(current: float, essential_monthly: float, income_drop_pct: float = 100.0,
                    current_income: float = 0.0) -> Optional[float]:
    """Months savings last if income falls by income_drop_pct and essentials continue."""
    gap = essential_monthly - current_income * (1 - income_drop_pct / 100)
    return None if gap <= 0 else current / gap
