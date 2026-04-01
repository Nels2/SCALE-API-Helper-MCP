from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config_alt import MCP_BEARER_TOKEN
from models import RunAPIRequest, QueryRequest, EmptyBody, VMQuery, VMChangeStateQuery, VMSnapshotQuery, VMSnapshotDeleteQuery, VMDetailsQuery, TaskTagStatusFilterRequest
from scale_tools import run_api, query_api, fetch_vm, iso_read, vmSnapshots_read, virtualDisk_read, getVM_sysStats, snapshotVM, drive_read, ping_read, delete_snapshotVM, condition_read, vmNetDevices_read, user_read, clusterSpec_read, cluster_read, taskTagStatus_read, taskTagStatusFilter, getVM_details, cloneVM, exportVM, changeVM_state, generate_session, get_session, kill_session

security = HTTPBearer(auto_error=False)

def verify_bearer_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials or credentials.credentials != MCP_BEARER_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid bearer token")
    return credentials.credentials

app = FastAPI(
    title="scale-api-agent",
    version="1.5.4",
    description="SCALE API Proxy server secured with Bearer Auth.",
    dependencies=[Depends(verify_bearer_token)],
    openapi_tags=[
        {"name": "SCALE Session-Based Tools", "description": "Session management routes"},
        {"name": "SCALE API Explore", "description": "Query schema"},
        {"name": "SCALE API Prod. Interaction", "description": "Live proxy calls"},
    ]
)

@app.post("/run_api", tags=["SCALE API Prod. Interaction"])
async def run_api_route(body: RunAPIRequest):
    return await run_api(query=body.query, method=body.method, payload=body.payload)

@app.post("/query_api", tags=["SCALE API Explore"])
async def query_api_route(body: QueryRequest):
    return await query_api(query=body.query)

@app.post("/fetch_vm", tags=["SCALE API Explore"])
async def fetch_vm_route(body: VMQuery = Body(...)):
    return await fetch_vm(user=body.user, name=body.name)

@app.post("/iso_read", tags=["SCALE API Prod. Reading Actions"])
async def iso_read_route():
    return await iso_read()

@app.post("/drive_read", tags=["SCALE API Prod. Reading Actions"])
async def drive_read_route():
    return await drive_read()

@app.post("/ping_read", tags=["SCALE API Prod. Reading Actions"])
async def ping_read_route():
    return await ping_read()

@app.post("/condition_read", tags=["SCALE API Prod. Reading Actions"])
async def condition_read_route():
    return await condition_read()

@app.post("/clusterSpec_read", tags=["SCALE API Prod. Reading Actions"])
async def clusterSpec_read_route():
    return await clusterSpec_read()

@app.post("/cluster_read", tags=["SCALE API Prod. Reading Actions"])
async def cluster_read_route():
    return await cluster_read()

@app.post("/user_read", tags=["SCALE API Prod. Reading Actions"])
async def user_read_route():
    return await user_read()

@app.post("/virtualDisk_read", tags=["SCALE API Prod. Reading Actions"])
async def virtualDisk_read_route():
    return await virtualDisk_read()

@app.post("/taskTagStatus_read", tags=["SCALE API Prod. Reading Actions"])
async def taskTagStatus_read_route():
    return await taskTagStatus_read()

@app.post("/vmNetDevices_read", tags=["SCALE API Prod. Reading Actions"])
async def vmNetDevices_read_route():
    return await vmNetDevices_read()

@app.post("/vmSnapshots_read", tags=["SCALE API Prod. Reading Actions"])
async def vmSnapshots_read_route():
    return await vmSnapshots_read()






@app.post("/taskTagStatusFilter", tags=["SCALE API Prod. Run"])
async def taskTagStatusFilter_route(body: TaskTagStatusFilterRequest):
    return await taskTagStatusFilter(taskTag = body.taskTag)


@app.post("/getVM_details", tags=["SCALE API Prod. Run"])
async def getVM_details_route(body: VMDetailsQuery):
    return await getVM_details(vmUUID = body.vmUUID)

@app.post("/getVM_sysStats", tags=["SCALE API Prod. Run"])
async def getVM_sysStats_route(body: VMDetailsQuery):
    return await getVM_sysStats(vmUUID = body.vmUUID)


@app.post("/cloneVM", tags=["SCALE API Prod. Run"])
async def cloneVM_route(body: VMDetailsQuery):
    return await cloneVM(vmUUID = body.vmUUID)

@app.post("/exportVM", tags=["SCALE API Prod. Run"])
async def exportVM_route(body: VMDetailsQuery):
    return await exportVM(vmUUID = body.vmUUID)

@app.post("/changeVM_state", tags=["SCALE API Prod. Run"])
async def changeVM_state_route(body: VMChangeStateQuery):
    return await changeVM_state(vmUUID = body.vmUUID, actionType = body.actionType)

@app.post("/snapshotVM", tags=["SCALE API Prod. Run"])
async def snapshotVM_route(body: VMSnapshotQuery):
    return await snapshotVM(vmUUID = body.vmUUID, label = body.label)

@app.post("/delete_snapshotVM", tags=["SCALE API Prod. Run"])
async def delete_snapshotVM_route(body: VMSnapshotDeleteQuery):
    return await delete_snapshotVM(snapUUID = body.snapUUID)




@app.post("/generate_session", tags=["SCALE Session-Based Tools"])
async def generate_session_route(_: EmptyBody):
    return await generate_session()

@app.post("/get_session", tags=["SCALE Session-Based Tools"])
async def get_session_route(_: EmptyBody):
    return await get_session()

@app.post("/kill_session", tags=["SCALE Session-Based Tools"])
async def kill_session_route(_: EmptyBody):
    return await kill_session()
