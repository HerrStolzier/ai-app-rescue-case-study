# Before

Expected behavior:

- A scheduled sync should refresh OAuth tokens before API calls.
- Re-running the sync should update existing rows instead of duplicating them.
- Output should be a stable CSV that can be checked by a non-technical user.

Actual behavior:

- Expired-token handling is easy to leave implicit.
- Repeated API pulls can append duplicates.
- Credential boundaries are often unclear in handover notes.
