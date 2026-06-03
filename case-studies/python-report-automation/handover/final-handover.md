# Final Handover

Root cause:

The reporting process had no repeatable command and no validation path. Manual spreadsheet handling made missing totals and unknown customers easy to miss.

Files changed:

- Added `src/report_automation.py`
- Added sample inputs under `inputs/`
- Added unit tests under `tests/`

Verification performed:

- Confirmed paid orders are aggregated per customer.
- Confirmed refunded orders are excluded.
- Confirmed invalid paid rows are counted.
- Confirmed unknown customers are retained as `Unknown customer`.
- Confirmed output CSV order and totals are stable.

Remaining risks:

- This demo reads local sample files only.
- A production workflow should add API retries, logging, and client-specific report formatting.

Suggested next step:

- Add the real source system as an adapter while keeping the same tested summary function.
