const apiKey = process.env.AI_API_KEY;

if (!apiKey) {
  throw new Error("AI_API_KEY is required");
}

export async function POST(requestBody) {
  return {
    status: 200,
    body: {
      output: `Generated answer for ${requestBody.prompt}`,
      provider: "external-ai"
    }
  };
}
