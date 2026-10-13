"""Session-state tables. Session state is per-visitor and temporary, not secure storage."""
import pandas as pd
import streamlit as st

TABLE_KEYS = ["txns", "salary_budget", "money_map", "policies", "tasks", "household_goals", "household_members", "obligations"]


def get_table(key: str, schema: dict, rows=None) -> pd.DataFrame:
    """Return a DataFrame stored in session; create it with typed columns on first use."""
    if key not in st.session_state:
        df = pd.DataFrame({c: pd.Series(dtype=t) for c, t in schema.items()})
        if rows:
            df = pd.concat([df, pd.DataFrame(rows)], ignore_index=True).astype(schema)
        st.session_state[key] = df
    return st.session_state[key]
