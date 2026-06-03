let cachedClient;

function getAiClient() {
  if (!cachedClient) {
    const apiKey = process.env.AI_API_KEY;
    cachedClient = apiKey
      ? { mode: "external-ai", keyPrefix: apiKey.slice(0, 4) }
      : { mode: "local-demo", keyPrefix: "demo" };
  }

  return cachedClient;
}

export async function POST(requestBody) {
  if (!requestBody || typeof requestBody.prompt !== "string" || requestBody.prompt.trim() === "") {
    return {
      status: 400,
      body: {
        ok: false,
        error: "prompt is required"
      }
    };
  }

  const client = getAiClient();

  return {
    status: 200,
    body: {
      ok: true,
      providerMode: client.mode,
      output: `Demo answer for: ${requestBody.prompt.trim()}`
    }
  };
}
