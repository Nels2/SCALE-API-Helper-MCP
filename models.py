from pydantic import BaseModel
from typing import Optional, Dict, Any

class RunAPIRequest(BaseModel):
    query: str
    method: str
    payload: Optional[Dict[str, Any]] = None

class QueryRequest(BaseModel):
    query: str
    
class TaskTagStatusFilterRequest(BaseModel):
    taskTag: str

class EmptyBody(BaseModel):
    pass

class VMDetailsQuery(BaseModel):
    vmUUID: str

class VMChangeStateQuery(BaseModel):
    vmUUID: str
    actionType: str
    
class VMSnapshotQuery(BaseModel):
    vmUUID: str
    label: str
    
class VMSnapshotDeleteQuery(BaseModel):
    snapUUID: str

class VMQuery(BaseModel):
    user: Optional[str] = None
    name: Optional[str] = None
