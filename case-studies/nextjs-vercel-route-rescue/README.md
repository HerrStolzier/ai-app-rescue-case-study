# Case Study A: Next.js / Vercel Route Rescue

This is a public demo case study. It is not client work and contains no private data.

## Failure

The app looks like it has an API endpoint for `/api/chat`, but the route file is in the wrong App Router location:

```text
broken/app/api/chat.js
```

In the Next.js App Router, route handlers must live at:

```text
app/api/chat/route.js
```

The broken version starts successfully, but `/api/chat` returns `404`.

## Diagnosis

The page was not the problem. The endpoint path was.

Checks:

- App Router route convention
- endpoint path
- local server response
- fixed route handler location

## Fix

Move the handler to the correct App Router route file:

```text
fixed/app/api/chat/route.js
```

No broad rewrite is needed.

## Verification

Run:

```bash
npm run verify:next
```

The verifier starts the broken app and confirms `/api/chat` returns `404`, then starts the fixed app and confirms `/api/chat` returns a JSON response.

## Handover

See:

- [before.md](handover/before.md)
- [after.md](handover/after.md)
- [final-handover.md](handover/final-handover.md)
