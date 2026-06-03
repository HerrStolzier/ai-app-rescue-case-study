export async function GET() {
  return Response.json({
    ok: true,
    message: "This looks like a route handler, but App Router will not expose it here."
  });
}
