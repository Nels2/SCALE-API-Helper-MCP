from typing import Any
import httpx
import sqlite3
import json
from mcp.server.fastmcp import FastMCP
import requests
from config_alt import *
print(xcred)

# Initialize FastMCP server
mcp = FastMCP("scale-api-runner")
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Function to make requests to API
async def make_request(url: str, method: str, headers: dict = None, data: dict = None, params: dict = None) -> dict[str, Any] | None:
    """
    Makes an HTTP request to a specified SCALE API endpoint, handles errors, and returns the response.
    
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

@mcp.tool()
async def run_api(query: str, method: str) -> str:
    """
    RUN API, or run_api Forwards the query to the external SCALE REST API using the provided method and authorization token.
    
    Args:
        query (str): The path or query to search for in the external SCALE API.
        method (str): The HTTP method to use (GET, POST, PUT, DELETE, etc.).
    
    Returns:
        str: The JSON string of the API response or an error message if the request fails.
    
    Description:
        This function forwards the provided query and method to the external API, adds the necessary
        authentication token to the request headers, and handles the request asynchronously.
        It also handles response formatting and error handling to return a clean response.
    """
    # Prepare headers and data for the request
    
    # Host and URL setup
    host = "172.18.33.215/rest/v1"
    scale_api_url = f"https://{host}{query}"  # The query can be used as the API path here

    # Prepare headers and data for the request
    credentials = f"Basic {xcred}"
    headers = {"Authorization": credentials, "Content-Type": "application/json", "Connection": "keep-alive"}
    data = None  # This would depend on your API's request body
    params = None  # Query parameters, if any

    # Forward the request to the external API and return the response
    response = await make_request(f"{scale_api_url}", method, headers=headers, data=data, params=params)
    return response


if __name__ == "__main__":
    # Run the MCP server on stdio transport
    mcp.run(transport='stdio')
    # command to run this mcp-server from terminal for use with open-webui: ` uvx mcpo --port 5085 -- uv run 03_mcpserver.py `
