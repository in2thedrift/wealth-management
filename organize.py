"""Run this once in the folder that holds app.py (your repo root): python organize.py
It moves flat files into pages/, services/, components/, data/, utils/ and tests/, and restores dotfile names."""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
FOLDERS = {
    "services": ["budgeting", "calculators", "debt", "emergency_fund", "financial_health", "goals", "net_worth", "reporting", "retirement", "tax_estimation", "transaction_analysis"],
    "components": ["styling"],
    "data": ["content", "database", "repositories", "sample_data"],
    "utils": ["currency", "dates", "exports", "state", "validation"],
    "tests": ["test_calculators", "test_more"],
}
RENAMES = {"gitignore": ".gitignore", "env.example": ".env.example"}

moved = []
for old, new in RENAMES.items():
    if (ROOT / old).is_file() and not (ROOT / new).exists():
        (ROOT / old).rename(ROOT / new); moved.append(f"{old} -> {new}")
for f in ROOT.glob("*.py"):
    if re.match(r"^\d\d_.+\.py$", f.name):
        dest = "pages"
    else:
        dest = next((d for d, names in FOLDERS.items() if f.stem in names), None)
    if dest:
        (ROOT / dest).mkdir(exist_ok=True)
        shutil.move(str(f), str(ROOT / dest / f.name)); moved.append(f"{f.name} -> {dest}/")
print("\n".join(moved) or "Nothing to move.")
need = [f"services/{n}.py" for n in FOLDERS["services"]] + [f"pages/{p.name}" for p in []]
missing = [n for n in need if not (ROOT / n).is_file()]
print("\nStill missing:", missing or "nothing")
