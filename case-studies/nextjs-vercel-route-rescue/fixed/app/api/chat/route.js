export async function GET() {
  return Response.json({
    ok: true,
    message: "The App Router route is exposed from app/api/chat/route.js."
  });
}
