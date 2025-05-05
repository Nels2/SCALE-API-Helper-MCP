from typing import Any
import httpx
import sqlite3
import json
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("scale-api-proxy")

# Function to make requests to API
async def make_request(url: str, method: str, headers: dict = None, data: dict = None, params: dict = None) -> dict[str, Any] | None:
    """Make a request to the API with proper error handling."""
    headers = headers or {}
    headers["User-Agent"] = USER_AGENT
    async with httpx.AsyncClient() as client:
        try:
            if method.lower() == "get":
                response = await client.get(url, headers=headers, params=params, timeout=30.0)
            elif method.lower() == "post":
                response = await client.post(url, headers=headers, json=data, timeout=30.0)
            elif method.lower() == "put":
                response = await client.put(url, headers=headers, json=data, timeout=30.0)
            elif method.lower() == "delete":
                response = await client.delete(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

# Function to search for the endpoint in the database
def search_endpoint(query: str):
    """Search for an API endpoint in the local schema database."""
    conn = sqlite3.connect("api_schema.db")
    cursor = conn.cursor()
    cursor.execute("SELECT path, method, description, request_body, responses FROM api_endpoints WHERE path LIKE ?", (f"%{query}%",))
    results = cursor.fetchall()
    conn.close()

    return [{"path": path, "method": method, "description": description,
             "request_body": json.loads(request_body) if request_body != "None" else None,
             "responses": json.loads(responses)} for path, method, description, request_body, responses in results]

@mcp.tool()
async def query_api(query: str) -> str:
    """Search the API schema for an endpoint.
    Args:
        query: The path or query to search for in the API schema.
    """
    # Search for the endpoint in the local schema database
    results = search_endpoint(query)

    if not results:
        return json.dumps({"error": "No matching endpoints found"})

    # Return all paths as available options
    available_paths = [{"path": endpoint_info["path"], "description": endpoint_info["description"], "method": endpoint_info["method"], "request_body": endpoint_info["request_body"], "response": endpoint_info["responses"]} for endpoint_info in results]
    return json.dumps({"available_paths": available_paths})


if __name__ == "__main__":
    # Run the MCP server on stdio transport
    mcp.run(transport='stdio')
    # command to run this mcp-server from terminal for use with open-webui: ` uvx mcpo --port 5086 -- uv run 03_mcpserver.py `
