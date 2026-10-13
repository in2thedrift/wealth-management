"""Educational retirement projection. All values are estimates under user-chosen assumptions."""
from typing import Dict
from services import calculators as c


def project(age: int, retire_age: int, current: float, monthly: float, expenses_today: float, inflation: float,
            growth: float, post_retirement_return: float, retirement_years: int = 25, pension_today: float = 0.0) -> Dict[str, float]:
    """Corpus needed = present value at retirement of inflating monthly spending (net of pension, treated as
    today's money and inflated). Payments at month end; post-retirement return used as nominal return."""
    if retire_age <= age:
        raise ValueError("Retirement age must be greater than current age.")
    if min(current, monthly, expenses_today, pension_today) < 0 or retirement_years <= 0:
        raise ValueError("Amounts cannot be negative and retirement duration must be positive.")
    years = retire_age - age
    n = years * 12
    future_exp = c.inflate(expenses_today, inflation, years)
    future_pension = c.inflate(pension_today, inflation, years)
    need_monthly = max(future_exp - future_pension, 0.0)
    r_real = ((1 + post_retirement_return / 100) / (1 + inflation / 100)) ** (1 / 12) - 1
    m = retirement_years * 12
    annuity = m if abs(r_real) < 1e-12 else (1 - (1 + r_real) ** -m) / r_real
    corpus = need_monthly * annuity
    projected = c.lump_sum_fv(current, growth, years) + c.sip_fv(monthly, growth, n)
    return dict(years=years, future_monthly_expense=future_exp, corpus_needed=corpus, projected=projected,
                gap=corpus - projected, projected_real=c.real_value(projected, inflation, years),
                required_monthly=c.required_monthly(corpus, current, growth, n))
