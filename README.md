# SCALE API Helper + MCP (LLM-Aided Exploration)

This project offers a secure, interactive bridge between a local LLM environment and the SCALE Computing HyperCore REST API. It enables querying endpoints, managing session-based authentication, and performing live API actions through a token-secured FastAPI + MCP integration.

Originally developed to understand and experiment with the SCALE API, this evolved into a fully functional developer tool with OpenWebUI, Claude Desktop, or cURL support.


I've included scripts 01-02, the full API schema as `scale_api_full_schema.json`, and api_schema.db to show how I set this up and how it works.

Keep in mind that this is definitely no where near perfect. I'll work on this more in the future!

## Features

- **FastAPI Server** (`fastapi_server.py`) for exposing routes.
- **Tool Implementation** (`scale_tools.py`) for SCALE session lifecycle + query forwarding.
- **Bearer Auth** integration for secure access.
- **RAG Compatibility** with LLMs through MCP protocol.
- **Swagger UI (/docs)** with full OpenAPI support.

## File Overview

| File                            | Purpose                                               |
| ------------------------------- | ----------------------------------------------------- |
| `03_mcpserver_agent+auth.py`    | Exposes HTTP routes and secures them with bearer auth |
| `scale_tools.py`                | Defines tools: run\_api, query\_api, session ops      |
| `03_mcpserver_agent_no-auth.py` | [DEPRECATED] Raw MCP without auth                     |
| `03_mcpserver_helper.py`        | [DEPRECATED] Helper for exploring the API             |

---


## Requirements
- Python 3.10+
- [Ollama](https://ollama.com/) running reachable by you at an openai http/https endpoint. (optional)
- MCP runtime (e.g. via `uvx mcpo`)
- Tools: `fastapi`, `httpx`, `pydantic`, `uvicorn`

I personally used qwen3 at 0.6b, 1.7b, and 4b along with llama-3.2-3b-instruct from **unsloth**.

MCP runtime (e.g. via uvx mcpo)

Tools: fastapi, httpx, pydantic, uvicorn

## Setup Instructions

### 1. Clone & Install

```bash
git clone https://github.com/Nels2/SCALE-API-Helper
cd scale-api-agent
uv pip install -r requirements.txt
```

### 2. Configure

Edit `config_alt.py` with your actual token:

```python
MCP_BEARER_TOKEN = "your-secret-token"
```

### 3. Run the Server

```bash
uvicorn fastapi_server:app --host 0.0.0.0 --port 5075
```

Then visit: [http://localhost:5075/docs](http://localhost:5075/docs)

## MCP Usage (for OpenWebUI)

### Launch as MCP HTTP Tool

```bash
uvx mcpo --port 5075 -- uv run fastapi_server.py
```

Make sure OpenWebUI has this connection added:

```
URL: http://<your-ip>:5075/openapi.json
Auth: Bearer <your-token>
```

---

## Available Tools

- `run_api(query: str, method: str)`
- `query_api(query: str)`
- `generate_session()`
- `get_session()`
- `kill_session()`

All tools use dynamic session-based authentication against the SCALE cluster, with the session stored and validated from a local `.p` file.


## Example RAG output via python
Question Example 0, Straight Path: 
``` 
Ask a question about the API: /User
```
Answer:
```
mistral:7b's Response:
  Based on the API schema you provided, I can identify the following actions related to the "User" resource:

1. `POST /User` -- Creates a new user by sending a request with required details (such as username, email, password, etc.) inside the request body.
2. `GET /User` -- Retrieves a list of all users available in the system.
3. `GET /User/{uuid}` -- Retrieves information about a specific user, identified by a unique UUID (Universally Unique Identifier).
4. Both `POST /User/{uuid}` and `PATCH /User/{uuid}` are intended to edit/update user information. However, they differ in the manner they modify the data:
   - `POST /User/{uuid}` -- Creates a new user with an updated UUID, replacing any existing user with the same UUID.
   - `PATCH /User/{uuid}` -- Updates the existing record for that specific user identified by the provided UUID without replacing it.
5. `DELETE /User/{uuid}` -- Deletes a specific user identified by the provided UUID from the system.
```

Question Example 1, Straight Path 2:
```
Ask a question about the API: /virDomain
```
Answer:
```
mistral:7b's Response:
 1. To get a list of VMs, you can use GET method at either `/VirDomain` or `/VirDomain/{virDomainUUID}` endpoint if you have a specific UUID.
2. Create a new VM requires POST request to `/VirDomain`
3. Editing a VM can be done in three ways:
   - Using PUT method at `/VirDomain/{virDomainUUID}` (you might need to update the whole VM information)
   - Using PATCH method at `/VirDomain/{virDomainUUID}` (you can update specific fields)
4. To delete a VM, use DELETE method at `/VirDomain/{virDomainUUID}` endpoint.
5. Creating a new _VirDomainBlockDevice_ requires POST request to `/VirDomainBlockDevice` or `/VirDomainBlockDevice/{uuid}` if you have a specific UUID for editing the existing one.
6. Editing an existing _VirDomainBlockDevice_ can be done in three ways:
   - Using PUT method at `/VirDomainBlockDevice/{uuid}` (you might need to update the whole _VirDomainBlockDevice_ information)
   - Using PATCH method at `/VirDomainBlockDevice/{uuid}` (you can update specific fields)
7. Deleting an existing _VirDomainBlockDevice_ requires DELETE request to `/VirDomainBlockDevice/{uuid}` endpoint.
8. Creating and attaching a new virtual network device for the VM needs POST method at `/VirDomainNetDevice/{virDomainUUID}`. Make sure that the VM is shutoff before adding a network device.
9. Retrieve all virtual network devices with GET request to `/VirDomainNetDevice`. Get or edit specific virtual network device by using get(`GET /VirDomainNetDevice/{uuid}`) and editing operations (POST, PATCH, DELETE) by having the UUID. Make sure that the VM is shutoff before modifying a network device or deleting it using `/VirDomainNetDevice/{uuid}` endpoint.
10. Creating and initiating a VM Replication to a remote system can be done using POST method at `/VirDomainReplication`. You can edit an existing replication by having the UUID, and available editing operations are POST, PATCH, and DELETE as before. Check the documentation for specific parameters or formats related to this API for more details.
11. Capturing a persistent copy of a VM state requires using POST method at `/VirDomainSnapshot`. To get a list of VM snapshots use GET request to `/VirDomainSnapshot` or check a specific snapshot by having the UUID and using GET at `/VirDomainSnapshot/{uuid}`. Delete a snapshot with DELETE method at `/VirDomainSnapshot/{uuid}` endpoint.
12. Create an automated VM Snapshot Schedule and edit/manage it by using POST, PATCH, DELETE methods on respective endpoints:
   - `POST /VirDomainSnapshotSchedule` to create a schedule
   - `GET /VirDomainSnapshotSchedule/{uuid}` to get the list of schedules
   - `PATCH /VirDomainSnapshotSchedule/{uuid}` and `DELETE /VirDomainSnapshotSchedule/{uuid}` to edit or remove a snapshot schedule.
13. Retrieve stats for a VM by using GET request at either `/VirDomainStats` (retrieves all info) or `/VirDomainStats/{virDomainUUID}` (retrieves specific VM's stats).
14. You can export, import and clone VMs by using POST operations:
   - Export a VM: POST `/VirDomain/{virDomainUUID}/export`
   - Import a VM: POST `/VirDomain/import`
   - Clone a VM from snapshot: POST `/VirDomain/{virDomainUUID}/clone`
```



# Final Notes
## Architecture Overview

- `fastapi_server.py`: Handles route definitions, security, OpenAPI schema, and MCP tool forwarding.
- `scale_tools.py`: Implements all logic for SCALE API interaction.
- Tools are registered via `mcp.tool()` and referenced in `get_tool_refs()` for flexible use.

## Dev Notes

- Inspired by usage of `mistral:7b` with basic RAG. Although mistral seems to be more dated model nowadays..
- Can be extended to use structured OpenAPI schema in memory for smarter retrieval.
- Tested against **SCALE HyperCore v9.4.30.217736**


## License

MIT. Use and adapt freely.
