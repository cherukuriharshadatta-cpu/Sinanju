from __future__ import annotations

import json
from payments import FakePaymentGateway, confirm_payment

ORDER_ID = "ORDER-42"


def main() -> None:
    gateway = FakePaymentGateway()

    # force_retry=True intentionally probes the historical failure even on
    # revisions where the safety guard disables retries by default.
    confirm_payment(
        gateway,
        ORDER_ID,
        4999,
        simulate_timeout=True,
        force_retry=True,
    )

    count = len([c for c in gateway.charges if c["order_id"] == ORDER_ID])
    print(json.dumps({
        "order_id": ORDER_ID,
        "charge_count": count,
        "failure_signature": f"order={ORDER_ID};charges={count}",
    }))


if __name__ == "__main__":
    main()
