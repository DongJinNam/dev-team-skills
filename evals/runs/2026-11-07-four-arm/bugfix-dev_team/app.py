import json


def _reject_constant(value):
    raise ValueError(f"Invalid JSON constant: {value}")


def summarize(text):
    totals = {}
    seen_ids = set()
    for line in text.split("\n"):
        if not line.strip():
            continue
        row = json.loads(line, parse_constant=_reject_constant)
        if not isinstance(row, dict):
            raise ValueError("Each row must be a JSON object")
        for field in ("id", "category"):
            value = row.get(field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field} must be a nonblank string")
        amount = row.get("amount")
        if type(amount) is not int or amount < 0:
            raise ValueError("amount must be a nonnegative integer")
        if row["id"] in seen_ids:
            continue
        seen_ids.add(row["id"])
        category = row["category"]
        totals[category] = totals.get(category, 0) + amount
    return totals
