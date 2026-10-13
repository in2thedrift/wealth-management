"""Plain-text/markdown personal finance report."""
from datetime import date
from utils.currency import format_inr
from config import BRAND_NAME, DISCLOSURE


def build_report(profile: dict, indicators: dict, goals: list, tasks: list, notes: str, priorities: list) -> str:
    lines = [f"# {BRAND_NAME} personal finance report", f"Generated: {date.today().isoformat()}", "", "## Snapshot"]
    if not profile:
        lines.append("Not provided. Complete the Financial Health Passport.")
    for k, ind in indicators.items():
        v = ind["value"]
        lines.append(f"- {ind['label']}: " + ("Not provided" if v is None else (format_inr(v) if k in ("surplus", "net_worth") else f"{v:.2f}")))
    lines += ["", "## Top priorities"] + ([f"- {p}" for p in priorities] or ["- None selected"])
    lines += ["", "## Goals"] + ([f"- {g}" for g in goals] or ["- None recorded"])
    lines += ["", "## Open tasks"] + ([f"- {t}" for t in tasks] or ["- None"])
    lines += ["", "## Monthly review notes", notes or "None", "", "---", DISCLOSURE]
    return "\n".join(lines)
