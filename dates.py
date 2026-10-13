"""Indian financial-year helpers (FY runs 1 April to 31 March)."""
from datetime import date


def financial_year(d: date) -> str:
    start = d.year if d.month >= 4 else d.year - 1
    return f"{start}-{str(start + 1)[-2:]}"


def assessment_year(fy: str) -> str:
    start = int(fy[:4]) + 1
    return f"{start}-{str(start + 1)[-2:]}"


def is_overdue(due: date, today: date, done: bool) -> bool:
    return (not done) and due < today
