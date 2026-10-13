"""Debt payoff simulation (fixed rates, monthly interest, same total budget every month)."""
from typing import Dict, List


def simulate_payoff(debts: List[dict], extra: float = 0.0, strategy: str = "avalanche", max_months: int = 1200) -> Dict:
    """debts: dicts with name, balance, rate (annual %), emi. Freed-up EMIs roll into remaining debts.
    strategy: 'avalanche' (highest rate first) or 'snowball' (smallest balance first)."""
    if extra < 0:
        raise ValueError("Extra payment cannot be negative.")
    ds = [dict(d) for d in debts if d["balance"] > 0]
    budget = sum(d["emi"] for d in ds) + extra
    interest_total, m = 0.0, 0
    while ds and m < max_months:
        m += 1
        for d in ds:
            i = d["balance"] * d["rate"] / 1200
            d["balance"] += i
            interest_total += i
        paid = 0.0
        for d in ds:
            p = min(d["emi"], d["balance"]); d["balance"] -= p; paid += p
        pool = budget - paid
        order = sorted(ds, key=(lambda d: -d["rate"]) if strategy == "avalanche" else (lambda d: d["balance"]))
        for d in order:
            p = min(pool, d["balance"]); d["balance"] -= p; pool -= p
        ds = [d for d in ds if d["balance"] > 0.005]
    return dict(months=m, interest=interest_total, cleared=not ds)
