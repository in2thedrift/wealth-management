"""Input validation helpers."""


def require_non_negative(**values: float) -> None:
    """Raise ValueError naming the first negative or non-finite field."""
    for name, v in values.items():
        if v is None or v != v or v in (float("inf"), float("-inf")):
            raise ValueError(f"{name} must be a valid number.")
        if v < 0:
            raise ValueError(f"{name} cannot be negative.")
