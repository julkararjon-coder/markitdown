import os
import subprocess
import time
import httpx
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse, RedirectResponse, Response
import uvicorn

INTERNAL_PORT = 3001
PUBLIC_PORT = int(os.environ.get("PORT", 10000))

# Start the real markitdown-mcp server internally
subprocess.Popen([
    "markitdown-mcp", "--http",
    "--host", "127.0.0.1",
    "--port", str(INTERNAL_PORT)
])
time.sleep(2)

async def oauth_metadata(request):
    base = str(request.base_url).rstrip("/")
    return JSONResponse({
        "issuer": base,
        "authorization_endpoint": base + "/authorize",
        "token_endpoint": base + "/token",
        "registration_endpoint": base + "/register",
        "response_types_supported": ["code"],
        "grant_types_supported": ["authorization_code"],
        "token_endpoint_auth_methods_supported": ["none"],
        "code_challenge_methods_supported": ["S256"],
    })

async def protected_resource(request):
    base = str(request.base_url).rstrip("/")
    return JSONResponse({"resource": base + "/mcp", "authorization_servers": [base]})

async def register(request):
    return JSONResponse({
        "client_id": "public-client",
        "client_id_issued_at": 0,
        "redirect_uris": ["https://claude.ai/api/mcp/auth_callback"],
        "token_endpoint_auth_method": "none",
    }, status_code=201)

async def authorize(request):
    params = dict(request.query_params)
    redirect_uri = params.get("redirect_uri", "")
    state = params.get("state", "")
    return RedirectResponse(url=f"{redirect_uri}?code=publiccode&state={state}")

async def token(request):
    return JSONResponse({"access_token": "public-token", "token_type": "bearer", "expires_in": 31536000})

async def proxy_mcp(request):
    url = f"http://127.0.0.1:{INTERNAL_PORT}/mcp/"
    body = await request.body()
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.request(
            request.method, url,
            content=body,
            headers={k: v for k, v in request.headers.items() if k.lower() != "host"},
        )
    return Response(content=resp.content, status_code=resp.status_code, headers=dict(resp.headers))

routes = [
    Route("/.well-known/oauth-authorization-server", oauth_metadata),
    Route("/.well-known/oauth-protected-resource", protected_resource),
    Route("/register", register, methods=["POST"]),
    Route("/authorize", authorize, methods=["GET"]),
    Route("/token", token, methods=["POST"]),
    Route("/mcp", proxy_mcp, methods=["GET", "POST"]),
]

app = Starlette(routes=routes)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PUBLIC_PORT)
