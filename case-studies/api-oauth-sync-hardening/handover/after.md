# After

Change:

- Added a small OAuth-protected API sync demo.
- Added token refresh before API reads.
- Added stable `job_id` upsert behavior.
- Added gross-profit calculation and CSV output.
- Added tests for refresh, idempotency, and missing refresh-token failure.

Verification:

- `python3 -m unittest discover -s case-studies/api-oauth-sync-hardening/tests`
- `npm run verify:api-sync`
