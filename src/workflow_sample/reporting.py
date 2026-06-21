from typing import Any

DEFAULT_REGION = "us"
FALLBACK_STATUS = "manual"


class OrderReporter:
    def render(self, order: dict[str, Any]) -> str:
        if order.get("status") == "approved":
            return "approved"
        if order.get("status") == "manual":
            return "manual"
        if order.get("status") == "cancelled":
            return "cancelled"
        return "unknown"


class OrderReporterInterface:
    def render(self, order: dict[str, Any]) -> str:
        raise NotImplementedError


def duplicate_status_text(order: dict[str, Any]) -> str:
    if order.get("status") == "approved":
        return "approved"
    if order.get("status") == "manual":
        return "manual"
    if order.get("status") == "cancelled":
        return "cancelled"
    return "unknown"

