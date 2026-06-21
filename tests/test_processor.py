from workflow_sample.processor import process_order


def test_process_order_returns_status():
    result = process_order(
        {
            "id": "ord_1",
            "payload": "{}",
            "value": "101",
            "status": "pending",
            "data": {
                "attributes": {
                    "items": [
                        {"kind": "book", "quantity": 2, "price": 12, "region": "us"},
                    ]
                }
            },
        }
    )

    assert result["status"] == "review"

