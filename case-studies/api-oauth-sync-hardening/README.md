# Case Study E: OAuth API Sync Hardening

This is a public demo case study. It is not client work and contains no private data, secrets, customer systems, or paid API keys.

## Failure

Small SaaS integrations often look simple until the scheduled sync meets real API behavior:

- access tokens expire during a cron run,
- refresh tokens are not handled before the API call,
- repeated syncs duplicate rows,
- gross-profit or report calculations are not stable,
- there is no safe handover explaining credential boundaries.

## Diagnosis

The workflow needs a tested sync boundary:

- refresh an expired token before touching the API,
- fail early if a refresh token is missing,
- normalize API rows,
- upsert by stable external IDs,
- write a repeatable CSV output.

## Fix

The demo script uses an in-memory token store and fake API/OAuth clients. That keeps the proof inspectable without external services or credentials.

Run:

```bash
python3 case-studies/api-oauth-sync-hardening/src/api_oauth_sync.py \
  --output case-studies/api-oauth-sync-hardening/outputs/generated-jobs.csv
```

## Verification

Run:

```bash
npm run verify:api-sync
```

The tests verify:

- an expired access token is refreshed before the API call,
- the API receives the refreshed token,
- generated CSV output is stable,
- repeated syncs update rows without duplicates,
- a missing refresh token fails before any API call.

## Handover

See:

- [before.md](handover/before.md)
- [after.md](handover/after.md)
- [final-handover.md](handover/final-handover.md)
