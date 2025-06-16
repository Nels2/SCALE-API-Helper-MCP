# scale_tools.py
import httpx
import subprocess
import pickle
import os
import time
import sqlite3
import json
from typing import Any
from mcp.server.fastmcp import FastMCP
from config_alt import *

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

mcp = FastMCP("scale-api-agent")



async def make_request(url: str, method: str, headers: dict = None, data: dict = None, params: dict = None) -> dict[str, Any] | None:
    headers = headers or {}
    headers["User-Agent"] = USER_AGENT
    async with httpx.AsyncClient(verify=False) as client:
        try:
            response = await getattr(client, method.lower())(url, headers=headers, json=data, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}


@mcp.tool()
async def run_api(query: str, method: str) -> str:
    scale_api_url = f"https://172.18.33.216/rest/v1{query}"
    api_headers = pickle.load(open("/Projects/api_scale/session/aisys_sessionLogin.p", "rb"))
    return await make_request(scale_api_url, method, headers=api_headers)


# Function to search for the endpoint in the database
def search_endpoint(query: str):
    """
    Searches for a matching API endpoint in the local SQLite database.

    Args:
        query (str): The query string to search for in the API schema's paths.

    Returns:
        list[Dict[str, Any]]: A list of endpoint data (paths, methods, descriptions, etc.) that match the query.
        
    Description:
        This function queries the local SCALE API database (sqlite) for API endpoints that match a given query string.
        It returns a structured list containing the path, HTTP method, description, request body, and response details
        for each endpoint that matches the query. Useful for dynamically finding relevant API documentation.
    """
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
    """
    Queries the local SCALE REST API schema for matching endpoints and returns them in JSON format.

    Args:
        query (str): The path or query to search for in the local API schema.

    Returns:
        str: A JSON string containing all matching API paths or an error message if no matches are found.
    
    Description:
        This function performs a local database search to find API endpoints based on the given query string.
        It formats the results into a structured JSON response, making it easy for external clients to access
        the available API paths, methods, and descriptions.
    """
    # Search for the endpoint in the local schema database
    results = search_endpoint(query)

    if not results:
        return json.dumps({"error": "No matching endpoints found"})

    # Return all paths as available options
    available_paths = [{"path": endpoint_info["path"], "description": endpoint_info["description"], "method": endpoint_info["method"], "request_body": endpoint_info["request_body"], "response": endpoint_info["responses"]} for endpoint_info in results]
    return json.dumps({"available_paths": available_paths})


@mcp.tool()
async def generate_session() -> str:
    try:
        result = subprocess.run(['python', '/Projects/api_scale/gen_sessionID.py'], capture_output=True, text=True)
        result.check_returncode()
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error generating session ID: {e}"


@mcp.tool()
async def get_session() -> str:
    try:
        SESSION_FILE = "/Projects/api_scale/session/aisys_sessionLogin.p"
        last_mod_time = os.path.getmtime(SESSION_FILE)
        age = int(time.time()) - last_mod_time
        cookie_header = pickle.load(open(SESSION_FILE, "rb")).get('Cookie', '')
        session_id = cookie_header[len('sessionID='):] if cookie_header.startswith('sessionID=') else ''
        return f"Found Valid Session: {session_id} | Age: {age} seconds" if age < 43200 else f"Session expired: {session_id}"
    except Exception as e:
        return f"Session check failed: {e}"


@mcp.tool()
async def kill_session() -> str:
    try:
        result = subprocess.run(['python', '/Projects/api_scale/kill_sessionID.py'], capture_output=True, text=True)
        result.check_returncode()
        return "Session killed."
    except subprocess.CalledProcessError as e:
        return f"Error killing session: {e}"



# Export real references so fastapi_server can call them
def get_tool_refs():
    return {
        "run_api": run_api,
        "query_api": query_api,
        "generate_session": generate_session,
        "get_session": get_session,
        "kill_session": kill_session
    }


# expose HTTP app -- if needed...
mcp_http_app = mcp.streamable_http_app()
