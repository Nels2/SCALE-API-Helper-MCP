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
    """
    Makes an HTTP request to a specified SCALE Rest API endpoint, handles errors, and returns the response.
    
    Args:
        url (str): The URL of the API endpoint.
        method (str): The HTTP method to be used for the request (GET, POST, PUT, DELETE, etc.).
        headers (Optional[Dict[str, str]]): A dictionary containing headers like Authorization.
        data (Optional[Dict[str, Any]]): The request body data for POST, PUT, or PATCH methods.
        params (Optional[Dict[str, Any]]): Query parameters for GET requests.

    Returns:
        Optional[Dict[str, Any]]: The parsed JSON response from the API, or an error message if the request fails.
    
    Description:
        This function makes asynchronous API requests using the `httpx` library. It supports common HTTP
        methods (GET, POST, PUT, DELETE) and includes error handling for both network issues and HTTP errors.
        It raises exceptions for non-2xx HTTP responses and provides detailed error messages for debugging.
    """
    headers = headers or {}
    headers["User-Agent"] = USER_AGENT
    async with httpx.AsyncClient(verify=False) as client:
        try:
            method_lower = method.lower()
            request_args = {"headers": headers, "timeout": 30.0}

            if method_lower in ["get", "delete", "head", "options"]:
                # For methods that do not send JSON body, use params for query parameters
                request_args["params"] = data or params
            else:
                # For methods that can send a JSON body
                request_args["json"] = data
                if params:
                    request_args["params"] = params

            response = await getattr(client, method_lower)(url, **request_args)
            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            return {"error": str(e), "details": e.response.text}
        except Exception as e:
            return {"error": str(e)}

@mcp.tool()
async def run_api(query: str, method: str, payload: dict = None) -> str:
    host = "172.18.33.216"
    scale_api_url = f"https://{host}/rest/v1{query}"
    api_headers = pickle.load(open("/Projects/api_scale/session/aisys_sessionLogin.p", "rb"))
    return await make_request(scale_api_url, method, headers=api_headers, data=payload)


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
    """
    Executes gen_sessionID.py script to generate a new session ID, which is needed to make a request to the API.
    """
    try:
        result = subprocess.run(
            ['/Projects/api_scale/vfx/bin/python', '/Projects/api_scale/gen_sessionID.py'], 
            capture_output=True, 
            text=True
        )
        result.check_returncode()
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error generating session ID:\n{e.stderr or 'No stderr'}\n\nstdout:\n{e.stdout}"


@mcp.tool()
async def get_session() -> str:
    """
    Executes get_sessionID.py script to find the current ID, then validates based on a 12 hour time frame..
    """
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
    """
    Executes kill_sessionID.py script to terminates the connection, use generate_session() to get a new session going..
    """
    try:
        result = subprocess.run(['/Projects/api_scale/vfx/bin/python', '/Projects/api_scale/kill_sessionID.py'], capture_output=True, text=True)
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
