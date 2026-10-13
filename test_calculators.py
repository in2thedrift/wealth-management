import pytest
from services import calculators as c
from services.debt import simulate_payoff
from services.emergency_fund import plan
from services.goals import project
from services.financial_health import assess
from utils.currency import format_inr

def test_emi_known():           assert c.emi(1_000_000, 9, 120) == pytest.approx(12667.58, abs=0.01)
def test_emi_zero_rate():       assert c.emi(120000, 0, 12) == 10000
def test_emi_zero_principal():  assert c.emi(0, 9, 12) == 0
def test_emi_bad_tenure():
    with pytest.raises(ValueError): c.emi(1000, 5, 0)
def test_emi_negative():
    with pytest.raises(ValueError): c.emi(-1, 5, 12)
def test_amortization_ends_at_zero():
    s = c.amortization_schedule(500000, 10, 60); assert s[-1]["balance"] == 0 and len(s) == 60
def test_amortization_interest_total():
    s = c.amortization_schedule(100000, 12, 12); assert sum(r["interest"] for r in s) == pytest.approx(c.emi(100000, 12, 12) * 12 - 100000)
def test_inflate():             assert c.inflate(100, 10, 2) == pytest.approx(121)
def test_real_value_inverse():  assert c.real_value(c.inflate(100, 6, 5), 6, 5) == pytest.approx(100)
def test_sip_zero_rate():       assert c.sip_fv(1000, 0, 12) == 12000
def test_sip_known():           assert c.sip_fv(1000, 12, 12) == pytest.approx(12682.50, abs=0.01)
def test_required_monthly_roundtrip():
    need = c.required_monthly(1_000_000, 50000, 8, 120)
    assert c.lump_sum_fv(50000, 8, 10) + c.sip_fv(need, 8, 120) == pytest.approx(1_000_000)
def test_required_monthly_already_met(): assert c.required_monthly(1000, 5000, 8, 12) == 0
def test_emergency_zero_expenses(): assert plan(0, 1000, 6, 100)["coverage"] is None
def test_emergency_achieved():  assert plan(1000, 9000, 6, 100)["shortfall"] == 0
def test_emergency_no_contribution(): assert plan(1000, 0, 6, 0)["months_to_target"] is None
def test_goal_past_date():
    with pytest.raises(ValueError): project(1000, -1, 6, 0, 0, 8)
def test_goal_zero_growth():
    r = project(100000, 5, 0, 0, 1000, 0); assert r["projected"] == 60000 and r["gap"] == 40000
def test_debt_avalanche_not_worse():
    d = [dict(name="a", balance=100000, rate=10, emi=3000), dict(name="b", balance=20000, rate=36, emi=1000)]
    assert simulate_payoff(d, 2000, "avalanche")["interest"] <= simulate_payoff(d, 2000, "snowball")["interest"]
def test_debt_extra_saves_interest():
    d = [dict(name="a", balance=100000, rate=10, emi=3000)]
    assert simulate_payoff(d, 1000)["interest"] < simulate_payoff(d, 0)["interest"]
def test_debt_zero_principal(): assert simulate_payoff([dict(name="a", balance=0, rate=5, emi=100)])["months"] == 0
def test_health_zero_income():
    r = assess(0, 1000, 0, 0, 5000); assert r["savings_rate"]["value"] is None and r["dti"]["value"] is None
def test_health_missing_data():
    r = assess(None, None); assert r["surplus"]["value"] is None and r["net_worth"]["value"] is None
def test_health_deficit():       assert assess(10000, 8000, 3000)["surplus"]["value"] == -1000
def test_inr_format():
    assert format_inr(1234567) == "\u20b912,34,567" and format_inr(999) == "\u20b9999" and format_inr(None) == "Not provided"
    assert format_inr(-100000) == "-\u20b91,00,000" and format_inr(10**10) == "\u20b910,00,00,00,000"
