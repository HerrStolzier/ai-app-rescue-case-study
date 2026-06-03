import { spawn } from "node:child_process";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";

const root = process.cwd();
const nextBin = path.join(root, "node_modules", ".bin", "next");
const evidenceDir = path.join(root, "case-studies", "nextjs-vercel-route-rescue", "evidence");

async function runCommand(command, args) {
  const child = spawn(command, args, {
    cwd: root,
    stdio: ["ignore", "pipe", "pipe"]
  });

  let output = "";
  child.stdout.on("data", (chunk) => {
    output += chunk.toString();
  });
  child.stderr.on("data", (chunk) => {
    output += chunk.toString();
  });

  const exitCode = await new Promise((resolve) => child.once("exit", resolve));
  if (exitCode !== 0) {
    throw new Error(`${command} ${args.join(" ")} failed with ${exitCode}\n${output}`);
  }
  return output;
}

async function waitFor(url, timeoutMs = 30000) {
  const startedAt = Date.now();
  let lastError;

  while (Date.now() - startedAt < timeoutMs) {
    try {
      const response = await fetch(url);
      return response;
    } catch (error) {
      lastError = error;
      await new Promise((resolve) => setTimeout(resolve, 500));
    }
  }

  throw lastError || new Error(`Timed out waiting for ${url}`);
}

async function withNextDev(appDir, port, fn) {
  const child = spawn(nextBin, ["dev", appDir, "-p", String(port), "--hostname", "127.0.0.1"], {
    cwd: root,
    stdio: ["ignore", "pipe", "pipe"]
  });

  let logs = "";
  child.stdout.on("data", (chunk) => {
    logs += chunk.toString();
  });
  child.stderr.on("data", (chunk) => {
    logs += chunk.toString();
  });

  try {
    await waitFor(`http://127.0.0.1:${port}/`);
    return await fn({ logs });
  } finally {
    child.kill("SIGTERM");
    await new Promise((resolve) => child.once("exit", resolve));
  }
}

await mkdir(evidenceDir, { recursive: true });

const fixedBuildOutput = await runCommand(nextBin, [
  "build",
  "case-studies/nextjs-vercel-route-rescue/fixed"
]);

const brokenResult = await withNextDev("case-studies/nextjs-vercel-route-rescue/broken", 4311, async () => {
  const response = await fetch("http://127.0.0.1:4311/api/chat");
  const body = await response.text();
  if (response.status !== 404) {
    throw new Error(`Expected broken route to return 404, got ${response.status}: ${body}`);
  }
  return { status: response.status, body };
});

const fixedResult = await withNextDev("case-studies/nextjs-vercel-route-rescue/fixed", 4312, async () => {
  const response = await fetch("http://127.0.0.1:4312/api/chat");
  const body = await response.json();
  if (response.status !== 200 || body.ok !== true) {
    throw new Error(`Expected fixed route to return ok JSON, got ${response.status}: ${JSON.stringify(body)}`);
  }
  return { status: response.status, body };
});

await writeFile(
  path.join(evidenceDir, "verification.json"),
  JSON.stringify({ fixedBuildOutput, brokenResult, fixedResult }, null, 2) + "\n"
);

console.log("Next.js/Vercel route rescue verified");
