# SCALE API Helper + MCP

A secure, LLM-ready bridge between your local AI environment and the SCALE Computing HyperCore REST API. Exposes VM management operations as authenticated FastAPI routes and MCP tools — usable from OpenWebUI, Claude Desktop, or cURL.

Built to go beyond API exploration: this is a functional operator tool for taking real actions against a SCALE HyperCore cluster.

> Tested against **SCALE HyperCore v9.4.30.217736** & **v9.6.19.223352**

---

## Features

- **FastAPI proxy server** with Bearer Auth securing all routes
- **MCP tool integration** for OpenWebUI and Claude Desktop
- **Session-based auth** against SCALE HyperCore (stored locally in `.p` file)
- **VM lifecycle management**: snapshot, clone, export, state changes
- **Swagger UI** at `/docs` with full OpenAPI schema
- **RAG-compatible** schema querying for LLM-assisted API exploration

---

## File Overview

| File | Purpose |
|---|---|
| `03_mcpserver_agent+auth.py` | Route definitions, Bearer auth, OpenAPI schema, MCP forwarding |
| `scale_tools.py` | All SCALE API logic: session lifecycle, VM operations, query forwarding |
| `models.py` | Pydantic models for use with Swagger UI |
| `config_alt.py` | Bearer token and cluster host configuration |
| `scale_api_full_schema.json` | Full HyperCore OpenAPI schema (used for RAG/exploration) |
| `api_schema.db` | SQLite schema store for LLM-aided endpoint discovery |
| `01_*.py` / `02_*.py` / `03_flaskapi.py` / `03_llmRAG.py` | Setup and exploration scripts |

---

## Requirements

- Python 3.10+
- MCP runtime via `uvx mcpo`
- Dependencies: `fastapi`, `httpx`, `pydantic`, `uvicorn`
- any OpenAI API Compat. Server — tested with `nvidia/NVIDIA-Nemotron-3-Nano-4B-FP8` on vLLM (0.18.1)

---

## Setup

### 1. Clone & Install

```bash
git clone https://github.com/Nels2/SCALE-API-Helper-MCP
cd SCALE-API-Helper-MCP
uv pip install -r requirements.txt
```

### 2. Configure

Edit `config_alt.py`:

```python
MCP_BEARER_TOKEN = "your-secret-token"
SCALE_HOST = "your-cluster-ip"
```

### 3. Run

```bash
uvx mcpo --port 5075 -- uvicorn 03_mcpserver_agent+auth:app --host 0.0.0.0 --port 5075
```

Optionally, add --reload if you plan to make changes and dont wan't to kill the server.

Swagger UI: [http://localhost:5075/docs](http://localhost:5075/docs)

---

## MCP Usage

### OpenWebUI

```bash
uvx mcpo --port 5075 -- uv run fastapi_server.py
```

Add connection in OpenWebUI:
```
URL:  http://<your-ip>:5075/openapi.json
Auth: Bearer <your-token>
```

> **Note:** After adding new tools to the MCP server, restart the server process and reconnect in OpenWebUI — tool lists are cached at connection time.

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "scale-agent": {
      "url": "http://<your-ip>:5075",
      "headers": {
        "Authorization": "Bearer <your-token>"
      }
    }
  }
}
```

---

## Available Tools
 
### Session Management
| Tool | Description |
|---|---|
| `generate_session` | Authenticate against SCALE and store session |
| `get_session` | Retrieve current session info (validates 12hr window) |
| `kill_session` | Invalidate active session |
 
### Read Operations
| Tool | Description |
|---|---|
| `ping_read` | Check connectivity and session validity |
| `cluster_read` | Retrieve cluster node information |
| `clusterSpec_read` | Retrieve cluster spec/configuration |
| `condition_read` | List all active conditions/alerts |
| `user_read` | List all users on the system |
| `iso_read` | List all ISOs |
| `drive_read` | List all physical drives |
| `virtualDisk_read` | List all virtual disks |
| `vmNetDevices_read` | List all virtual network devices |
| `vmSnapshots_read` | List all VM snapshots |
| `taskTagStatus_read` | List all task/status tags |
| `taskTagStatusFilter` | Get status for a specific task tag by ID |
 
### VM Operations
| Tool | Description |
|---|---|
| `fetch_vm` | Search VMs by name or user (via NMAPX Dash) |
| `getVM_details` | Fetch full VM configuration by UUID |
| `getVM_sysStats` | Retrieve live CPU, memory, disk, and network stats |
| `changeVM_state` | Take action on a VM: `START`, `SHUTDOWN`, `STOP`, `PAUSE`, `REBOOT`, `RESET`, `LIVEMIGRATE`, `NMI` |
| `snapshotVM` | Take a named snapshot of a VM |
| `delete_snapshotVM` | Delete a snapshot by UUID |
| `cloneVM` | Clone a VM |
| `exportVM` | Export a VM to the configured SMB archive target |
 
### Raw Access
| Tool | Description |
|---|---|
| `run_api` | Direct proxy call — any endpoint, method, and payload |
| `query_api` | Search the local schema DB for matching endpoints |
 
---

## Architecture

```
OpenWebUI / Claude Desktop
        │
        ▼
  fastapi_server.py  ←── Bearer Auth
        │
        ▼
  scale_tools.py  ←── Session (.p file)
        │
        ▼
  SCALE HyperCore REST API
```

---

## Notes

- This is a personal developer tool but it IS technically production-hardened since it is secured by Bearer Auth.
- The SCALE API uses session cookies, not per-request tokens; the `.p` file persists this between calls, it is only valid based on the SCALE Permissions, but the script sets a hard time of 12 hours to auto refresh token.
- `run_api` gives you a raw escape hatch for any endpoint not yet wrapped as a named tool... but your model has to be smart enough to handle embedded JSON within JSON.

---

## License

MIT. Use and adapt freely.
