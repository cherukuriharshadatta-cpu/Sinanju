# ADR-001 — Persist one idempotency identity across confirmation retries

Status: accepted

The historical duplicate-charge incident was possible because each confirmation
retry used a different request identity.

The payment confirmation path now derives one idempotency key from the logical
order ID and reuses that same key on every attempt.

This change is intended to mitigate the historical duplicate-charge mechanism.
It does **not** certify that automatic retries are production-safe under every
provider, load condition, or multi-region deployment.
