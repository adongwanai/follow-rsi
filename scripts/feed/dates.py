"""Public daily sections use source dates, never ingestion timestamps."""


def daily_section(item, date, retrospective=False):
    """Classify a paper using verified HF list membership and source dates."""
    if retrospective:
        return "historical"
    if item.get("window_status") in ("backlog", "stale", "already_published"):
        return "historical"
    if item.get("window_status") == "in_window":
        return "hf_today" if item.get("news_date") in item.get("hf_daily_dates", []) else "other_today"
    if date in item.get("hf_daily_dates", []):
        return "hf_today"
    if any(str(item.get(field) or "")[:10] == date for field in ("published", "updated")):
        return "other_today"
    return "historical"
