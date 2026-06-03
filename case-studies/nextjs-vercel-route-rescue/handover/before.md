# Before

Expected behavior:

- `GET /api/chat` returns a JSON response.

Actual behavior:

- The app starts.
- The page renders.
- `GET /api/chat` returns `404`.

Likely root cause:

- The handler exists as `app/api/chat.js`, but the Next.js App Router only exposes route handlers from `route.js` files inside a route segment folder.
