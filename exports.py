"""CSV / JSON export helpers."""
import json
import pandas as pd


def df_to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def session_to_json(tables: dict) -> bytes:
    return json.dumps({k: json.loads(v.to_json(orient="records", date_format="iso")) for k, v in tables.items()}, indent=2).encode()
