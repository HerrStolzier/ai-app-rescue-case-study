# Before

Expected behavior:

- A signed-in user creates a report.
- The report is saved and visible only to that user.

Actual behavior:

- The client sends a local owner value.
- The database policy expects the authenticated user id.
- The write is rejected or the row would be owned by the wrong identity.

Root cause:

- Client identity and database ownership are mixed.
