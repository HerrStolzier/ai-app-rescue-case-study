# Final Handover

Root cause:

The app trusted a client-provided `user_id`. RLS expected the row owner to match the authenticated user, so the insert failed when the client sent `local_user`.

Files changed:

- SQL policy demo documented in `sql/after.sql`
- Verification added in `scripts/verify.mjs`

Verification performed:

- Confirmed the broken write fails the RLS ownership check.
- Confirmed the fixed write derives ownership from the session.
- Confirmed a different user cannot read the fixed row.

Remaining risks:

- This demo does not connect to a live Supabase project.
- A production fix should be validated against the actual policies, JWT claims, RPC functions, and client library calls.

Suggested next step:

- Add a small integration test around the real insert path before launch.
