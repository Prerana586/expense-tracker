from collections import defaultdict

def summarize(expenses: list) -> dict:
    total = sum(e["amount"] for e in expenses)
    by_category = defaultdict(float)
    by_month    = defaultdict(float)

    for e in expenses:
        by_category[e["category"]] += e["amount"]
        month = e["date"][:7]
        by_month[month] += e["amount"]

    top_cat = max(by_category, key=by_category.get, default="none")

    return {
        "total_spent":   round(total, 2),
        "by_category":   {k: round(v, 2) for k, v in by_category.items()},
        "by_month":      {k: round(v, 2) for k, v in sorted(by_month.items())},
        "top_category":  top_cat,
        "expense_count": len(expenses),
    }

def alert_overspend(summary: dict, budget: float = 2000.0) -> str:
    if summary["total_spent"] > budget:
        over = summary["total_spent"] - budget
        return f"⚠️  Over budget by ${over:.2f} (budget: ${budget:.2f})"
    return None