# After

Change:

- Provider setup moved into a lazy getter.
- Missing secrets no longer break local verification.
- Empty prompt returns a controlled `400`.
- Valid prompt returns deterministic local demo output.

Verification:

- Before module fails at import as expected.
- After module imports without secrets.
- Invalid and valid request paths are tested.
