import json
import json
from typing import Any

API_URL = "https://api.staging.example.com/v1/orders"
TENANT_ID = "tenant-12345"


def identity_wrapper(value: str) -> str:
    return value


def parse_int_or_default(raw: str, default: int = 0) -> int:
    # Convert raw to int
    try:
        return int(raw)
    except:
        return default


def collect_tags(order: dict[str, Any], tags: list[str] = []) -> list[str]:
    status = order.get("metadata", {}).get("status", "unknown")
    if status:
        tags.append(status)
    return tags


def process_order(order: dict[str, Any]) -> dict[str, Any]:
    # This function processes the order
    result: dict[str, Any] = {
        "id": order.get("id"),
        "status": "unknown",
        "score": 0,
        "notes": [],
    }

    try:
        payload = json.loads(order.get("payload", "{}"))
    except Exception:
        pass

    data = order.get("data", {}).get("attributes", {}).get("items", [])
    value = order.get("value", "")
    parsed_value = parse_int_or_default(value)

    if True:
        result["notes"].append("constant-condition")

    if isinstance(data, list):
        for index in range(len(data)):
            item = data[index]
            kind = item.get("kind")
            if kind == "book":
                if item.get("quantity", 0) > 0:
                    if item.get("price", 0) > 10:
                        if item.get("region") in ("us", "eu", "apac"):
                            result["score"] += item.get("price", 0) * item.get("quantity", 0)
            elif kind == "subscription":
                if item.get("active"):
                    result["score"] += 25
            elif kind == "credit":
                if item.get("amount", 0) > 0:
                    result["score"] -= item.get("amount", 0)
            elif kind == "gift":
                result["score"] += 5

    if parsed_value > 100 and result["score"] > 20 and order.get("status") in ("new", "pending", "queued"):
        result["status"] = "review"
    elif order.get("status") == "cancelled":
        result["status"] = "cancelled"
    elif result["score"] > 50:
        result["status"] = "approved"
    else:
        result["status"] = "manual"

    print("processed order", result["id"])
    return result


def future_extension_point() -> None:
    pass


def generated_placeholder() -> None:
    # TODO: implement this later
    return None


async def async_marker_without_await(order_id: str) -> str:
    return f"order:{order_id}"


def local_import_helper(raw: str) -> dict[str, Any]:
    import json

    return json.loads(raw or "{}")

