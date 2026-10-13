"""CSV validation and rule-based analysis of transactions. Findings are SUSPECTED patterns for user review."""
from typing import List, Tuple
import pandas as pd

REQUIRED = ["date", "description", "amount"]
MAX_ROWS = 5000
COLUMNS = ["date", "description", "amount", "type", "category", "payment_method"]
RULES = {"Food": ["swiggy", "zomato", "grocery", "bigbasket", "restaurant"], "Transport": ["uber", "ola", "metro", "fuel", "petrol"],
         "Utilities": ["electricity", "broadband", "recharge", "water", "gas"], "Subscriptions": ["netflix", "spotify", "prime", "hotstar", "youtube"],
         "Housing": ["rent", "maintenance"], "Health": ["pharmacy", "hospital", "clinic"], "EMI": ["emi", "loan"], "Insurance": ["premium", "insurance"]}


def categorize(description: str) -> str:
    d = str(description).lower()
    for cat, words in RULES.items():
        if any(w in d for w in words):
            return cat
    return "Uncategorised"


def clean_transactions(raw: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    """Validate an uploaded frame. Returns (valid rows, human-readable errors). Bad rows are rejected, never guessed."""
    raw = raw.rename(columns=lambda c: str(c).strip().lower())
    missing = [c for c in REQUIRED if c not in raw.columns]
    if missing:
        return pd.DataFrame(columns=COLUMNS), [f"Missing required column(s): {', '.join(missing)}."]
    if len(raw) > MAX_ROWS:
        return pd.DataFrame(columns=COLUMNS), [f"File has {len(raw)} rows; the limit is {MAX_ROWS}."]
    df, errors = raw.copy(), []
    df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["description"] = df["description"].astype(str).str.strip()
    bad = df["date"].isna() | df["amount"].isna() | (df["amount"] == 0) | df["description"].isin(["", "nan"])
    if "type" in df.columns:
        t = df["type"].astype(str).str.strip().str.title()
        bad |= ~t.isin(["Income", "Expense"])
        df["type"] = t
    else:
        df["type"] = df["amount"].apply(lambda a: "Income" if a > 0 else "Expense")
    errors += [f"Row {i + 2}: invalid date, amount, description or type." for i in df.index[bad]]
    df = df[~bad].copy()
    df["amount"] = df["amount"].abs()
    for col, default in [("category", None), ("payment_method", "Unknown")]:
        if col not in df.columns:
            df[col] = default
    df["category"] = df["category"].where(df["category"].notna() & (df["category"].astype(str) != ""), None)
    return df[COLUMNS].reset_index(drop=True), errors


def _expenses(df: pd.DataFrame) -> pd.DataFrame:
    e = df[df["type"] == "Expense"].copy()
    e["date"] = pd.to_datetime(e["date"])
    e["month"] = e["date"].dt.to_period("M").astype(str)
    e["key"] = e["description"].str.lower().str.replace(r"\d+", "", regex=True).str.strip()
    return e


def monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["month", "Income", "Expense", "Net"])
    d = df.copy(); d["month"] = pd.to_datetime(d["date"]).dt.to_period("M").astype(str)
    p = d.pivot_table(index="month", columns="type", values="amount", aggfunc="sum", fill_value=0).reset_index()
    for c in ("Income", "Expense"):
        if c not in p: p[c] = 0.0
    p["Net"] = p["Income"] - p["Expense"]
    return p[["month", "Income", "Expense", "Net"]]


def recurring(df: pd.DataFrame) -> pd.DataFrame:
    """Same description in 3+ months with amounts within 10% of each other (suspected recurring)."""
    e = _expenses(df)
    if e.empty: return pd.DataFrame(columns=["description", "months_seen", "monthly_amount", "annual_cost"])
    g = e.groupby("key")["amount"].agg(["mean", "std", "count"]).join(e.groupby("key")["month"].nunique().rename("months"))
    g = g[(g["months"] >= 3) & ((g["std"].fillna(0) / g["mean"]) <= 0.10)].reset_index()
    return pd.DataFrame({"description": g["key"], "months_seen": g["months"], "monthly_amount": g["mean"], "annual_cost": g["mean"] * 12})


def possible_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    e = _expenses(df)
    return e[e.duplicated(["date", "description", "amount"], keep=False)][["date", "description", "amount"]]


def unusually_large(df: pd.DataFrame) -> pd.DataFrame:
    e = _expenses(df)
    if len(e) < 5: return e.iloc[0:0][["date", "description", "amount"]]
    return e[e["amount"] > e["amount"].mean() + 2 * e["amount"].std()][["date", "description", "amount"]]


def repeated_small(df: pd.DataFrame, limit: float = 300, min_count: int = 5) -> pd.DataFrame:
    e = _expenses(df); e = e[e["amount"] <= limit]
    g = e.groupby(["month", "key"])["amount"].agg(["count", "sum"]).reset_index()
    return g[g["count"] >= min_count].rename(columns={"key": "description", "count": "times", "sum": "month_total"})
