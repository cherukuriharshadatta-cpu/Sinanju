# Current dependencies on confirmation retry behavior

Known repository-level dependencies:

- `payments.py` currently defaults `RETRIES_ENABLED = False`.
- `confirm_payment()` now persists one idempotency identity per logical order.
- The provider in this repository is a fake test double.
- Production traffic, real provider behavior, multi-region consistency, and
  deployment configuration are outside this repository's evidence boundary.

CodeGenius should scan this file and the current code before claiming that the
historical guard can be reconsidered.
