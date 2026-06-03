# Final Handover

Root cause:

The app had a file that looked like an API handler, but it was not in the App Router route-handler location. Next.js did not expose `app/api/chat.js` as `/api/chat`, so the endpoint returned `404`.

Files changed:

- Added `app/api/chat/route.js`

Verification performed:

- Started the broken app and confirmed `GET /api/chat` returned `404`.
- Started the fixed app and confirmed `GET /api/chat` returned `200` with JSON.

Remaining risks:

- This demo does not include auth, rate limiting, or external provider calls.
- If this route later calls an AI provider, secrets should be added through the deployment environment, not committed.

Suggested next step:

- Add a small integration test for the route before connecting a real provider.
