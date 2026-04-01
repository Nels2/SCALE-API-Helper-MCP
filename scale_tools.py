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

mcp = FastMCP("scale-api-proxy")


async def make_request(url: str, method: str, headers: dict = None, data: dict = None, params: dict = None) -> dict[str, Any] | None:
    headers = headers or {}
    headers["User-Agent"] = USER_AGENT
    async with httpx.AsyncClient(verify=False) as client:
        try:
            method_lower = method.lower()
            request_args = {"headers": headers, "timeout": 30.0}
            if method_lower in ["get", "delete", "head", "options"]:
                request_args["params"] = data or params
            else:
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


def _load_session_headers() -> dict:
    with open("/Projects/api_scale/session/aisys_sessionLogin.p", "rb") as f:
        return pickle.load(f)


def search_endpoint(query: str):
    conn = sqlite3.connect("api_schema.db")
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT path, method, description, request_body, responses FROM api_endpoints WHERE path LIKE ?",
            (f"%{query}%",)
        )
        results = cursor.fetchall()
    finally:
        conn.close()

    return [
        {
            "path": path,
            "method": method,
            "description": description,
            "request_body": json.loads(request_body) if request_body != "None" else None,
            "responses": json.loads(responses),
        }
        for path, method, description, request_body, responses in results
    ]


@mcp.tool()
async def run_api(query: str, method: str, payload: dict = None) -> str:
    host = "172.18.33.216"
    scale_api_url = f"https://{host}/rest/v1{query}"
    return await make_request(scale_api_url, method, headers=_load_session_headers(), data=payload)


@mcp.tool()
async def query_api(query: str) -> str:
    """
    Queries the local SCALE REST API schema for matching endpoints.
    """
    results = search_endpoint(query)
    if not results:
        return json.dumps({"error": "No matching endpoints found"})
    available_paths = [
        {
            "path": e["path"],
            "description": e["description"],
            "method": e["method"],
            "request_body": e["request_body"],
            "response": e["responses"],
        }
        for e in results
    ]
    return json.dumps({"available_paths": available_paths})


@mcp.tool()
async def fetch_vm(user: str = None, name: str = None) -> str:
    """
    Look up VMs by Name OR User via NMAPX Dash [WebAD].
    """
    if not user and not name:
        return json.dumps({"error": "Must provide either 'user' or 'name' parameter"})

    params = {"user": user} if user else {"name": name}
    async with httpx.AsyncClient(timeout=5.0, verify=False) as client:
        try:
            response = await client.get("http://172.18.33.140:444/api/symconsole?", params=params)
            response.raise_for_status()
            return response.text
        except httpx.HTTPError as e:
            return json.dumps({"error": f"Remote request failed: {str(e)}"})
        except Exception as e:
            return json.dumps({"error": f"Unexpected error: {str(e)}"})


@mcp.tool()
async def iso_read() -> str:
    """
    Retrieves a list of all ISOs from the SCALE API server.
    """
    host = "172.18.33.216"
    scale_api_url = f"https://{host}/rest/v1/ISO"
    return await make_request(scale_api_url, "GET", headers=_load_session_headers())

@mcp.tool()
async def drive_read() -> str:
    """
    Retrieves a list of all Physical Drives from the SCALE API server.
    """
    host = "172.18.33.216"
    scale_api_url = f"https://{host}/rest/v1/Drive"
    return await make_request(scale_api_url, "GET", headers=_load_session_headers())

@mcp.tool()
async def ping_read() -> str:
    """
    Retrieve a ping response from the SCALE API server to check connectivity and session validity.
    """
    host = "172.18.33.216"
    scale_api_url = f"https://{host}/rest/v1/ping"
    return await make_request(scale_api_url, "GET", headers=_load_session_headers())

@mcp.tool()
async def condition_read() -> str:
    """
    Retrieves a list of all active conditions from the SCALE API server.
    """
    host = "172.18.33.216"
    scale_api_url = f"https://{host}/rest/v1/Condition/filter?includeSet=true"
    return await make_request(scale_api_url, "GET", headers=_load_session_headers())

@mcp.tool()
async def clusterSpec_read() -> str:
    """
    Retrieves the current ClusterSpec record from the SCALE API server.
    """
    host = "172.18.33.216"
    scale_api_url = f"https://{host}/rest/v1/ClusterSpec"
    return await make_request(scale_api_url, "GET", headers=_load_session_headers())

@mcp.tool()
async def cluster_read() -> str:
    """
    Retrieves information about a given system (SCALE API Server)
    """
    host = "172.18.33.216"
    scale_api_url = f"https://{host}/rest/v1/Cluster"
    return await make_request(scale_api_url, "GET", headers=_load_session_headers())

@mcp.tool()
async def user_read() -> str:
    """
    Retrieves information about all users present in system (SCALE API Server)
    """
    host = "172.18.33.216"
    scale_api_url = f"https://{host}/rest/v1/User"
    return await make_request(scale_api_url, "GET", headers=_load_session_headers())

@mcp.tool()
async def virtualDisk_read() -> str:
    """
    Retrieves information about all users present in system (SCALE API Server)
    """
    host = "172.18.33.216"
    scale_api_url = f"https://{host}/rest/v1/VirtualDisk"
    return await make_request(scale_api_url, "GET", headers=_load_session_headers())


@mcp.tool()
async def taskTagStatus_read() -> str:
    """
    Retrieves information about all statuses (SCALE API Server)
    """
    host = "172.18.33.216"
    scale_api_url = f"https://{host}/rest/v1/TaskTag"
    return await make_request(scale_api_url, "GET", headers=_load_session_headers())

@mcp.tool()
async def vmNetDevices_read() -> str:
    """
    Retrieves list of all virtual network devices (SCALE API Server)
    """
    host = "172.18.33.216"
    scale_api_url = f"https://{host}/rest/v1/VirDomainNetDevice"
    return await make_request(scale_api_url, "GET", headers=_load_session_headers())

@mcp.tool()
async def vmSnapshots_read() -> str:
    """
    Retrieves list of all virtual network devices (SCALE API Server)
    """
    host = "172.18.33.216"
    scale_api_url = f"https://{host}/rest/v1/VirDomainSnapshot"
    return await make_request(scale_api_url, "GET", headers=_load_session_headers())



@mcp.tool()
async def taskTagStatusFilter(taskTag: str) -> str:
    """
    Retrieves information about all statuses, filteed by specific task (status) ID (SCALE API Server)
    """
    host = "172.18.33.216"
    scale_api_url = f"https://{host}/rest/v1/TaskTag/{taskTag}"
    method = "GET"
    return await make_request(scale_api_url, method, headers=_load_session_headers())

@mcp.tool()
async def getVM_details(vmUUID: str) -> str:
    """
    Retrieves information about a specific VM (SCALE API Server). Use fetch_vm to get VM UUIDs based on username or VM name.
    """
    host = "172.18.33.216"
    scale_api_url = f"https://{host}/rest/v1/VirDomain/{vmUUID}"
    method = "GET"
    return await make_request(scale_api_url, method, headers=_load_session_headers())

@mcp.tool()
async def getVM_sysStats(vmUUID: str) -> str:
    """
    Retrieves CPU, Memory, Disks and Network info about a specific VM (SCALE API Server). Use fetch_vm to get VM UUIDs based on username or VM name.
    """
    host = "172.18.33.216"
    scale_api_url = f"https://{host}/rest/v1/VirDomainStats/{vmUUID}"
    method = "GET"
    return await make_request(scale_api_url, method, headers=_load_session_headers())


@mcp.tool()
async def cloneVM(vmUUID: str) -> str:
    """
    Clones a specific VM (SCALE API Server). Use fetch_vm to get VM UUIDs based on username or VM name.
    """
    host = "172.18.33.216"
    scale_api_url = f"https://{host}/rest/v1/VirDomain/{vmUUID}/clone"
    method = "POST"
    return await make_request(scale_api_url, method, headers=_load_session_headers())

@mcp.tool()
async def exportVM(vmUUID: str) -> str:
    """
    Exports a specific VM (SCALE API Server) to the Archive Server. Use fetch_vm to get VM UUIDs based on username or VM name.
    """
    host = "172.18.33.216"
    scale_api_url = f"https://{host}/rest/v1/VirDomain/{vmUUID}/export"
    method = "POST"
    payload = {
        "target": {
            "pathURI": f"{smbConnectionStuff}",
            "compress": True,
            "allowNonSequentialWrites": True,
            "parallelCountPerTransfer": 4
        }
        }
    return await make_request(scale_api_url, method, headers=_load_session_headers(), data=payload)

@mcp.tool()
async def changeVM_state(vmUUID: str, actionType: str) -> str:
    """
    Take action on a specific VM (SCALE API Server) - actionType can be one of: "START", "SHUTDOWN", "STOP", "PAUSE", "REBOOT", "RESET", "LIVEMIGRATE", "NMI"
    Use fetch_vm to get VM UUIDs based on username or VM name.
    """
    host = "172.18.33.216"
    scale_api_url = f"https://{host}/rest/v1/VirDomain/action"
    method = "POST"
    payload = [
        {
            "virDomainUUID": f"{vmUUID}",
            "actionType": f"{actionType}",
        }
    ]
    return await make_request(scale_api_url, method, headers=_load_session_headers(), data=payload)

@mcp.tool()
async def snapshotVM(vmUUID: str, label: str) -> str:
    """
    Snapshots a specific VM (SCALE API Server) in real-time. Use fetch_vm to get VM UUIDs based on username or VM name.
    """
    host = "172.18.33.216"
    scale_api_url = f"https://{host}/rest/v1/VirDomainSnapshot"
    method = "POST"
    payload = {
        "domainUUID": f"{vmUUID}",
        "label": f"{label}",
        "type": "USER",
        "blockCountDiffFromSerialNumber": -1,
        "replication": False,
    }
    return await make_request(scale_api_url, method, headers=_load_session_headers(), data=payload)

@mcp.tool()
async def delete_snapshotVM(SnapUUID: str) -> str:
    """
    Deletes a specific snapshot from a singular VM (SCALE API Server) in real-time. Use vmSnapshots_read to get snapshot UUIDs based on VM UUID.
    """
    host = "172.18.33.216"
    scale_api_url = f"https://{host}/rest/v1/VirDomainSnapshot/{SnapUUID}"
    method = "DELETE"
    return await make_request(scale_api_url, method, headers=_load_session_headers())















@mcp.tool()
async def generate_session() -> str:
    """
    Runs gen_sessionID.py to generate a new session ID.
    """
    try:
        result = subprocess.run(
            ['/Projects/api_scale/vfx/bin/python', '/Projects/api_scale/gen_sessionID.py'],
            capture_output=True, text=True
        )
        result.check_returncode()
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error generating session ID:\n{e.stderr or 'No stderr'}\n\nstdout:\n{e.stdout}"


@mcp.tool()
async def get_session() -> str:
    """
    Validates the current session based on a 12-hour window.
    """
    try:
        SESSION_FILE = "/Projects/api_scale/session/aisys_sessionLogin.p"
        age = int(time.time()) - os.path.getmtime(SESSION_FILE)
        with open(SESSION_FILE, "rb") as f:
            cookie_header = pickle.load(f).get('Cookie', '')
        session_id = cookie_header[len('sessionID='):] if cookie_header.startswith('sessionID=') else ''
        if age < 43200:
            return f"Found Valid Session: {session_id} | Age: {age} seconds"
        return f"Session expired: {session_id}"
    except Exception as e:
        return f"Session check failed: {e}"


@mcp.tool()
async def kill_session() -> str:
    """
    Terminates the current session.
    """
    try:
        result = subprocess.run(
            ['/Projects/api_scale/vfx/bin/python', '/Projects/api_scale/kill_sessionID.py'],
            capture_output=True, text=True
        )
        result.check_returncode()
        return "Session killed."
    except subprocess.CalledProcessError as e:
        return f"Error killing session: {e}"


mcp_http_app = mcp.streamable_http_app()
