import json


def _reject_json_constant(value):
    raise ValueError(f"Invalid JSON constant: {value}")


def summarize(text):
    totals = {}
    seen = set()
    for line in text.split("\n"):
        if not line.strip():
            continue
        row = json.loads(line, parse_constant=_reject_json_constant)
        if not isinstance(row, dict):
            raise ValueError("Each row must be a JSON object")
        row_id = row.get("id")
        category = row.get("category")
        amount = row.get("amount")
        if not isinstance(row_id, str) or not row_id.strip():
            raise ValueError("id must be a nonblank string")
        if not isinstance(category, str) or not category.strip():
            raise ValueError("category must be a nonblank string")
        if type(amount) is not int or amount < 0:
            raise ValueError("amount must be a nonnegative integer")
        if row_id in seen:
            continue
        seen.add(row_id)
        totals[category] = totals.get(category, 0) + amount
    return totals
