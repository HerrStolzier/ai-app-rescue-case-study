# Case Study D: AI-built App Hardening

This is a public demo case study. It is not client work and contains no private data.

## Failure

AI-generated app code often works in a chat preview but fails in a real build, test, or deployment environment.

Demo failure:

```text
The route initializes an AI provider at module import time.
If AI_API_KEY is missing during build/test, importing the module throws immediately.
```

That makes the app hard to verify and easy to break in CI or deployment.

## Diagnosis

The issue is not the provider itself. The app has unsafe runtime assumptions:

- secret required at import time,
- no input validation,
- raw provider error shape,
- no local demo mode.

## Fix

Move provider setup behind a lazy getter, validate input, and provide a safe local demo mode for verification.

Demo files:

- [before/route.mjs](before/route.mjs)
- [after/route.mjs](after/route.mjs)
- [verify.mjs](scripts/verify.mjs)

## Verification

Run:

```bash
npm run verify:ai
```

The verifier confirms:

- the before module fails at import without `AI_API_KEY`,
- the after module imports without secrets,
- invalid input returns a controlled `400`,
- valid input returns a deterministic demo response.

## Handover

See:

- [before.md](handover/before.md)
- [after.md](handover/after.md)
- [final-handover.md](handover/final-handover.md)
