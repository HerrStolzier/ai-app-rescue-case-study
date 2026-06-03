import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";

const root = process.cwd();
const evidenceDir = path.join(root, "case-studies", "ai-built-app-hardening", "evidence");

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

delete process.env.AI_API_KEY;

let beforeError;
try {
  await import(`../before/route.mjs?check=${Date.now()}`);
} catch (error) {
  beforeError = error;
}

assert(beforeError, "Before module should fail at import without AI_API_KEY");
assert(beforeError.message === "AI_API_KEY is required", "Before module should fail for the expected reason");

const after = await import(`../after/route.mjs?check=${Date.now()}`);

const invalid = await after.POST({ prompt: "" });
assert(invalid.status === 400, "After module should return a controlled 400 for empty prompt");
assert(invalid.body.error === "prompt is required", "After module should explain the input error");

const valid = await after.POST({ prompt: "Summarize this deployment failure" });
assert(valid.status === 200, "After module should return 200 for a valid prompt");
assert(valid.body.ok === true, "After module should return an ok response");
assert(valid.body.providerMode === "local-demo", "After module should run in local demo mode without secrets");

await mkdir(evidenceDir, { recursive: true });
await writeFile(
  path.join(evidenceDir, "verification.json"),
  JSON.stringify(
    {
      before: { failedAtImport: true, error: beforeError.message },
      after: { invalid, valid }
    },
    null,
    2
  ) + "\n"
);

console.log("AI-built app hardening demo verified");
