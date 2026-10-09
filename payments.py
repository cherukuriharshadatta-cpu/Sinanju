from __future__ import annotations

RETRIES_ENABLED = False


class FakePaymentGateway:
    """Tiny fake provider used only by the CodeGenius test repository."""

    def __init__(self) -> None:
        self.charges: list[dict] = []
        self._by_idempotency_key: dict[str, dict] = {}

    def charge(self, order_id: str, amount: int, *, idempotency_key: str | None = None) -> dict:
        if idempotency_key and idempotency_key in self._by_idempotency_key:
            return self._by_idempotency_key[idempotency_key]

        charge = {
            "charge_id": f"ch_{len(self.charges) + 1}",
            "order_id": order_id,
            "amount": amount,
            "idempotency_key": idempotency_key,
        }
        self.charges.append(charge)

        if idempotency_key:
            self._by_idempotency_key[idempotency_key] = charge
        return charge


def confirm_payment(
    gateway: FakePaymentGateway,
    order_id: str,
    amount: int,
    *,
    simulate_timeout: bool = False,
    force_retry: bool | None = None,
) -> dict:
    """Confirm a payment. Historical bug: every retry used a new request identity."""
    should_retry = RETRIES_ENABLED if force_retry is None else force_retry
    attempts = 2 if (simulate_timeout and should_retry) else 1
    result = None

    for attempt in range(attempts):
        # BUG: request identity changes every attempt.
        key = f"{order_id}:attempt:{attempt + 1}"
        result = gateway.charge(order_id, amount, idempotency_key=key)

        # Attempt 1 "times out" after the provider already created the charge.
        if simulate_timeout and attempt == 0 and should_retry:
            continue
        break

    assert result is not None
    return result
