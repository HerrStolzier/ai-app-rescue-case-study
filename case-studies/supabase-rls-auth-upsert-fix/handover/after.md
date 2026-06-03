# After

Change:

- The row owner is derived from the authenticated session.
- RLS remains strict: users can insert and read only their own rows.

Verification:

- Broken insert is rejected.
- Fixed insert is accepted.
- Owner can read the row.
- Another user cannot read the row.
