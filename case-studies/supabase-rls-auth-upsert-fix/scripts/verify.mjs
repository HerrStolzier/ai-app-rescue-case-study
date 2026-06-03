import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";

const root = process.cwd();
const evidenceDir = path.join(root, "case-studies", "supabase-rls-auth-upsert-fix", "evidence");

const reports = [];

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

function canInsert(row, session) {
  return row.user_id === session.userId;
}

function canRead(row, session) {
  return row.user_id === session.userId;
}

function brokenInsert(payload, session) {
  const row = {
    id: "report_before",
    user_id: payload.user_id ?? "local_user",
    report_text: payload.report_text
  };

  if (!canInsert(row, session)) {
    return { ok: false, reason: "RLS_WITH_CHECK_FAILED", row };
  }

  reports.push(row);
  return { ok: true, row };
}

function fixedInsert(payload, session) {
  const row = {
    id: "report_after",
    user_id: session.userId,
    report_text: payload.report_text
  };

  if (!canInsert(row, session)) {
    return { ok: false, reason: "RLS_WITH_CHECK_FAILED", row };
  }

  reports.push(row);
  return { ok: true, row };
}

const ownerSession = { userId: "user_123" };
const otherSession = { userId: "user_999" };

const broken = brokenInsert(
  { user_id: "local_user", report_text: "North gate checked" },
  ownerSession
);

assert(broken.ok === false, "Broken insert should be rejected by RLS");
assert(broken.reason === "RLS_WITH_CHECK_FAILED", "Broken insert should fail for the expected reason");

const fixed = fixedInsert(
  { user_id: "local_user", report_text: "North gate checked" },
  ownerSession
);

assert(fixed.ok === true, "Fixed insert should be accepted");
assert(fixed.row.user_id === ownerSession.userId, "Fixed row should be owned by the authenticated user");
assert(canRead(fixed.row, ownerSession) === true, "Owner should be able to read the fixed row");
assert(canRead(fixed.row, otherSession) === false, "Another user should not be able to read the fixed row");

await mkdir(evidenceDir, { recursive: true });
await writeFile(
  path.join(evidenceDir, "verification.json"),
  JSON.stringify({ broken, fixed, ownerCanRead: true, otherCanRead: false }, null, 2) + "\n"
);

console.log("Supabase RLS/auth/upsert demo verified");
