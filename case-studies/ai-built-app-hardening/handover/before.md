# Before

Expected behavior:

- The app can be imported, tested, and built without live provider secrets.
- Runtime requests validate input and return predictable errors.

Actual behavior:

- Importing the route throws if `AI_API_KEY` is missing.
- Tests and builds can fail before a request is handled.
- Empty prompts are not validated.
