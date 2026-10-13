"""Net worth from user-entered records (estimates, not verified)."""
from datetime import date
import pandas as pd


def summarize(df: pd.DataFrame, today: date, stale_days: int = 180) -> dict:
    if df.empty:
        return dict(assets=0.0, liabilities=0.0, net_worth=None, by_category=pd.DataFrame(), stale=df)
    d = df.copy(); d["value"] = pd.to_numeric(d["value"], errors="coerce").fillna(0)
    assets = d.loc[d["kind"] == "Asset", "value"].sum(); liab = d.loc[d["kind"] == "Liability", "value"].sum()
    updated = pd.to_datetime(d["last_updated"], errors="coerce")
    stale = d[updated.isna() | ((pd.Timestamp(today) - updated).dt.days > stale_days)]
    return dict(assets=assets, liabilities=liab, net_worth=assets - liab, by_category=d.groupby(["kind", "category"])["value"].sum().reset_index(), stale=stale)
