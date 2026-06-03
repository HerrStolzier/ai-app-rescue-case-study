# Case Study B: Supabase RLS / Auth / Upsert Fix

This is a public demo case study. It is not client work and contains no private data.

## Failure

A user action appears valid in the UI, but the data write does not land correctly.

Common pattern:

```text
The client sends user_id = "local_user" or no authenticated owner.
RLS expects auth.uid() = user_id.
The insert is rejected or the row is owned incorrectly.
```

## Diagnosis

The bug is not "Supabase is broken." The app mixes local client identity with database ownership.

Checks:

- what owner is sent by the client
- what owner RLS expects
- whether the insert uses `auth.uid()`
- whether another user can read the row

## Fix

Do not trust the client-provided owner. Map ownership from the authenticated session and keep the RLS policy strict.

Demo files:

- [before.sql](sql/before.sql)
- [after.sql](sql/after.sql)
- [verify.mjs](scripts/verify.mjs)

## Verification

Run:

```bash
npm run verify:supabase
```

The verifier confirms:

- the broken insert is denied because the owner is wrong,
- the fixed insert is owned by the authenticated user,
- another user cannot read the fixed row.

## Boundary

The verifier is a small policy/session simulator, not a Supabase emulator. The SQL files show the intended database-side shape; the script proves the specific failure mechanics without requiring a live Supabase project or real data.

## Handover

See:

- [before.md](handover/before.md)
- [after.md](handover/after.md)
- [final-handover.md](handover/final-handover.md)
