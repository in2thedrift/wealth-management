"""Pure, testable financial formulas. No rounding here; round only for display.
Conventions: rates are annual percentages; interest compounds monthly; payments at month end.
Floats are used for projections (estimates); amounts shown to users are rounded at display time."""
from typing import Dict, List, Optional
from utils.validation import require_non_negative


def monthly_rate(annual_pct: float) -> float:
    return annual_pct / 1200.0


def emi(principal: float, annual_rate: float, months: int) -> float:
    """Standard EMI = P*r*(1+r)^n / ((1+r)^n - 1); zero rate -> P/n."""
    require_non_negative(principal=principal, annual_rate=annual_rate)
    if months <= 0:
        raise ValueError("Tenure must be at least 1 month.")
    if principal == 0:
        return 0.0
    r = monthly_rate(annual_rate)
    if r == 0:
        return principal / months
    g = (1 + r) ** months
    return principal * r * g / (g - 1)


def amortization_schedule(principal: float, annual_rate: float, months: int) -> List[Dict[str, float]]:
    """Month-by-month schedule: payment, interest, principal, balance."""
    pay, bal, r, rows = emi(principal, annual_rate, months), principal, monthly_rate(annual_rate), []
    for m in range(1, months + 1):
        interest = bal * r
        princ = pay - interest
        bal = max(bal - princ, 0.0) if m < months else 0.0
        rows.append({"month": m, "payment": pay, "interest": interest, "principal": princ, "balance": bal})
    return rows


def inflate(amount: float, inflation_pct: float, years: float) -> float:
    """Future cost = amount * (1+i)^years."""
    require_non_negative(amount=amount, years=years)
    return amount * (1 + inflation_pct / 100) ** years


def real_value(future_amount: float, inflation_pct: float, years: float) -> float:
    """Today's purchasing power of a future nominal amount."""
    return future_amount / (1 + inflation_pct / 100) ** years


def lump_sum_fv(principal: float, annual_rate: float, years: float) -> float:
    """Compound growth, monthly compounding."""
    require_non_negative(principal=principal, years=years)
    return principal * (1 + monthly_rate(annual_rate)) ** (years * 12)


def simple_interest(principal: float, annual_rate: float, years: float) -> float:
    require_non_negative(principal=principal, annual_rate=annual_rate, years=years)
    return principal * annual_rate / 100 * years


def sip_fv(monthly: float, annual_rate: float, months: int) -> float:
    """Future value of end-of-month contributions; zero rate handled separately."""
    require_non_negative(monthly=monthly)
    r = monthly_rate(annual_rate)
    if months <= 0:
        return 0.0
    return monthly * months if r == 0 else monthly * (((1 + r) ** months - 1) / r)


def required_monthly(target: float, current: float, annual_rate: float, months: int) -> float:
    """Monthly amount needed so current savings plus contributions reach target."""
    if months <= 0:
        raise ValueError("Time horizon must be at least 1 month.")
    need = target - lump_sum_fv(current, annual_rate, months / 12)
    if need <= 0:
        return 0.0
    unit = sip_fv(1.0, annual_rate, months)
    return need / unit


def project_series(current: float, monthly: float, annual_rate: float, months: int) -> List[float]:
    """Balance at the end of each month (for charts)."""
    r, bal, out = monthly_rate(annual_rate), current, []
    for _ in range(months):
        bal = bal * (1 + r) + monthly
        out.append(bal)
    return out


def fd_maturity(principal: float, annual_rate: float, years: float, compounds_per_year: int = 4) -> float:
    """Fixed deposit maturity; quarterly compounding by default (check your bank's actual rule)."""
    require_non_negative(principal=principal, annual_rate=annual_rate, years=years)
    return principal * (1 + annual_rate / 100 / compounds_per_year) ** (compounds_per_year * years)


def rd_maturity(monthly: float, annual_rate: float, months: int) -> float:
    """Recurring deposit estimate: deposit at start of each month, quarterly compounding."""
    require_non_negative(monthly=monthly, annual_rate=annual_rate)
    return sum(monthly * (1 + annual_rate / 400) ** (4 * (months - k) / 12) for k in range(months))
