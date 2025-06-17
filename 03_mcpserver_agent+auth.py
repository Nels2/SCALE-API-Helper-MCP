from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.models import APIKey, APIKeyIn, SecurityScheme
from scale_tools import get_tool_refs
from config_alt import MCP_BEARER_TOKEN

# === Auth setup
security = HTTPBearer(auto_error=False)

def verify_bearer_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != MCP_BEARER_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid bearer token")
    return credentials.credentials

# === FastAPI app with global Bearer Auth enforcement
app = FastAPI(
    title="scale-api-agent",
    version="1.5.1",
    description="SCALE API Proxy server secured with Bearer Auth.",
    dependencies=[Depends(verify_bearer_token)],
    swagger_ui_oauth2_redirect_url=None,
    openapi_tags=[
        {"name": "SCALE Session-Based Tools", "description": "Session management routes"},
        {"name": "SCALE API Explore", "description": "Query schema"},
        {"name": "SCALE API Prod. Interaction", "description": "Live proxy calls"}
    ]
)

# === Get registered tool functions
tool_refs = get_tool_refs()

# === Request models
class RunAPIRequest(BaseModel):
    query: str
    method: str
    body: dict | None = None  # Optional, for POST/PUT/other methods, this was completely missing lol

class QueryRequest(BaseModel):
    query: str

class EmptyBody(BaseModel):
    pass

# === Routes
@app.post("/run_api", tags=["SCALE API Prod. Interaction"])
async def run_api_route(body: RunAPIRequest):
    return await tool_refs["run_api"](query=body.query, method=body.method, body=body.body)

@app.post("/query_api", tags=["SCALE API Explore"])
async def query_api_route(body: QueryRequest):
    return await tool_refs["query_api"](query=body.query)

@app.post("/generate_session", tags=["SCALE Session-Based Tools"])
async def generate_session_route(_: EmptyBody):
    return await tool_refs["generate_session"]()

@app.post("/get_session", tags=["SCALE Session-Based Tools"])
async def get_session_route(_: EmptyBody):
    return await tool_refs["get_session"]()

@app.post("/kill_session", tags=["SCALE Session-Based Tools"])
async def kill_session_route(_: EmptyBody):
    return await tool_refs["kill_session"]()


