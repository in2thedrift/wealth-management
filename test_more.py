import pandas as pd, pytest
from datetime import date
from services import budgeting as b, transaction_analysis as ta, retirement as rt, tax_estimation as tx, net_worth as nw, calculators as c
from utils.dates import financial_year, assessment_year, is_overdue

def test_budget_overspend():
    s = b.summarize(10000, {"a": 12000}, 500); assert s["overspend"] and not s["target_feasible"] and s["max_feasible_saving"] == 0
def test_budget_zero_income(): assert b.summarize(0, {}, 0)["remaining"] == 0
def test_budget_negative():
    with pytest.raises(ValueError): b.summarize(-1, {})
def test_examples_never_exceed_free():
    for e in b.example_budgets(50000, 48000): assert e["savings"] <= 2000
def test_extra_saving_zero_rate(): assert b.extra_saving_effect(100, 0, 1)["estimated_value"] == 1200

def test_csv_missing_columns():
    d, e = ta.clean_transactions(pd.DataFrame({"foo": [1]})); assert d.empty and "Missing" in e[0]
def test_csv_rejects_bad_rows():
    raw = pd.DataFrame({"date": ["01/01/2025", "bad", "02/01/2025"], "description": ["Rent", "x", ""], "amount": [-5000, 10, 20]})
    d, e = ta.clean_transactions(raw); assert len(d) == 1 and len(e) == 2 and d.iloc[0]["amount"] == 5000 and d.iloc[0]["type"] == "Expense"
def test_csv_row_limit():
    d, e = ta.clean_transactions(pd.DataFrame({"date": ["01/01/2025"] * 5001, "description": ["a"] * 5001, "amount": [1] * 5001})); assert d.empty and e
def _tx(rows): return pd.DataFrame(rows, columns=["date", "description", "amount", "type", "category", "payment_method"]).assign(date=lambda d: pd.to_datetime(d["date"]))
def test_recurring_detected():
    t = _tx([(f"2025-0{m}-05", "Netflix", 649, "Expense", None, "UPI") for m in (1, 2, 3)]); r = ta.recurring(t)
    assert len(r) == 1 and r.iloc[0]["annual_cost"] == pytest.approx(649 * 12)
def test_recurring_not_for_two_months():
    assert ta.recurring(_tx([(f"2025-0{m}-05", "Gym", 500, "Expense", None, "UPI") for m in (1, 2)])).empty
def test_duplicates():
    assert len(ta.possible_duplicates(_tx([("2025-01-01", "Shop", 99, "Expense", None, "UPI")] * 2))) == 2
def test_empty_frames():
    e = _tx([]); assert ta.recurring(e).empty and ta.monthly_summary(e).empty and ta.unusually_large(e).empty
def test_categorize(): assert ta.categorize("Swiggy order") == "Food" and ta.categorize("zzz") == "Uncategorised"

def test_retirement_past_age():
    with pytest.raises(ValueError): rt.project(60, 55, 0, 0, 1000, 6, 8, 7)
def test_retirement_zero_inflation_zero_return():
    r = rt.project(30, 40, 0, 0, 1000, 0, 0, 0, 10); assert r["corpus_needed"] == pytest.approx(1000 * 120)
def test_retirement_pension_covers_all():
    assert rt.project(30, 60, 0, 0, 1000, 6, 8, 7, 25, 2000)["corpus_needed"] == 0
def test_retirement_real_less_than_nominal():
    r = rt.project(30, 60, 100000, 10000, 40000, 6, 9, 7); assert r["projected_real"] < r["projected"]

def test_tax_slabs():
    s = [(400000, 0), (800000, 5), (None, 10)]; assert tx.slab_tax(1000000, s) == pytest.approx(20000 + 20000)
def test_tax_zero_and_negative():
    assert tx.slab_tax(0, [(None, 10)]) == 0
    with pytest.raises(ValueError): tx.slab_tax(-1, [(None, 10)])
def test_tax_rebate_and_cess():
    r = tx.total_tax(700000, [(300000, 0), (None, 10)], 4, 700000, 40000); assert r["total"] == 0
    r2 = tx.total_tax(1000000, [(None, 10)], 4); assert r2["total"] == pytest.approx(104000)

def test_net_worth():
    df = pd.DataFrame({"kind": ["Asset", "Liability"], "category": ["Gold", "Loan"], "value": [100.0, 40.0], "last_updated": [pd.Timestamp("2025-01-01")] * 2})
    s = nw.summarize(df, date(2025, 1, 10)); assert s["net_worth"] == 60 and s["stale"].empty
def test_net_worth_empty(): assert nw.summarize(pd.DataFrame(), date.today())["net_worth"] is None

def test_fy():
    assert financial_year(date(2025, 3, 31)) == "2024-25" and financial_year(date(2025, 4, 1)) == "2025-26" and assessment_year("2025-26") == "2026-27"
def test_overdue(): assert is_overdue(date(2025, 1, 1), date(2025, 2, 1), False) and not is_overdue(date(2025, 1, 1), date(2025, 2, 1), True)
def test_fd_rd():
    assert c.fd_maturity(1000, 0, 5) == 1000 and c.rd_maturity(100, 0, 12) == pytest.approx(1200)
